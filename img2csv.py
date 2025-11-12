#!/bin/env python
''' Program wrapper to Tesseract '''
import os
import sys
import mimetypes
from tkinter.filedialog import askopenfilenames
from PIL import Image, UnidentifiedImageError
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

class NotIsImageException(Exception):
    ''' Custon exception to indicate that file is not a image '''

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

def get_dataframe_from_image(filepath: str) -> pandas.DataFrame:
    ''' Method to extract string from image '''
    heads: list[str] = []
    bodys: list[str] = []
    # Open an image file
    try:
        img = Image.open(filepath).convert('RGB')
    except (FileNotFoundError, UnidentifiedImageError, ValueError, TypeError) as e:
        raise NotIsImageException(f'Não foi possível abrir o arquivo {filepath}!') from e

    df: pandas.DataFrame = pytesseract.image_to_data(
        image=img,
        lang='por',
        config=CMDARG,
        output_type=pytesseract.Output.DATAFRAME)

    if not isinstance(df, pandas.DataFrame):
        raise ValueError('O resultado gerado não condiz com o solicitado!')

    # Filtra textos válidos
    df = df[(df.conf > 0) & (df.text.notnull()) & (df.text.str.strip() != '')].copy()
    df['text'] = df['text'].str.strip()

    lines_nums: list[int] = sorted(df['line_num'].unique())


    skipt_line: int = 0
    # Alternância: linha ímpar = cabeçalhos / linha par = dados
    for i in range(0, len(lines_nums), 2):
        line_head_num = lines_nums[i + skipt_line]
        line_data_num = lines_nums[i + 1 + skipt_line] if i + 1 + skipt_line < len(lines_nums) else None

        # Palavras de cabeçalho e dados
        head_line = df[df.line_num == line_head_num].copy()
        data_line = df[df.line_num == line_data_num].copy() if line_data_num else pandas.DataFrame()

        # Ordenar por posição x
        head_line = head_line.sort_values('left')
        data_line = data_line.sort_values('left') if not data_line.empty else data_line

        # Verifica se a linha realmente é de cabeçalhos
        if not any(head_line['text'].str.endswith(':')):
            # Trata como linha de dados sem cabeçalho
            if i == 0:
                heads = ['Título:']
                text = ' '.join(head_line['text'].tolist()).strip()
                bodys = [text]
            skipt_line = 1
            # Reassignment to variables after skipt one row
            line_head_num = lines_nums[i + skipt_line]
            line_data_num = lines_nums[i + 1 + skipt_line] if i + 1 + skipt_line < len(lines_nums) else None
            head_line = df[df.line_num == line_head_num].copy()
            data_line = df[df.line_num == line_data_num].copy() if line_data_num else pandas.DataFrame()
            head_line = head_line.sort_values('left')
            data_line = data_line.sort_values('left')

        # Divide linha de cabeçalhos em colunas
        current: str = ''
        check_pos: bool = False
        positions: list[int] = []
        for _, word in head_line.iterrows():
            if check_pos:
                positions.append(word['left'] - 10)
                check_pos = False
            current += ' ' + word['text']
            if word['text'].endswith(':'):
                heads.append(current.strip())
                check_pos = True
                current = ''
        if current:
            heads.append(current.strip())

        positions.append(img.width)

        left_prev: int = 0
        for pos in positions:
            if data_line.empty:
                bodys.append('')
                continue
            words = data_line[(data_line['left'] >= left_prev) & (data_line['left'] < pos)]
            text = ' '.join(words['text'].tolist())
            bodys.append(text.strip())
            left_prev = pos

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
        result = get_dataframe_from_image(filepath)
        all_results.append(result)
    dataframe = pandas.concat(all_results, ignore_index=True)
    filepath = os.path.join(os.path.dirname(filepaths[0]), 'result.csv')
    dataframe.to_csv(filepath, index=False, sep=';', encoding='1252')
    os.startfile(filepath)
