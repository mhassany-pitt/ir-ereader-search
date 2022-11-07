import os
import typesense
from flask import Blueprint

client = typesense.Client({
    'nodes': [{'host': 'localhost', 'port': '8108', 'protocol': 'http'}],
    'api_key': os.environ.get("TYPESENSE_API_KEY"),
    'connection_timeout_seconds': 2
})

search = Blueprint('search', __name__, template_folder='templates')


def index(course, section, file, html_content):
    # https://typesense.org/docs/guide/building-a-search-application.html#build-a-search-application
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
