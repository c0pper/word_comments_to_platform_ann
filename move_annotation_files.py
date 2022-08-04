from itertools import count
from pathlib import Path
import shutil
from datetime import datetime
from tqdm import tqdm


# date_time_obj = None
# while not date_time_obj:
#     date_str = input("Input date in format DD-MM-YY: ")
#     try:
#         date_time_obj = datetime.strptime(date_str, '%d-%m-%y')
#     except ValueError:
#         print("Wrong format, try again.")
    


p = Path('C:\\Users\\smarotta\\Desktop\\trascrizioni_scaricate')

# trova file con data modifica posteriore a quella fornita nelle sottocartelle del path fornito e li copia nella cartella "files form after" a livello del file script
def get_files_from_date(path: Path, epoch: int):
    """Trova file con data modifica posteriore a quella fornita nelle sottocartelle del path fornito e li copia nella cartella "files form after" a livello del file script"""

    l = list(path.glob('**/*.docx'))
    
    script_path = Path(__file__).parent
    copied_path = script_path / f'files_from_after_{date_str}'
    copied_path.mkdir(mode=0o777, exist_ok=True)

    new_files = [x for x in l if x.stat().st_mtime > epoch]
    for f in tqdm(new_files):
        dest_path = copied_path / f.name
        if not dest_path.is_file(): # file doesn't exist
            print(f"Copying {f.name}")
            shutil.copyfile(f, dest_path)
        else:
            print(f"\n{f.name} exists already")


def move_annotation_files(path: Path, destination_path: Path):
    """ Find in the tree and move all annotated files to single destination folder"""
    destination_path.mkdir(exist_ok=True)
    l = list(path.glob('**/*annotato.docx'))
    errors = 0
    for f in tqdm(l):
        dest_path = destination_path / f.name
        try:
            if not dest_path.is_file(): # file doesn't exist
                print(f"Moving {f.name}")
                shutil.move(f, dest_path)
        except FileNotFoundError:
            errors +=1
    print("Completed with", errors, "errors")

# move_annotation_files(Path('C:\\Users\\smarotta\\Desktop\\trascrizioni_scaricate'), Path('C:\\Users\\smarotta\\Desktop\\trasc_ann'))
# get_files_from_date(p, date_time_obj.timestamp())
