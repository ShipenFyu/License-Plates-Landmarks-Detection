import os
import cv2
import re
from tqdm import tqdm


def extract_coordinates(filename):
    parts = filename.split('-')
    part3 = parts[2]
    part4 = parts[3]

    coords_part3 = list(map(int, re.findall(r'\d+', part3)))
    coords_part4 = list(map(int, re.findall(r'\d+', part4)))

    return coords_part3, coords_part4


def crop_image(image_path, filename):
    img = cv2.imread(image_path)
    if img is None:
        print("Failed to load image")
        return None, None

    height, width = img.shape[:2]

    target_size = 640

    coords_part3, coords_part4 = extract_coordinates(filename)
    all_coords = coords_part3 + coords_part4

    min_x = min(all_coords[::2])
    max_x = max(all_coords[::2])
    min_y = min(all_coords[1::2])
    max_y = max(all_coords[1::2])

    left = (width - target_size) // 2
    right = left + target_size
    top = (height - target_size) // 2
    bottom = top + target_size

    if min_x <= left or max_x >= right or min_y <= top or max_y >= bottom:
        print("\nCoordinates are out of the image boundaries.")
        return None, None

    if right - left < target_size or bottom - top < target_size:
        print("\nUnable to crop the image without excluding some coordinates.")
        return None, None

    cropped_img = img[top:bottom, left:right]
    names = [all_coords[0] - left, all_coords[1] - top, all_coords[2] - all_coords[0], all_coords[3] - all_coords[1],
             all_coords[8] - left, all_coords[9] - top, 0.0, all_coords[10] - left, all_coords[11] - top, 0.0,
             all_coords[4] - left, all_coords[5] - top, 0.0, all_coords[6] - left, all_coords[7] - top, 0.0]

    return cropped_img, names


if __name__ == '__main__':
    images_path = './CCPD2019/ccpd_base'
    images_names = os.listdir(images_path)

    index = 0
    for index in tqdm(range(10000)):
        img_cropped, name_list = crop_image(os.path.join(images_path, images_names[index]), images_names[index])

        if img_cropped is not None:
            new_filename = '-'.join(map(str, name_list)) + '.jpg'
            cv2.imwrite('./CCPD2019/dataset/{}'.format(new_filename), img_cropped)
        else:
            print("Image could not be cropped.")
    print('Finished!')
