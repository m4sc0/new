import requests
from pathlib import Path
from zipfile import ZipFile
from io import BytesIO
from image import TemplateImage, get_local_image_path
from template_metadata import TemplateMetadata
from getpass import getpass
from typing import List
from config import config

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

def list_remote_templates(remote_url: str) -> List[TemplateImage]:
    url = f"{remote_url}/list"
    response = requests.get(url)
    response.raise_for_status()

    result = response.json()['result']

    templates = []

    for _id, entry in result.items():
        template = TemplateImage(
                category=entry['category'],
                name=entry['name'],
                version=entry['version']
            )
        templates.append(template)

    return templates
def zip_template_folder(folder: Path) -> BytesIO:
    buffer = BytesIO()
    with ZipFile(buffer, "w") as zipf:
        for path in folder.rglob("*"):
            arcname = path.relative_to(folder)
            zipf.write(path, arcname)
    buffer.seek(0)
    return buffer

def upload_template(remote_url: str, image: TemplateImage, verbose: bool = False):
    path = get_local_image_path(image)

    if not path.exists():
        raise FileNotFoundError(f"Template not found in local cache: {path}")

    metadata_path = path / "template.json"
    if not metadata_path.exists():
        raise FileNotFoundError(f"Missing template.json in: {path}")

    metadata = TemplateMetadata.load(metadata_path)

    zip_bytes = zip_template_folder(path)

    token_valid, token_config = config.get_upload_token()

    if not token_valid:
        token = getpass("Upload token: ")
    else:
        token = token_config

    if verbose:
        print(f"Uploading {image} to {remote_url}...")

    response = requests.post(
        f"{remote_url}/upload",
        headers={"Authorization": f"Bearer {token}"},
        files={"file": ("template.zip", zip_bytes.getvalue(), "application/zip")},
        data={
            "category": image.category,
            "name": image.name,
            "version": image.version,
            "description": metadata.description or "No description"
        }
    )

    if response.status_code == 200:
        print(f"Upload successful: {image}")
    else:
        raise Exception(f"Upload failed: {response.status_code} - {response.text}")

