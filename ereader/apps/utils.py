import os


def courses_path():
    return os.environ.get("STORAGE_COURSES")


def course_path(course, create=False):
    path = '{}/{}'.format(courses_path(), course['id'])
    if create and not os.path.exists(path):
        os.makedirs(path)
    return path


def section_path(course, section, create=False):
    path = '{}/{}'.format(course_path(course), section['id'])
    if create and not os.path.exists(path):
        os.makedirs(path)
    return path


def file_path(course, section, file, page=None, create=False):
    path = '{}/{}'.format(section_path(course, section), file['id'])

    if page:
        path = '{}p{}'.format(path, page)
    elif create and not os.path.exists(path):
        os.makedirs(path)

    return path
