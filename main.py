#!/usr/bin/env python
# Given a .docx file, extract a CSV list of all tagged (commented) text
# This is version 6.0 of the script
# Date: 12 February 2020

from ast import Raise
from doc_converter import getTextFromDoc, normalize_fucked_encoding
import zipfile
from bs4 import BeautifulSoup as Soup
import re
import os
from datetime import datetime
from tqdm import tqdm
from entities import extraction, taxonomy


def get_txt_paths(txt):
        txt = normalize_fucked_encoding(txt)
        txt = re.sub(' +', ' ', txt)
        txt = re.sub('(S\d+)', r'\n\1', txt) # newline ogni enunciato
        tax_txt_file_path = tax_test_folder+"/"+docfile.split('.')[0]+".txt"
        xtr_txt_file_path = xtr_test_folder+"/"+docfile.split('.')[0]+".txt"

        return (tax_txt_file_path, xtr_txt_file_path)


def return_comments_dicts(path: str, docfile: str) -> list:
    """
    In a word file, for every comment in it creates a dict with the text of the comment, the text on which the comment was placed, the start character of the comment and the end character of the comment.
    Then returns a list of dictionaries, one dictionary per comment in the file.
    """

    unzip = zipfile.ZipFile(path+"\\"+docfile)
    try:
        comments = Soup(unzip.read('word/comments.xml'), 'lxml')
        doc = unzip.read('word/document.xml').decode()
        txt = getTextFromDoc(path+"\\"+docfile)
        txt = re.sub('(S\d+)', r'\n\1', txt) # newline ogni enunciato
        txt = re.sub(' +', ' ', txt)
        
        #  test per provare a usare l'intero rigo dove avviene l'annotazione invece che solo la parte evidenziata
        #  perchè a volte le annotazioni fanno cagare
        #  non si può fare perchè rovinerebbe le estrazioni

        # txt_lines = [x.strip() for x in txt.split('\n')]
        # print(txt_lines)


        #populate comments_dicts list with dicts for every comment
        start_loc = {x.group(1): x.start() for x in re.finditer(r'<w:commentRangeStart.*?w:id="(.*?)"', doc)}
        end_loc = {x.group(1): x.end() for x in re.finditer(r'<w:commentRangeEnd.*?w:id="(.*?)".*?>', doc)}
        comments_dicts = []
        for c in comments.find_all('w:comment'):
            c_id = c.attrs['w:id']
            # Use the locations we found earlier to extract the xml fragment from the document for
            # each comment ID, adding spaces to separate any paragraphs in multi-paragraph comments
            xml = re.sub(r'(<w:p .*?>)', r'\1 ', doc[start_loc[c_id]:end_loc[c_id] + 1])
            # print(xml+"\n\n")
            cmt = ''.join(c.findAll(text=True))
            cmt = re.sub(' +', ' ', cmt)
            text_reference_soup = Soup(xml, 'lxml').findAll(text=True)
            if len(text_reference_soup) > 1:
                text_reference = "".join(text_reference_soup)     
            else:
                # text_reference = ''.join(text_reference_soup).encode('cp1252').decode('ISO-8859-1')
                text_reference = text_reference_soup[0]
            
            text_reference = normalize_fucked_encoding(text_reference)
            text_reference = re.sub(' +', ' ', text_reference)
            text_reference = re.sub('(S\d+)', r'\n\1', text_reference)
            
            cmt_and_txt = {"comment": cmt.split(";")[0].strip(), "text": text_reference, "start":txt.find(text_reference), "end": txt.find(text_reference)+len(text_reference)}
            print(cmt_and_txt)

            comments_dicts.append(cmt_and_txt)
        return comments_dicts
    except KeyError:
        print(f"No comments found in {path}+\+{docfile}")
        return False


