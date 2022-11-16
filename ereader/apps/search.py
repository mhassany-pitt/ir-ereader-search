import os
import typesense
from flask import Blueprint, request, abort, render_template

client = typesense.Client({
    'nodes': [{
        'host': os.environ.get("TYPESENSE_HOST"),
        'port': os.environ.get("TYPESENSE_PORT"),
        'protocol': os.environ.get("TYPESENSE_PROTOCOL"),
    }],
    'api_key': os.environ.get("TYPESENSE_API_KEY"),
    'connection_timeout_seconds': int(os.environ.get("TYPESENSE_CONNECTION_TIMEOUT_SECONDS"))
})

search = Blueprint('search', __name__, template_folder='templates')


def index(course, section, file, page_num, html_content):
    # https://typesense.org/docs/guide/building-a-search-application.html#build-a-search-application
    ''' index given html content '''

    # whenever a new page is added to a course, this function will be called.
    # course, section, and file has the following format

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


@search.route('/api/search', methods=['POST'])
def do_search():
    ''' perform search '''
    query_text = request.values.get('qtext')

    # ... search and return the results

    return []
