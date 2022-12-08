import os
import pytesseract
import subprocess
from PyPDF2 import PdfFileReader, PdfFileWriter
from apps.utils import file_path
from apps.search import index


def process_pdf(course, section, file, src_pdf_file_path, p_count):
    ''' break pdf into pages '''
    file['page_size'] = {}

    src_pdf_file = open(src_pdf_file_path, 'rb')
    pdf_reader = PdfFileReader(src_pdf_file)

    last_page_size = None

    for fpage_i, pdf_page in enumerate(pdf_reader.pages):
        pdf_writer = PdfFileWriter()
        pdf_writer.addPage(pdf_page)

        page_size = ','.join([str(pdf_page.mediabox.width),
                              str(pdf_page.mediabox.height)])
        if page_size != last_page_size:
            file['page_size'][fpage_i] = page_size
            last_page_size = page_size

        pdf_page_path = file_path(course, section, file, str(fpage_i))
        with open(pdf_page_path, 'wb') as pdf_page_file:
            pdf_writer.write(pdf_page_file)

        pdf_2_html(course, section, file, fpage_i,
                   pdf_page_path, p_count + fpage_i)

        os.remove(pdf_page_path)

    os.remove(src_pdf_file_path)

    src_pdf_file.close()

    file['page_count'] = len(pdf_reader.pages)

    return file['page_count']


def process_image(course, section, file, src_image_file_path, p_count):
    ''' convert image into single page pdf '''
    pdf_file_path = '{}.pdf'.format(src_image_file_path)

    with open(pdf_file_path, 'w+b') as pdf_file:
        pdf_file.write(pytesseract.image_to_pdf_or_hocr(
            src_image_file_path, extension='pdf'))

    os.remove(src_image_file_path)

    return process_pdf(course, section, file, pdf_file_path, p_count)


def process_html(course, section, file, src_html_file_path, p_count):
    ''' process uploaded html file '''
    html_file_path = '{}p0.html'.format(src_html_file_path)
    os.rename(src_html_file_path, html_file_path)

    with open(html_file_path, 'r') as html_file:
        html_content = html_file.read()
        index(course, section, file, 0, html_content, p_count)

    return 1


def pdf_2_html(course, section, file, fpage_i, pdf_path, page_i):
    ''' convert single page pdf to html '''
    # -- pdftohtml conversion --
    # https://github.com/coolwanglu/pdf2htmlEX
    # Docker image - 1.23GB by Kim Lokøy kim.lokoy@gmail.com
    # docker run -ti --rm -v ~/Desktop:/pdf bwits/pdf2htmlex pdf2htmlEX --zoom 1.3 test.pdf

    slash_index = pdf_path.rindex('/')
    command = 'docker run -ti --rm -v "{}":/pdf bwits/pdf2htmlex pdf2htmlEX --zoom 1.3 {}'\
        .format(os.path.abspath(pdf_path[:slash_index]), pdf_path[slash_index+1:])

    subprocess.run([command], shell=True)

    with open('{}.html'.format(pdf_path), 'r') as html_file:
        html_content = html_file.read()
        index(course, section, file, fpage_i, html_content, page_i)
