from flask import Blueprint


search = Blueprint('search', __name__, template_folder='templates')


def index_html(course, section, file, html_file_path):
    ''' index given html file '''

    # whenever a new page is added to a course, this function will be called.
    # course, section, and file has the following format
    # html_file_path needs to be indexed (it is a single html file - a pdf page, uploaded image/web-page)
    # use typesense to index it.

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
    #                     "depth": 0,
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

    # later on we will use this function to query/search within the index

    return []
