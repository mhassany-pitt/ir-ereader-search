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
# "ref" which will hold oru reference scheme and the content 
# as the html. This is what will be called to search for specific
# content, which needs to be passsed tot he result of the search 
# function.

schema =  {
    "name": "pages", 
    "fields": [
    {
    "name": "reference_information",
    "type": "string"
    },
    {
    "name": "content",
    "type": "string"
    }
    ]
}

# This creates the schema in typesense. 

try:
    client.collections['pages'].delete()
except Exception as e:
    pass

client.collections.create(schema)
#client.collections['pages'].update(schema)

def index(course, section, file, page_num, html_content):
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
    result = Tree.tostring(tree.getroot(), pretty_print=True, method="html").decode()

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
            parser.feed(item)

    # This is the empty string that will be used to hold the content. 
    content_string = ''

    # For each item in the list of content, that item is appended to 
    # the content_string that will be passed as content to the index. 

    ## Note ## This is not perfect.  But it will work for now so that 
    # Emily can get the search feature going.  I will work to improve 
    # This method. Ultimately, whatever solution I come up with, content 
    # will be returned as a single string representing a single page of 
    # content. 
    for item in parsed_text:
            content_string += f'{item}' 

    # This is the document that will be added to the index. 
    document = {
        "reference_information": f"c{course}s{section}f{file}p{page_num}",
        "content": content_string
    }

    # This is the command in type sense to add the document. 
    client.collections['pages'].documents.upsert(document)
    return 0


@search.route('/api/search', methods=['POST'])
def do_search():
    ''' perform search '''
    query_text = request.values.get('qtext')

    # ... search and return the results

    return []
