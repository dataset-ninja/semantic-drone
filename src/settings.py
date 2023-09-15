from typing import Dict, List, Optional, Union

from dataset_tools.templates import (
    AnnotationType,
    Category,
    CVTask,
    Domain,
    Industry,
    License,
    Research,
)

##################################
# * Before uploading to instance #
##################################
PROJECT_NAME: str = "Semantic Drone"
PROJECT_NAME_FULL: str = "Semantic Drone Dataset v1.1"
HIDE_DATASET = True  # set False when 100% sure about repo quality

##################################
# * After uploading to instance ##
##################################
LICENSE: License = License.Custom(url="http://dronedataset.icg.tugraz.at/", redistributable=False)
APPLICATIONS: List[Union[Industry, Domain, Research]] = [Domain.DroneInspection()]
CATEGORY: Category = Category.Aerial(extra=Category.Drones())

CV_TASKS: List[CVTask] = [CVTask.SemanticSegmentation()]
ANNOTATION_TYPES: List[AnnotationType] = [AnnotationType.SemanticSegmentation()]

RELEASE_DATE: Optional[str] = "2019-01-25"  # e.g. "YYYY-MM-DD"
if RELEASE_DATE is None:
    RELEASE_YEAR: int = None

HOMEPAGE_URL: str = "https://www.tugraz.at/index.php?id=22387"
# e.g. "https://some.com/dataset/homepage"

PREVIEW_IMAGE_ID: int = 4179421
# This should be filled AFTER uploading images to instance, just ID of any image.

GITHUB_URL: str = "https://github.com/dataset-ninja/semantic-drone"
# URL to GitHub repo on dataset ninja (e.g. "https://github.com/dataset-ninja/some-dataset")

##################################
### * Optional after uploading ###
##################################
DOWNLOAD_ORIGINAL_URL: Optional[
    Union[str, dict]
] = "https://docs.google.com/forms/d/e/1FAIpQLSfhqqdqoB-2c3S8FVq5YsToTExF-EQ4KFeUrYvEuylGSDX0kA/viewform"
# Optional link for downloading original dataset (e.g. "https://some.com/dataset/download")

CLASS2COLOR: Optional[Dict[str, List[str]]] = {
    "unlabeled": [0, 0, 0],
    "paved-area": [128, 64, 128],
    "dirt": [130, 76, 0],
    "grass": [0, 102, 0],
    "gravel": [112, 103, 87],
    "water": [28, 42, 168],
    "rocks": [48, 41, 30],
    "pool": [0, 50, 89],
    "vegetation": [107, 142, 35],
    "roof": [70, 70, 70],
    "wall": [102, 102, 156],
    "window": [254, 228, 12],
    "door": [254, 148, 12],
    "fence": [190, 153, 153],
    "fence-pole": [153, 153, 153],
    "person": [255, 22, 96],
    "dog": [102, 51, 0],
    "car": [9, 143, 150],
    "bicycle": [119, 11, 32],
    "tree": [51, 51, 0],
    "bald-tree": [190, 250, 190],
    "ar-marker": [112, 150, 146],
    "obstacle": [2, 135, 115],
    "conflicting": [255, 0, 0],
}
# If specific colors for classes are needed, fill this dict (e.g. {"class1": [255, 0, 0], "class2": [0, 255, 0]})

# If you have more than the one paper, put the most relatable link as the first element of the list
PAPER: Optional[Union[str, List[str]]] = None
BLOGPOST: Optional[Union[str, List[str]]] = None

CITATION_URL: Optional[str] = "http://dronedataset.icg.tugraz.at/"
AUTHORS: Optional[List[str]] = [
    "Christian Mostegel",
    "Michael Maurer",
    "Nikolaus Heran",
    "Jesus Pestana Puerta",
    "Friedrich Fraundorfer",
]

ORGANIZATION_NAME: Optional[
    Union[str, List[str]]
] = "Institute of Computer Graphics and Vision (ICG), Graz University of Technology, Austria"
ORGANIZATION_URL: Optional[Union[str, List[str]]] = "https://www.tugraz.at/institute/icg/home"

# Set '__PRETEXT__' or '__POSTTEXT__' as a key with value:str to add custom text. e.g. SLYTAGSPLIT = {'__POSTTEXT__':'some text}
SLYTAGSPLIT: Optional[Dict[str, Union[List[str], str]]] = None
TAGS: Optional[List[str]] = None


SECTION_EXPLORE_CUSTOM_DATASETS: Optional[List[str]] = None

##################################
###### ? Checks. Do not edit #####
##################################


def check_names():
    fields_before_upload = [PROJECT_NAME]  # PROJECT_NAME_FULL
    if any([field is None for field in fields_before_upload]):
        raise ValueError("Please fill all fields in settings.py before uploading to instance.")


def get_settings():
    if RELEASE_DATE is not None:
        global RELEASE_YEAR
        RELEASE_YEAR = int(RELEASE_DATE.split("-")[0])

    settings = {
        "project_name": PROJECT_NAME,
        "project_name_full": PROJECT_NAME_FULL or PROJECT_NAME,
        "hide_dataset": HIDE_DATASET,
        "license": LICENSE,
        "applications": APPLICATIONS,
        "category": CATEGORY,
        "cv_tasks": CV_TASKS,
        "annotation_types": ANNOTATION_TYPES,
        "release_year": RELEASE_YEAR,
        "homepage_url": HOMEPAGE_URL,
        "preview_image_id": PREVIEW_IMAGE_ID,
        "github_url": GITHUB_URL,
    }

    if any([field is None for field in settings.values()]):
        raise ValueError("Please fill all fields in settings.py after uploading to instance.")

    settings["release_date"] = RELEASE_DATE
    settings["download_original_url"] = DOWNLOAD_ORIGINAL_URL
    settings["class2color"] = CLASS2COLOR
    settings["paper"] = PAPER
    settings["blog"] = BLOGPOST
    settings["citation_url"] = CITATION_URL
    settings["authors"] = AUTHORS
    settings["organization_name"] = ORGANIZATION_NAME
    settings["organization_url"] = ORGANIZATION_URL
    settings["slytagsplit"] = SLYTAGSPLIT
    settings["tags"] = TAGS

    settings["explore_datasets"] = SECTION_EXPLORE_CUSTOM_DATASETS

    return settings
