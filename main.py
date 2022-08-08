#!/usr/bin/env python
# Given a .docx file, extract a CSV list of all tagged (commented) text
# This is version 6.0 of the script
# Date: 12 February 2020

from doc_converter import getTextFromDoc, normalize_fucked_encoding
import zipfile
from bs4 import BeautifulSoup as Soup
import re
import os
from datetime import datetime
from tqdm import tqdm


taxonomy = {
    #  entità operatore
    "presentazione società": "presentazione_societa",
    "presentazione prodotto": "presentazione_prodotto",
    "dettaglio esposizione": "dettaglio_esposizione",
    "interlocutore alternativo": "interlocutore_alternativo",
    "recapiti alternativi": "recapiti_alternativi",
    "stato attività impresa": "stato_attivita_impresa",
    "scadenza pagamento": "scadenza_pagamento",
    "volontà risolutiva": "volonta_risolutiva",
    "appuntamento": "appuntamento",
    "bene finanziato": "bene_finanziato",
    "situazione economica": "situazione_economica",
    "altre disponibilità": "altre_disponibilita",
    "nucleo familiare": "nucleo_familiare",
    "capacità di rimborso": "capacita_di_rimborso",
    "impegni economici": "impegni_economici",
    "proposta agevolazione": "proposta_agevolazione",
    "proposta saldo e stralcio": "proposta_saldo_e_stralcio",
    "proposto pdr": "proposto_pdr",
    "proposto rifinanziamento": "proposto_rifinanziamento",
    "proposto accodamento": "proposto_accodamento",
    "proposto consolidamento": "proposto_consolidamento",
    "antiusura": "antiusura",
    "proiezione medio lungo termine": "proiezione_medio_lungo_termine",
    "sostegno da terzi": "sostegno_da_terzi",
    "tempistiche introiti": "tempistiche_introiti",
    "pagamento effettuato": "pagamento_effettuato",
    "utilizzo leve": "utilizzo_leve",
    "conferma accordi": "conferma_accordi",
    "estremi di pagamento": "estremi_di_pagamento",
    "richiesto riscontro di pagamento": "richiesto_riscontro_di_pagamento",
    "invio modulistica": "invio_modulistica",
    "richiesta documenti": "richiesta_documenti",
    "invito a confronto diretto": "invito_a_confronto_diretto",

    #  entità debitore
    "non è a conoscenza del debito": "ignora_debito",
    "maggiori dettagli su debito": "maggiori_dettagli_debito",
    "vuole confronto diretto con mandante": "confronto_diretto_mandante",
    "volontà pagamento": "volonta_pagamento",
    "volontà di pagamento": "volonta_pagamento",
    "rifiuta pagamento": "rifiuta_pagamento",
    "contestazione": "contestazione",
    "potenziale reclamo": "potenziale_reclamo",
    "in attesa liquidità": "attesa_liquidita",
    "richiesta agevolazione": "richiesta_agevolazione",
    "chiede/rimanda appuntamento": "chiede_rimanda_appuntamento",
    "rimanda appuntamento": "chiede_rimanda_appuntamento",
    "chiede appuntamento": "chiede_rimanda_appuntamento",
    "dettagli su modalità di pagamento": "dettagli_modalita_pagamento",
    "cliente assente": "cliente_assente",
    "reale interlocutore": "reale_interlocutore",
    "stato attività impresa": "stato_attivita_impresa",
    "difficoltà economiche": "difficolta_economiche",
    "salute": "salute",
    "accordi presenti": "accordi_presenti",
    "procedimento legale": "procedimento_legale",
    "debito già pagato": "debito_gia_pagato",
    "pagamento non effettuato": "pagamento_non_effettuato",
    "proposta agevolazione": "proposta_agevolazione",
    "ha qualcuno che lo può aiutare": "ha_qualcuno_che_puo_aiutare",
    "ha fonti di reddito": "ha_fonti_reddito",
    "garanzie": "garanzie",
    "modulistica": "modulistica",
}
extraction = {
    #  entità operatore

    
    #  entità debitore
    "data pagamento": "data_pagamento",
    "importo sostenibile": "importo_sostenibile",
    "prospettiva temporale": "prospettiva_temporale"
}


highlited_only_mode = True #  se True, invece che creare un annotazione dell'intero documento, crea un annotazione del segmento di testo commentato


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
        # print(txt)
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


