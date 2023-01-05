"""
    entities.py
    -----------

    This module contains dictionaries for taxonomy and extraction entites where key is the text found in the word
    comments and value is the name of the entity in the linguistic project. Provides a mapping to be used by
    :func:`main.create_annotation_and_text_file`
"""

taxonomy = {
    #  operatore
    "rispetto script": "rispetto_script",
    "presentazione società": "presentazione_societa",
    "presentazione prodotto": "presentazione_prodotto",
    "dettaglio esposizione": "dettaglio_esposizione",
    "interlocutore alternativo": "interlocutore_alternativo",
    "recapiti alternativi": "recapiti_alternativi",
    "stato attività impresa": "stato_attivita_impresa",
    "scadenza pagamento": "scadenza_pagamento",
    "volontà risolutiva": "volonta_risolutiva",
    "pagamento acconto": "pagamento_acconto",
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
    "vantaggio": "vantaggio",
    "conferma accordi": "conferma_accordi",
    "estremi di pagamento": "estremi_di_pagamento",
    "richiesto riscontro di pagamento": "richiesto_riscontro_di_pagamento",
    "invio modulistica": "invio_modulistica",
    "richiesta documenti": "richiesta_documenti",
    "invito a confronto diretto": "invito_a_confronto_diretto",

    #  debitore
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
    "data pagamento": "data_pagamento",
    "dettagli su modalità di pagamento": "dettagli_modalita_pagamento",
    "cliente assente": "cliente_assente",
    "reale interlocutore": "reale_interlocutore",
    "difficoltà economiche": "difficolta_economiche",
    "salute": "salute",
    "accordi presenti": "accordi_presenti",
    "procedimento legale": "procedimento_legale",
    "debito già pagato": "debito_gia_pagato",
    "pagamento non effettuato": "pagamento_non_effettuato",
    "proposta agevolazione": "proposta_agevolazione",
    "ha qualcuno che lo può aiutare": "ha_qualcuno_che_puo_aiutare",
    "ha fonti di reddito": "ha_fonti_reddito",
    "importo sostenibile": "importo_sostenibile",
    "prospettiva temporale": "prospettiva_temporale",
    "garanzie": "garanzie",
    "modulistica": "modulistica"
    # "stato attività impresa": "stato_attivita_impresa"
}

extraction = {
}
