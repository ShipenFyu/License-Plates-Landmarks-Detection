import os
import json
import shutil
from tqdm import tqdm


def label_ccpd():
    dataset_folder = './data/widerface/train/images'
    label_path = './data/widerface/train/label.txt'

    image_files = os.listdir(dataset_folder)

    with open(label_path, 'w') as f:
        for image_file in tqdm(image_files):
            f.write('# ' + image_file + '\n')

            pixel_coordinates = os.path.splitext(image_file)[0].split('-')
            pixel_coordinates = ' '.join(pixel_coordinates)
            f.write(pixel_coordinates + '\n')
        print('Finished!')


def label_yellow():
    dataset_folder = './yellow/imgs'
    label_path = './yellow/det_train.txt'
    save_data_folder = './data/widerface/train/images'
    save_label_path = './data/widerface/train/label.txt'

    result_dict = {}

    with open(label_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for line in lines:
        parts = line.strip().split('\t')
        file_path = parts[0].split('/')[-1]
        json_data = json.loads(parts[1])
        points = json_data[0]['points']

        points_list = [coord for point in points for coord in point]

        result_dict[file_path] = points_list

    with open(save_label_path, 'w') as f:
        for image_file, points in tqdm(result_dict.items()):
            origin_path = os.path.join(dataset_folder, image_file)
            target_path = os.path.join(save_data_folder, image_file)
            shutil.copy(origin_path, target_path)

            f.write('# ' + image_file + '\n')

            pixel_coordinates = ['0'] * 16
            pixel_coordinates[0] = str(points[2])
            pixel_coordinates[1] = str(points[3])
            pixel_coordinates[2] = str(points[6] - points[2])
            pixel_coordinates[3] = str(points[7] - points[3])
            pixel_coordinates[4] = str(points[2])
            pixel_coordinates[5] = str(points[3])
            pixel_coordinates[6] = str(0.0)
            pixel_coordinates[7] = str(points[4])
            pixel_coordinates[8] = str(points[5])
            pixel_coordinates[9] = str(0.0)
            pixel_coordinates[10] = str(points[6])
            pixel_coordinates[11] = str(points[7])
            pixel_coordinates[12] = str(0.0)
            pixel_coordinates[13] = str(points[0])
            pixel_coordinates[14] = str(points[1])
            pixel_coordinates[15] = str(0.0)

            pixel_coordinates = ' '.join(pixel_coordinates)
            f.write(pixel_coordinates + '\n')
        print('Finished!')


if __name__ == '__main__':
    # label_ccpd()
    label_yellow()
