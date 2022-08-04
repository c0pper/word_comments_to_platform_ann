from pathlib import Path

july_date_in_epoch = 1657497600
p = Path('C:\\Users\\smarotta\\PycharmProjects\\mirco_annotazioni_server_1maggio\\Banking_-_Performing')
# p = Path('C:\\Users\\smarotta\\PycharmProjects\\word_comments_to_platform_ann\\input_docs_debug')
l = list(p.glob('**/*.docx'))
# print(l)
print([x.name for x in list(p.glob('**/*.docx')) if x.stat().st_mtime > july_date_in_epoch])