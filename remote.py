import requests
from pathlib import Path
from zipfile import ZipFile
from io import BytesIO
from image import TemplateImage, get_local_image_path
from template_metadata import TemplateMetadata

def fetch_metadata(remote_url: str, image: TemplateImage) -> TemplateMetadata:
    url = f"{remote_url}/meta/{image.category}/{image.name}/{image.version}"
    response = requests.get(url)
    response.raise_for_status()
    return TemplateMetadata(**response.json())

def pull_template(remote_url: str, image: TemplateImage, verbose: bool = False) -> Path:
    url = f"{remote_url}/get/{image.category}/{image.name}/{image.version}"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Template '{image}' not found at remote: {remote_url}")

    target_path = get_local_image_path(image)
    if verbose:
        print(f"Extracting to {target_path}")

    with ZipFile(BytesIO(response.content)) as zipf:
        zipf.extractall(target_path)

    return target_path
