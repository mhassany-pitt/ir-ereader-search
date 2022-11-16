import os
import shutil
import json
from flask import Blueprint, request, abort, render_template
from apps.transform import process_html, process_image, process_pdf
from apps.utils import courses_path, course_path, section_path, file_path


ereader = Blueprint('ereader', __name__, template_folder='templates')


@ereader.route('/api/courses', methods=['GET'])
def get_courses():
    courses = []

    for path in os.listdir(courses_path()):
        if path.endswith('.json'):
            with open(course_path({'id': path}), 'r') as json_content:
                courses.append(json.load(json_content))

    return courses


@ereader.route('/api/courses/<id>', methods=['GET'])
def get_course(id):
    course_json = course_path({'id': id + '.json'})

    if os.path.exists(course_json):
        with open(course_json, 'r') as json_content:
            return json.load(json_content)

    abort(404)


@ereader.route('/api/courses/<id>', methods=['DELETE'])
def remove_course(id):
    course_dir = course_path({'id': id})
    course_path = '{}.json'.format(course_dir)

    if not os.path.exists(course_path):
        abort(404)
        return

    os.remove(course_path)
    shutil.rmtree(course_dir)

    return {'status': 'ok'}


@ ereader.route('/api/courses/<cid>/<sid>/<fid>/<pnum>', methods=['GET'])
def get_course_resource(cid, sid, fid, pnum):
    path = '{}/{}/{}/{}p{}.html'.format(
        courses_path(), cid, sid, fid, pnum)

    if os.path.exists(path):
        with open(path, 'r') as file:
            return render_template(
                'ereader_page.html',
                content=file.read(),
                root_url=request.url_root
            )

    abort(404)


@ ereader.route('/api/courses', methods=['PATCH'])
def post_course():
    # parse course object into dict
    course = json.loads(request.form.get('model'))

    # persist course.sections.files
    for section in (course['sections'] if 'sections' in course else []):
        for file in (section['files'] if 'files' in section else []):
            form_attr_name = 'file_id[{}]'.format(file['id'])
            if form_attr_name not in request.files:
                continue

            save_file(course, section, file, request.files[form_attr_name])

    remove_orphan_files(course)

    # then store or update courses/[course-id].json
    with open(course_path({'id': course['id'] + '.json'}, True), 'w') as course_json:
        json.dump(course, course_json)

    return {'status': 'ok'}


def save_file(course, section, file, uploaded_file):
    file_path = '{}/{}'.format(section_path(course, section, True), file['id'])
    file_ext = uploaded_file.filename[uploaded_file.filename.rindex('.') + 1:]
    uploaded_file.save(file_path)

    if file_ext == 'pdf':
        process_pdf(course, section, file, file_path)
    elif file_ext in ['png', 'jpg', 'jpeg']:
        process_image(course, section, file, file_path)
    elif file_ext == 'html':
        process_html(course, section, file, file_path)


def remove_orphan_files(course):
    section_ids = [str(section['id']) for section in course['sections']]
    for section_id in os.listdir(course_path(course)):
        p = section_path(course, {'id': section_id})

        if section_id not in section_ids and os.path.isdir(p):
            shutil.rmtree(p)

    for section in course['sections']:
        file_ids = [str(file['id']) for file in (
            section['files'] if 'files' in section else [])]

        p = section_path(course, section)
        for file_id in (os.listdir(p) if os.path.isdir(p) else []):
            if file_id.split('p')[0] not in file_ids or not file_id.endswith('.html'):
                os.remove(file_path(course, section, {'id': file_id}))
