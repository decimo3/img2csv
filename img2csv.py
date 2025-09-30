#!/bin/env python
''' Program wrapper to Tesseract '''
import os
import sys
import mimetypes
from tkinter.filedialog import askopenfilenames
import cv2
import pandas
import pytesseract
import dotenv

# Set what environment it is
DEV_ENV = not getattr(sys, 'frozen', False)

# Set variable that define the folder that it's executed
if not DEV_ENV:
    BASE_FOLDER = os.path.dirname(sys.executable)
else:
    BASE_FOLDER = os.path.dirname(os.path.abspath(__file__))

# Load configuration file
dotenv.load_dotenv(os.path.join(BASE_FOLDER, 'img2csv.conf'))

# Build Tesseract command arguments using tessdata directory from environment
CMDARG = '--tessdata-dir ' + os.getenv('TESSDATA', '')

# Get image slices from environment variable, split by comma
SLICES = os.getenv('SLICES', '').split(',')

def get_table_from_string(text: str) -> tuple[list[str], list[str]]:
    ''' Method to transform string to CSV table '''
    head: list[str] = []
    body: list[str] = []
    for line in text.split('\n'):
        if not line:
            continue
        if line.endswith(':'):
            head.append(line)
            continue
        body.append(line)
    if len(body) == 0:
        body.append('')
    print(head)
    print()
    print(body)
    return head, body

def get_string_from_image(filepath: str) -> pandas.DataFrame:
    ''' Method to extract string from image '''
    heads: list[str] = []
    bodys: list[str] = []
    # Open an image file
    img = cv2.imread(filepath) # pylint: disable=no-member
    if img is None:
        raise Exception(f'Não foi possível abrir o arquivo {filepath}!')
    for i, (y1, y2, x1, x2) in enumerate(SLICES):
        slice_img = img[y1:y2, x1:x2]
        if DEV_ENV:
            cv2.imshow(f"Slice {i}", slice_img) # pylint: disable=no-member
        # Extract text from the image
        text = pytesseract.image_to_string(image=slice_img, lang='por')
        values = get_table_from_string(text)
        heads.extend(values[0])
        bodys.extend(values[1])
    return pandas.DataFrame(data=[bodys], columns=heads)

if __name__ == '__main__':
    TESSPATH = os.getenv('TESSPATH')
    if not TESSPATH or not os.path.exists(TESSPATH):
        raise FileExistsError('Tesseract-OCR is not installed on default path!')
    # If Tesseract is not in your system PATH, specify its executable path
    pytesseract.pytesseract.tesseract_cmd = TESSPATH
    # Ask for file if file is not specified on arguments
    filepaths = sys.argv[1:] if len(sys.argv) > 1 else askopenfilenames()
    all_results = []
    for filepath in filepaths:
        if not os.path.exists(filepath):
            print(f'O arquivo {filepath} não está acessível! Pulando...')
            continue
        mimetype = mimetypes.guess_type(filepath)
        if mimetype[0] and not mimetype[0].startswith('image'):
            print(f'O arquivo {filepath} não é suportado! Pulando...')
            continue
        result = get_string_from_image(filepath)
        all_results.append(result)
    dataframe = pandas.concat(all_results, ignore_index=True)
    filepath = os.path.join(os.path.dirname(filepaths[0]), 'result.csv')
    dataframe.to_csv(filepath, index=False, sep=';', encoding='1252')
    os.startfile(filepath)
