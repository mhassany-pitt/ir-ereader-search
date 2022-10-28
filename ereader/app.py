import os
import shutil
import json
import traceback
from flask import Flask, render_template, request, abort, redirect, url_for
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

storage_dir = './storage'
courses_dir = '{}/courses'.format(storage_dir)


@app.route("/")
def index():
    # return render_template('index.html')
    return ''


@app.route("/api/index", methods=["GET"])
def should_index():
    for path in os.listdir(courses_dir):
        if path.endswith('.reindex'):
            return {'state': 'ok'}

    abort(404)


@app.route("/api/index", methods=["PATCH"])
def index_updates():
    # TODO: index *.reindex files
    return {'state': 'ok'}


@app.route("/api/courses", methods=["GET"])
def get_courses():
    courses = []

    for path in os.listdir(courses_dir):
        if path.endswith('.json'):
            with open('{}/{}'.format(courses_dir, path), 'r') as json_content:
                courses.append(json.load(json_content))

    return courses


@app.route("/api/courses/<id>", methods=["GET"])
def get_course(id):
    course_path = '{}/{}.json'.format(courses_dir, id)
    if not os.path.exists(course_path):
        abort(404)
        return

    with open(course_path, 'r') as json_content:
        return json.load(json_content)


@app.route("/api/courses/<id>", methods=["DELETE"])
def remove_course(id):
    course_dir = '{}/{}'.format(courses_dir, id)
    course_path = '{}.json'.format(course_dir)

    if not os.path.exists(course_path):
        abort(404)
        return

    os.remove(course_path)
    shutil.rmtree(course_dir)

    return {'status': 'ok'}


@app.route("/api/courses", methods=["PATCH"])
def post_course():
    # parse course object into dict
    model = json.loads(request.form.get('model'))

    # ensure courses/[course-id] dir exists
    course_dir = '{}/{}'.format(courses_dir, model['id'])
    if not os.path.exists(course_dir):
        os.makedirs(course_dir)

    # store courses/[course-id].json
    with open('{}.json'.format(course_dir), 'w') as file:
        json.dump(model, file)

    new_files = []

    # persist course.sections.files
    for section in (model['sections'] if 'sections' in model else []):
        # ensure course/[course-id]/[section-id] dir
        section_dir = '{}/{}'.format(course_dir, section['id'])
        if not os.path.exists(section_dir):
            os.makedirs(section_dir)

        for file in (section['files'] if 'files' in section else []):
            name = 'file_id[{}]'.format(file['id'])

            if name in request.files:
                new_file = request.files[name]
                ext = new_file.filename.split('.')[1]
                target = '{}/{}.{}'.format(section_dir, file['id'], ext)

                # overwrite (delete old one and create new)
                if os.path.exists(target):
                    os.remove(target)
                new_file.save(target)

                new_files.append(target)

    # mark pending files to re-index
    with open('{}.reindex'.format(course_dir), 'w') as file:
        file.write('\n'.join(new_files))

    return {'status': 'ok'}
