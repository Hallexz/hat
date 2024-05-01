from docx import Document
import PyPDF2
from langdetect import detect
import os

import fileinput
from googletrans import Translator



def docx_to_txt(path):
    document = Document(path)
    text = ' '.join([paragraph.text for paragraph in document.paragraphs])
    return text

directory_path = 'summary'

counter = 0  # Initialize a counter
with open('summarys.txt', 'w') as output_file:
    for filename in os.listdir(directory_path):
        if filename.endswith('.docx'):
            docx_path = os.path.join(directory_path, filename)
            text = docx_to_txt(docx_path)
            output_file.write(f'File {counter}: {filename}\n{text}\n\n')  
            counter += 1  

def pdf_to_txt(path):
    pdf_file = open(path, 'rb')
    pdf_reader = PyPDF2.PdfFileReader(pdf_file)
    text = ''
    for page_num in range(pdf_reader.numPages):
        page_obj = pdf_reader.getPage(page_num)
        text += page_obj.extractText()
    pdf_file.close()
    return text

directory_path = 'summary'

with open('summarys.txt', 'a') as output_file:  
    for filename in os.listdir(directory_path):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(directory_path, filename)
            text = pdf_to_txt(pdf_path)
            output_file.write(f'{counter}: {filename}\n{text}\n\n')  
            counter += 1  