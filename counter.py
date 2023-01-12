from pathlib import Path
from platform_utils_eai.functions import create_folder_structure
from main import return_comments_dicts
from tqdm import tqdm
from entities import operatore_entities, debitore_entities
import matplotlib.pyplot as plt
import numpy as np

# word_files_path = Path(f"{input('input the path where the docx files are: ')}")
#
# op = 0
# deb = 0
# if not word_files_path.exists():
#     raise Exception(f"Path {word_files_path} doesn't exist")
# else:
#     folders = create_folder_structure(str(word_files_path))
#     docs_tot = len(word_files_path.glob("*.docx"))
#
#     for f in tqdm(word_files_path.glob("*.docx")):
#         # print("---------\n" + "WORKING ON: ", f.name)
#         if "_annotato" in f.name:
#             file_comments_dicts = return_comments_dicts(f)
#             if file_comments_dicts:  # if comments where found
#                 for d in file_comments_dicts:
#                     ann = d['comment'].lower()
#                     if ann in debitore_entities.keys():
#                         deb += 1
#                         # print(deb)
#                     elif ann in operatore_entities.keys():
#                         op += 1
#                         # print(op)
# op_train = int(op*80/100)
# op_val = op - op_train
# deb_train = int(deb*80/100)
# deb_val = deb - deb_train
# print(op, op_train, op_val, deb, deb_train, deb_val)

#  annotazioni totali
#  deb = 3726 train: 2979 test: 759
#  op =  14794 - train: 11808 test: 2974

op_tot = 14794
op_train = 11835
op_val = 2959
deb_tot = 3726
deb_train = 2980
deb_val = 746

docs_tot = 4772

D = {
    "op tot ent": op_tot,
    "op train ent": op_train,
    "op val ent": op_val,
    "deb tot ent": deb_tot,
    "deb train ent": deb_train,
    "deb val ent": deb_val
}
labels = ['op', 'deb']
tot = [op_tot, deb_tot]
train = [op_train, deb_train]
val = [op_val, deb_val]
x = np.arange(len(labels))  # the label locations
width = 0.3

# plot data in grouped manner of bar type
plt.bar(x - width, tot, width, color='blue')
plt.bar(x, train, width, color='orange')
plt.bar(x + width, val, width, color='green')
plt.xticks(x, labels)
plt.ylabel("N of annotations")
plt.legend(["total", "train set", "val set"])
plt.savefig("class_distribution")
plt.show()

# names = ['tot ent op', 'tot ent deb']
# values = [14794, 3726]
#
# plt.figure(figsize=(9, 9))
#
# plt.bar(names, values)
# plt.savefig("class_distribution")