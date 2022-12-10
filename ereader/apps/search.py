import os
import typesense
from flask import Blueprint, request, abort, render_template
from lxml import etree as Tree
from html.parser import HTMLParser
from io import StringIO

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

# Create a schema to hold the collection

# This is required by typesense to hold the schema that
# will be used to index our data. By setting a schema
# we can index documents using the same "format".

# Essentially, each document in typsense will have this
# "c_id,s_id,f_id,fp_i,p_i" which will hold reference and the content
# as the html. This is what will be called to search for specific
# content, which needs to be passsed tot he result of the search
# function.

schema = {
    'name': 'pages',
    'fields': [
        {'name': 'c_id', 'type': 'string'},
        {'name': 's_id', 'type': 'int64'},
        {'name': 'f_id', 'type': 'int64'},
        {'name': 'fp_i', 'type': 'int64'},
        {'name': 'p_i', 'type': 'int64'},
        {'name': 'content', 'type': 'string'},
        {"name": "sentences", "type": "string[]"}
    ]
}

# This creates the schema in typesense.
try:
    # # -- uncomment to reset
    # client.collections['pages'].delete()
    client.collections.create(schema)
except Exception as e:
    pass


def index(course, section, file, fpage_i, html_content, page_i):
    # This part of the indexing function parses the html.
    # This code is kind of ugly but it works and I have
    # more fine grained control over what is happening,
    # should I need to change or update something.

    # This creates a parser object to be used by the lxml package
    parser = Tree.HTMLParser()

    # This parses html content using lxml.  This is a very basic
    # parsing and is stored as a bytes object. This DOES NOT extract
    # the content from the parsed HTML.  The content, at this point
    # is still held between tags.
    tree = Tree.parse(StringIO(html_content), parser)

    # This decodes the bytes and converts the content to a string.
    # the pretty_print method is set to True so this can be printed
    # and read by a human, but it is not necessary for parsing. Again
    # at this point, no content has been extracted.
    result = Tree.tostring(
        tree.getroot(), pretty_print=True, method="html").decode()

    # Here I splie the sting of decoded html on the newline character.
    # Tags are still included and content has not yet been extracted.
    splitter = result.split('\n')

    # This initializes a list that I used to filter unimportant tags.
    # Below, I iterate through each line with the HTML tags, and
    # append lines containing tags, that have content within the tags.
    important_tags = []

    # This is the portion of the code that filters the unimportant tags.
    # for each line in the parsed HTML content, strip the white space
    # from the line, and if the line is not empty, it starts with a "<"
    # and it does not inlcude <style, then that line is appended
    for line in splitter:
        stripped = line.lstrip()
        if stripped != '' and stripped[0] == '<' and "<style" not in stripped:
            important_tags.append(stripped)

    # This is a list which will hold a list of the content from
    # the parsed HTML.
    parsed_text = []

    # This is an object that I used to extract the content. The sole
    # function of this object is to extract the content from between tags.
    class MyHTMLParser(HTMLParser):
        def handle_data(self, data):
            parsed_text.append(data)

    # This contains the content extracting object in the lines above.
    parser = MyHTMLParser()

    # This function extracts the content from each of the tags.
    for item in important_tags:
        # Catch parsing error
        if len(item) >= 7 and item[-7] == '-':
            catch_error = item.replace('-', '')
            parser.feed(catch_error)
        elif len(item) >= 7 and item[-7] != '-':
            catch_error = item + ' '
            parser.feed(catch_error)
        else:
            parser.feed(item)

    # This is the empty string that will be used to hold the content.
    content_string = ''

    # This will hold a list of each sentence.
    # I split on '. ' the extra space after the "." should help identify sentences only.
    split_content = content_string.split('. ')

    # Added functionality if we ever want to implement word specific data.
    # This holds each word in the entire page.
    no_ws = []
    words = content_string.split(' ')
    for word in words:
        if len(word) != 0:
            no_ws.append(word)
        else:
            pass

    # Added functionality if we ever want sentences that are split into each individual word.
    words_by_sentence = []
    for sentence in split_content:
        split_sentence = sentence.split(' ')
        words_by_sentence.append(split_sentence)

    # For each item in the list of content, that item is appended to
    # the content_string that will be passed as content to the index.

    # Note ## This is not perfect.  But it will work for now so that
    # Emily can get the search feature going.  I will work to improve
    # This method. Ultimately, whatever solution I come up with, content
    # will be returned as a single string representing a single page of
    # content.
    for item in parsed_text:
        content_string += f'{item}'

    # This is the document that will be added to the index.
    document = {
        'c_id': course['id'],
        's_id': section['id'],
        'f_id': file['id'],
        'fp_i': fpage_i,  # file_page_index
        'p_i': page_i,  # page_index
        'content': content_string,
        'sentences': split_content
    }

    # This is the command in type sense to add the document.
    client.collections['pages'].documents.upsert(document)


@search.route('/api/search', methods=['POST'])
def do_search():
    ''' perform search '''
    # qet the 'query' value and pass it to typesense to search
    # only search in the specified course (c_id)
    return client.collections['pages'].documents.search({
        'q': request.json['query'],
        'query_by': 'content',
        'filter_by': 'c_id:' + request.json['c_id'],
        'sort_by': 'p_i:asc'
    })
