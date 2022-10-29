import os
import shutil
import json
import traceback
import subprocess
from flask import Flask, request, abort, send_file
from flask_cors import CORS
from PyPDF2 import PdfFileReader, PdfFileWriter

app = Flask(__name__)
CORS(app)

# storage path
storage_dir = './storage'
courses_dir = '{}/courses'.format(storage_dir)

# download https://pdfbox.apache.org/download.html
pdfbox_app = './utils/pdfbox-app.jar'


@app.route('/api/courses', methods=['GET'])
def get_courses():
    courses = []

    for path in os.listdir(courses_dir):
        if path.endswith('.json'):
            with open('{}/{}'.format(courses_dir, path), 'r') as json_content:
                courses.append(json.load(json_content))

    return courses


@app.route('/api/courses/<id>', methods=['GET'])
def get_course(id):
    course_path = '{}/{}.json'.format(courses_dir, id)
    if not os.path.exists(course_path):
        abort(404)
        return

    with open(course_path, 'r') as json_content:
        return json.load(json_content)


@app.route('/api/courses/<id>', methods=['DELETE'])
def remove_course(id):
    course_dir = '{}/{}'.format(courses_dir, id)
    course_path = '{}.json'.format(course_dir)

    if not os.path.exists(course_path):
        abort(404)
        return

    os.remove(course_path)
    shutil.rmtree(course_dir)

    return {'status': 'ok'}


@app.route('/api/courses/<course_id>/<section_id>/<file_id>/<page>', methods=['GET'])
def get_course_pdf_page(course_id, section_id, file_id, page):
    pdf_path = '{}/{}/{}/{}p{}.pdf'.format(
        courses_dir, course_id, section_id, file_id, page)

    if os.path.exists(pdf_path):
        return send_file(pdf_path, mimetype='application/pdf')
    else:
        abort(404)


@app.route('/api/courses', methods=['PATCH'])
def post_course():
    # parse course object into dict
    model = json.loads(request.form.get('model'))

    # ensure courses/[course-id] dir exists
    course_dir = '{}/{}'.format(courses_dir, model['id'])
    if not os.path.exists(course_dir):
        os.makedirs(course_dir)

    # persist course.sections.files
    for section in (model['sections'] if 'sections' in model else []):
        # ensure course/[course-id]/[section-id] dir
        section_dir = '{}/{}'.format(course_dir, section['id'])
        if not os.path.exists(section_dir):
            os.makedirs(section_dir)

        for file in (section['files'] if 'files' in section else []):
            name = 'file_id[{}]'.format(file['id'])
            if name not in request.files:
                continue

            new_file = request.files[name]
            ext = new_file.filename.split('.')[1]
            target = '{}/{}.{}'.format(section_dir, file['id'], ext)

            new_file.save(target)

            if ext != 'pdf':
                continue

            file['mediabox'] = {}
            file['pages'] = split_pdf(section_dir, file, target)

    # store courses/[course-id].json
    with open('{}.json'.format(course_dir), 'w') as file:
        json.dump(model, file)

    return {'status': 'ok'}


def split_pdf(section_dir, file, target):
    prefix = '{}/{}p'.format(section_dir, file['id'])

    src_pdf = open(target, 'rb')
    reader = PdfFileReader(src_pdf)

    last_mediabox = None

    for i, page in enumerate(reader.pages):
        writer = PdfFileWriter()
        writer.addPage(page)

        with open(prefix + str(i) + '.pdf', 'wb') as pdf_page:
            writer.write(pdf_page)

        mediabox = ','.join([
            str(page.mediabox.width),
            str(page.mediabox.height)
        ])

        if mediabox != last_mediabox:
            file['mediabox'][i] = mediabox
            last_mediabox = mediabox

    src_pdf.close()
    os.remove(target)

    return len(reader.pages)
