# https://www.tugraz.at/index.php?id=22387

import csv
import os
import shutil
from urllib.parse import unquote, urlparse

import numpy as np
import supervisely as sly
from cv2 import connectedComponents
from dataset_tools.convert import unpack_if_archive
from dotenv import load_dotenv
from PIL import Image
from supervisely.io.fs import (
    dir_exists,
    file_exists,
    get_file_ext,
    get_file_name,
    get_file_name_with_ext,
    get_file_size,
)
from tqdm import tqdm

import src.settings as s


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    # project_name = "semantic_drone_dataset"
    dataset_path = (
        "/mnt/d/datasetninja-raw/semantic drone dataset/semantic_drone_dataset/training_set"
    )
    images_folder = "images"
    masks_folder = "gt/semantic/label_images"
    masks_values_data_file = "gt/semantic/class_dict.csv"
    images_ext = ".jpg"
    masks_ext = ".png"
    ds_name = "ds"
    batch_size = 1

    def get_unique_colors(img):
        unique_colors = []
        img = img.astype(np.int32)
        h, w = img.shape[:2]
        colhash = img[:, :, 0] * 256 * 256 + img[:, :, 1] * 256 + img[:, :, 2]
        unq, unq_inv, unq_cnt = np.unique(colhash, return_inverse=True, return_counts=True)
        indxs = np.split(np.argsort(unq_inv), np.cumsum(unq_cnt[:-1]))
        col2indx = {unq[i]: indxs[i][0] for i in range(len(unq))}
        for col, indx in col2indx.items():
            if col != 0:
                unique_colors.append((col // (256**2), (col // 256) % 256, col % 256))

        return unique_colors

    def create_ann(image_path):
        labels = []

        mask_path = os.path.join(masks_path, get_file_name(image_path) + masks_ext)
        if file_exists(mask_path):
            mask_np = sly.imaging.image.read(mask_path)
            img_height = mask_np.shape[0]
            img_wight = mask_np.shape[1]
            unique_colors = get_unique_colors(mask_np)
            for color in unique_colors:
                mask = np.all(mask_np == color, axis=2)
                ret, curr_mask = connectedComponents(mask.astype("uint8"), connectivity=8)
                for i in range(1, ret):
                    obj_mask = curr_mask == i
                    bitmap = sly.Bitmap(data=obj_mask)
                    if bitmap.area > 50:
                        obj_class = color_to_obj_class[color]
                        label = sly.Label(bitmap, obj_class)
                        labels.append(label)

        return sly.Annotation(img_size=(img_height, img_wight), labels=labels)

    color_to_obj_class = {}
    masks_values_data_path = os.path.join(dataset_path, masks_values_data_file)
    with open(masks_values_data_path, "r") as file:
        csvreader = csv.reader(file)
        for idx, row in enumerate(csvreader):
            if idx != 0:
                color = tuple(map(int, row[1:]))
                color_to_obj_class[color] = sly.ObjClass(row[0], sly.Bitmap)

    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)

    meta = sly.ProjectMeta(obj_classes=list(color_to_obj_class.values()))
    api.project.update_meta(project.id, meta.to_json())

    images_path = os.path.join(dataset_path, images_folder)
    masks_path = os.path.join(dataset_path, masks_folder)

    dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)

    images_names = [im_name for im_name in os.listdir(images_path)]

    progress = sly.Progress("Create dataset {}".format(ds_name), len(images_names))

    for images_names_batch in sly.batched(images_names, batch_size=batch_size):
        images_pathes_batch = [os.path.join(images_path, im_name) for im_name in images_names_batch]

        img_infos = api.image.upload_paths(dataset.id, images_names_batch, images_pathes_batch)
        img_ids = [im_info.id for im_info in img_infos]

        anns = [create_ann(image_path) for image_path in images_pathes_batch]
        api.annotation.upload_anns(img_ids, anns)

        progress.iters_done_report(len(images_names_batch))

    return project
