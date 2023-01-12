"""
A differenza di Platform, intelliJ considera tutte le annotazioni nei file e non solo quelle riportate nella tassonomia.
Per questo è necessario dividere train_lib e val_lib in *_lib_debitore e *_lib_operatore. le librerie conterranno solo
i file annotati rispettivamente con entità assegnate a operatore o debitore, cosi da essere caricate nei relativi
progetti. Alla fine avremo 4 librerie, 2 per progetto: op_train_lib, op_val_lib, deb_train_lib, deb_val_lib.
"""
from pathlib import Path
from tqdm import tqdm
from entities import operatore_entities, debitore_entities
import shutil


def get_valid_dirs(root: str, categories: list):
    """

    :param root: root of the run folder
    :param categories: example - debitore_entities.values()
    :return: dizionario con percorsi alle categorie filtrate a seconad di deb o op per tax e xtr
    """
    run_path = Path(root)

    valid_dirs = {}

    for directory in run_path.glob("*"):
        print(f"\n\nWORKING IN {directory}\n")
        # ann_train = Path(directory / "ann_split" / "train").glob("**/*.ann")
        # test_train = Path(directory / "test_split" / "train").glob("**/*.txt")
        # ann_val = Path(directory / "ann_split" / "val").glob("**/*.ann")
        # test_val = Path(directory / "test_split" / "val").glob("**/*.txt")
        # print(directory.name, len(list(ann_train)), len(list(test_train)))
        # print(directory.name, len(list(ann_val)), len(list(test_val)))
        for i in ["ann_split", "test_split"]:
            print([i.name for i in list(Path(directory / i / "train").glob("*")) if i.name in categories])
            for split in ["train", "val"]:
                valid_dirs[f"{directory.name}_{i}_{split}"] = []
                for cat_dir in Path(directory / i / split).glob("*"):
                    cat_name = cat_dir.name
                    if cat_name not in categories:
                        pass
                    elif cat_name in categories:
                        print(cat_dir)
                        valid_dirs[f"{directory.name}_{i}_{split}"].append(cat_dir)
    return valid_dirs


def get_file_list(dirs: dict):
    """

    :param dirs: dictionary returned by :func:`get_valid_dirs`
    :return: dictionary containing list of files for tax_ann_split_train, tax_ann_split_val, tax_test_split_train, tax_test_split_val, xtr_ann_split_train, xtr_ann_split_val, xtr_test_split_train, xtr_test_split_val
    """
    files = {}
    for k, dir_list in dirs.items():
        files[k] = []
        if dir_list:
            for d in dir_list:
                files[k] = files[k] + list(d.glob("*"))
    return files


def copy_files(root: str, files: dict):
    """
    Copy files to the intellij_lib folder inside the run root folder

    :param root: root of the run folder
    :param files: dict returned by :func:`get_file_list`
    """
    root = Path(root)
    for k, list_of_files in files.items():
        for file in list_of_files:
            dest = Path(root / "intellij_lib" / k)
            dest.mkdir(exist_ok=True, parents=True)
            shutil.copy(file, dest)


if __name__ == "__main__":
    root = input("Enter run root path: ")
    deb_dirs = get_valid_dirs(root, debitore_entities.values())
    op_dirs = get_valid_dirs(root, operatore_entities.values())

    copy_files(root, get_file_list(deb_dirs))