def create_ann_file(docfile: str, comments_dicts: list):
    """
    Highlited only mode: for every comment in the current file, create an ann file with the annotation for the text highlighted by the comment. This works better for autoML
    Non Highlited only mode: create a single ann file for the current file with all the annotations for all the comments
    """
    if highlited_only_mode:
        for idx, c in enumerate(comments_dicts):
            if c['comment'].lower() in taxonomy:
                with open(tax_ann_folder+"/"+docfile.split('.')[0]+"_"+str(idx)+".ann", 'a', encoding="utf-8") as ann:
                    tax_count = 1
                    # print("TAX: ", c["text"])
                    ann.write(f"C{tax_count}		{taxonomy[c['comment'].lower()]}\n")
                    ann.close()


            if c['comment'].lower() in extraction:
                with open(xtr_ann_folder+"/"+docfile.split('.')[0]+"_"+str(idx)+".ann", 'a', encoding="utf-8") as ann:
                    xtr_count = 1
                    if c["start"] == -1:
                        # raise Exception(f"'{c['text']}' not found in text ({docfile.split('.')[0]})")
                        pass
                    else:
                        # print("XTR: ", c["text"])
                        ann.write(f"T{xtr_count}		{extraction[c['comment'].lower()]} {c['start']} {c['end']}	{c['text']}\n")
                    ann.close()

    else:
        if c['comment'].lower() in taxonomy:
            with open(tax_ann_folder+"/"+docfile.split('.')[0]+".ann", 'a', encoding="utf-8") as ann:
                tax_count = 1
                for c in comments_dicts:
                    ann.write(f"C{tax_count}		{taxonomy[c['comment'].lower()]}\n")
                    tax_count +=1
                ann.close()

        if c['comment'].lower() in extraction:
            with open(xtr_ann_folder+"/"+docfile.split('.')[0]+".ann", 'a', encoding="utf-8") as ann:
                xtr_count = 1
                for c in comments_dicts:
                    if c["start"] == -1:
                        # raise Exception(f"'{c['text']}' not found in text ({docfile.split('.')[0]})")
                        pass
                    else:
                        ann.write(f"T{xtr_count}		{extraction[c['comment'].lower()]} {c['start']} {c['end']}	{c['text']}\n")
                        xtr_count +=1
                ann.close()
    print(f"Found {len(comments_dicts)} annotations")


def create_test_file(path: str, docfile: str, comments_dicts: list):
    """
    Highlited only mode: for every comment in the current file, create a txt file with the text highlighted by the comment. This works better for autoML
    Non Highlited only mode: create a single txt file for the current file and places it both in tax folder and xtr folder
    """
    if highlited_only_mode:
        for idx, c in enumerate(comments_dicts):
            if c['comment'].lower() in taxonomy:
                with open(tax_test_folder+"/"+docfile.split('.')[0]+"_"+str(idx)+".txt", 'w', encoding="utf-8") as file:
                    # print(txt)
                    file.write(c['text'])
                    file.close()
            
            if c['comment'].lower() in extraction:
                if c["start"] == -1:
                    # raise Exception(f"'{c['text']}' not found in text ({docfile.split('.')[0]})")
                    pass
                else:
                    with open(xtr_test_folder+"/"+docfile.split('.')[0]+"_"+str(idx)+".txt", 'w', encoding="utf-8") as file:
                        # print(txt)
                        file.write(c['text'])
                        file.close()
    else:
        txt = getTextFromDoc(path+"\\"+docfile)
        txt = normalize_fucked_encoding(txt)
        txt = re.sub(' +', ' ', txt)
        txt = re.sub('(S\d+)', r'\n\1', txt) # newline ogni enunciato
        with open(tax_test_folder+"/"+docfile.split('.')[0]+".txt", 'w', encoding="utf-8") as file:
            # print(txt)
            file.write(txt)
            file.close()
        with open(xtr_test_folder+"/"+docfile.split('.')[0]+".txt", 'w', encoding="utf-8") as file:
            # print(txt)
            file.write(txt)
            file.close()



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
    timenow = datetime.now().strftime('%d_%m_%y_%H_%M')
    tax_folder = f"runs/run_{timenow}/tax"
    xtr_folder = f"runs/run_{timenow}/xtr"
    tax_test_folder = f"runs/run_{timenow}/tax/test"
    tax_ann_folder = f"runs/run_{timenow}/tax/ann"
    xtr_test_folder = f"runs/run_{timenow}/xtr/test"
    xtr_ann_folder = f"runs/run_{timenow}/xtr/ann"
    os.makedirs("runs", exist_ok=True)
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
                if file_comments_dicts != False:
                    print(root, f)
                    create_test_file(root, f, file_comments_dicts)
                    create_ann_file(f, file_comments_dicts)
    create_zip()
