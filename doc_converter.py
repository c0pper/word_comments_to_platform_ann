import docx
from numpy import unicode_

def normalize_fucked_encoding(str):
    char_to_replace = {
        "�": "è",
        "Ã¬": "ì",
        "Ã©": "é",
        "Ã²": "ò",
        "Ã¨": "è",
        "Ã": "à",
        "Ã¹": "ù",
        "à¹": "ù",
        "Ãˆ": "È"
    }
    for key, value in char_to_replace.items():
        str = str.replace(key, value)
    return str

def getTextFromDoc(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        para.text = normalize_fucked_encoding(para.text)
        fullText.append(para.text)
    return ''.join(fullText).encode('cp1252').decode('ISO-8859-1')

# print(getTextFromDoc("input_docs/BANCA AGRICOLA POPOLARE DI RAGUSA SOC. COOP. PER AZIONI/2039349906/annotazioni2039349906_202106241143_2519253b-3907-4a04-99f6-fc85b3984548_annotato.doc.docx"))