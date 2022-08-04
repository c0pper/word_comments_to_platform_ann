from pathlib import Path
import shutil
from datetime import datetime
from tqdm import tqdm

july_date_in_epoch = 1657497600
date_str =datetime.fromtimestamp(july_date_in_epoch).strftime("%d-%m-%y")
# p = Path('C:\\Users\\smarotta\\PycharmProjects\\mirco_annotazioni_server_1maggio\\Banking_-_Performing')
p = Path('C:\\Users\\smarotta\\PycharmProjects\\word_comments_to_platform_ann\\input_docs_debug')

# trova file con data modifica posteriore a quella fornita nelle sottocartelle del path fornito e li copia nella cartella "files form after" a livello del file script
def get_files_from_date(path: Path, epoch: int):
    """Trova file con data modifica posteriore a quella fornita nelle sottocartelle del path fornito e li copia nella cartella "files form after" a livello del file script"""

    l = list(path.glob('**/*.docx'))
    date_str =datetime.fromtimestamp(july_date_in_epoch).strftime("%d-%m-%y")

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

get_files_from_date(p, july_date_in_epoch)
