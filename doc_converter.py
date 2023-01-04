"""
    doc_converter.py
    ----------------

    This module contains helper functions to retrieve and process the text extracted from docx files
"""

import docx
from pathlib import Path


def normalize_fucked_encoding(string) -> str:
    """
    Manually replace bad characters. See https://www.i18nqa.com/debug/utf8-debug.html

    :param string: text to be normalized
    :return: normalized string
    """
    char_to_replace = {
        "�": "è",  # almeno prendo la maggior parte dei verbi essere correttamente
        "Ã¬": "ì",
        "Ã©": "é",
        "Ã²": "ò",
        "Ã¨": "è",
        "Ã": "à",
        "Ã¹": "ù",
        "à¹": "ù",
        "Ãˆ": "È",
    }
    for key, value in char_to_replace.items():
        string = string.replace(key, value)
    return string


def get_text_from_doc(filename: Path) -> str:
    """
    Retrieve text from docx file

    :param filename: path of a single word document (.docx)
    :return: text in string form
    """
    doc = docx.Document(filename)
    full_text = []
    for para in doc.paragraphs:
        para.text = normalize_fucked_encoding(para.text)
        full_text.append(para.text)
    return ''.join(full_text).encode('cp1252').decode('ISO-8859-1')

