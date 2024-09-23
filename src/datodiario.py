import requests
from pathlib import Path


def fetch_daily_data(url: str, save_path: Path) -> bool:
    """Download a file from the given URL and save it to the specified path.

    Args:
        url (str): Download URL.
        save_path (Path): Path where the file will be saved.
        progress_callback (function, optional): A callback function to report download progress.

    Raises:
        FileNotFoundError: if the path of the file to be saved does not exist.

    Returns:
        bool: Returns true if you were able to download the file or false if not.
    """

    response = requests.get(url, stream=True)

    save_path.parent.mkdir(parents=True, exist_ok=True)

    if response.status_code == 200 and "no existe" not in str(response.content):
        try:
            with open(save_path, "wb") as file:
                file.write(response.content)
        except FileNotFoundError:
            print("El path del archivo a salvar no existe")
            return False
    else:
        return False
    return True