def create_annotation_and_text_file(path: str, docfile: str, comments_dicts: list):
    """
    Highlited only mode: for every comment in the current file, create an ann file with the annotation for the text highlighted by the comment. This works better for autoML
    Non Highlited only mode: create a single ann file for the current file with all the annotations for all the comments
    """
    if highlited_only_mode:
        for idx, c in enumerate(comments_dicts):
            if c['comment'].lower() in taxonomy:
                with open(tax_test_folder+"/"+docfile.split('.')[0]+"_"+str(idx)+".txt", 'w', encoding="utf-8") as file:
                    # print(txt)
                    file.write(c['text'])
                    
                with open(tax_ann_folder+"/"+docfile.split('.')[0]+"_"+str(idx)+".ann", 'a', encoding="utf-8") as ann:
                    tax_count = 1
                    # print("TAX: ", c["text"])
                    ann.write(f"C{tax_count}		{taxonomy[c['comment'].lower()]}\n")


            if c['comment'].lower() in extraction:
                if c["start"] == -1:
                    # raise Exception(f"'{c['text']}' not found in text ({docfile.split('.')[0]})")
                    pass
                else:
                    with open(xtr_test_folder+"/"+docfile.split('.')[0]+"_"+str(idx)+".txt", 'w', encoding="utf-8") as file:
                        # print(txt)
                        file.write(c['text'])
                    with open(xtr_ann_folder+"/"+docfile.split('.')[0]+"_"+str(idx)+".ann", 'a', encoding="utf-8") as ann:
                        xtr_count = 1
                        # print("XTR: ", c["text"])
                        ann.write(f"T{xtr_count}		{extraction[c['comment'].lower()]} {c['start']} {c['end']}	{c['text']}\n")

    if not highlited_only_mode:
        tax_count = 1
        xtr_count = 1
        
        txt = getTextFromDoc(path+"\\"+docfile)
        tax_txt_file_path, xtr_txt_file_path = get_txt_paths(txt)

        # txt = getTextFromDoc(path+"\\"+docfile)
        # txt = normalize_fucked_encoding(txt)
        # txt = re.sub(' +', ' ', txt)
        # txt = re.sub('(S\d+)', r'\n\1', txt) # newline ogni enunciato
        # tax_txt_file_path = tax_test_folder+"/"+docfile.split('.')[0]+".txt"
        # xtr_txt_file_path = xtr_test_folder+"/"+docfile.split('.')[0]+".txt"

        for c in comments_dicts:
            if c['comment'].lower() in taxonomy:
                if not os.path.exists(tax_txt_file_path):
                    print(f"{tax_txt_file_path} not exist")
                    with open(tax_test_folder+"/"+docfile.split('.')[0]+".txt", 'a', encoding="utf-8") as text_file:
                        text_file.write(txt)
                else:
                    print(f"{tax_txt_file_path} exist")

                with open(tax_ann_folder+"/"+docfile.split('.')[0]+".ann", 'a', encoding="utf-8") as ann:
                    # for c in comments_dicts:
                    ann.write(f"C{tax_count}		{taxonomy[c['comment'].lower()]}\n")
                    tax_count +=1

            if c['comment'].lower() in extraction:
                if not os.path.exists(xtr_txt_file_path):
                    print(f"{xtr_txt_file_path} not exist")
                    with open(xtr_test_folder+"/"+docfile.split('.')[0]+".txt", 'a', encoding="utf-8") as text_file:
                        text_file.write(txt)
                else:
                    print(f"{xtr_txt_file_path} exist")

                with open(xtr_ann_folder+"/"+docfile.split('.')[0]+".ann", 'a', encoding="utf-8") as ann:
                    # for c in comments_dicts:
                    if c["start"] == -1:
                        # raise Exception(f"'{c['text']}' not found in text ({docfile.split('.')[0]})")
                        pass
                    else:
                        ann.write(f"T{xtr_count}		{extraction[c['comment'].lower()]} {c['start']} {c['end']}	{c['text']}\n")
                        xtr_count +=1
    print(f"Found {len(comments_dicts)} annotations")


def create_zip():
    for i in [tax_folder, xtr_folder]:
        os.chdir(i)
        split = 0.8
        #create train lib
        with zipfile.ZipFile(f'{i.split("/")[-1]}_train_lib{timenow}.zip', 'w') as zipObj:
            for root, dirs, files in os.walk(f'ann'):
                for f in files[:int(len(files)*split)]:
                    zipObj.write(os.path.join(root, f))
            for root, dirs, files in os.walk(f'test'):
                for f in files[:int(len(files)*split)]:
                    zipObj.write(os.path.join(root, f))
        #create test lib
        with zipfile.ZipFile(f'{i.split("/")[-1]}_test_lib{timenow}.zip', 'w') as zipObj:
            for root, dirs, files in os.walk(f'ann'):
                for f in files[int(len(files)*split):]:
                    zipObj.write(os.path.join(root, f))
            for root, dirs, files in os.walk(f'test'):
                for f in files[int(len(files)*split):]:
                    zipObj.write(os.path.join(root, f))
        os.chdir("../../..")


if __name__ == "__main__":
    highlited_only_mode = True #  se True, invece che creare un annotazione dell'intero documento, crea un annotazione del segmento di testo commentato

    runs_folder_path = input("input the path where the run output should be stored: ").replace("\\","/")
    if os.path.exists(runs_folder_path):
        timenow = datetime.now().strftime('%d_%m_%y_%H_%M')
        tax_folder = f"{runs_folder_path}/run_{timenow}/tax"
        xtr_folder = f"{runs_folder_path}/run_{timenow}/xtr"
        tax_test_folder = f"{runs_folder_path}/run_{timenow}/tax/test"
        tax_ann_folder = f"{runs_folder_path}/run_{timenow}/tax/ann"
        xtr_test_folder = f"{runs_folder_path}/run_{timenow}/xtr/test"
        xtr_ann_folder = f"{runs_folder_path}/run_{timenow}/xtr/ann"
        os.makedirs(tax_folder, exist_ok=True)
        os.makedirs(xtr_folder, exist_ok=True)
        os.makedirs(tax_test_folder, exist_ok=True)
        os.makedirs(tax_ann_folder, exist_ok=True)
        os.makedirs(xtr_test_folder, exist_ok=True)
        os.makedirs(xtr_ann_folder, exist_ok=True)


        for root, dirs, files in os.walk('C:\\Users\\smarotta\\Desktop\\trasc_ann\\post_11-07-22'):
            for f in tqdm(files):
                print("---------\n" + "WORKING ON: " + os.path.join(root, f))
                file_comments_dicts = return_comments_dicts(root, f)
                if "_annotato" in f:
                    if file_comments_dicts:
                        print(root, f)
                        create_annotation_and_text_file(root, f, file_comments_dicts)
        create_zip()
    else:
        raise Exception(f"Path {runs_folder_path} doesn't exist")