from flask import Blueprint


search = Blueprint('search', __name__, template_folder='templates')


def index_html(course, section, file, html_file_path):
    ''' index given html file '''
    # ----> course, section, and file format
    # {
    #     "id": "INFSCI2140",
    #     "teacher": "Dr. Daqin He",
    #     "title": "Information Storage & Retrieval",
    #     "sections": [
    #         {
    #             "id": 1,
    #             "title": "Session 01",
    #             "files": [
    #                 {
    #                     "id": 2,
    #                     "title": "Introduction to IR",
    #                     "page_count": 2,
    #                     "page_size": {
    #                         "0": "612,792"
    #                     },
    #                 }
    #             ]
    #         }
    #     ],
    #     "i": 37, <-- auto increment (used for generating unique id)
    # }

    return 0


@search.route('/api/search', methods=['GET'])
def query():
    ''' perform search '''
    return []
