import cv2
import numpy as np
# from matplotlib import pyplot as plt
import os
import logging

def extract_peek(array_vals, min_vals=10, min_rect=5):
    extract_points = []
    start_point = None
    end_point = None
    for i, point in enumerate(array_vals):
        if point > min_vals and start_point == None:
            start_point = i
        elif point < min_vals and start_point != None:
            end_point = i

        if start_point != None and end_point != None:
            extract_points.append((start_point, end_point))
            start_point = None
            end_point = None

    for point in extract_points:
        if point[1] - point[0] < min_rect:
            extract_points.remove(point)
    return extract_points

def find_borders(img):
    hori_vals = np.sum(img, axis=1)
    hori_points = extract_peek(hori_vals)
    rows = []
    
    for hori_point in hori_points:
        extract_img = img[hori_point[0]:hori_point[1], :]
        vec_vals = np.sum(extract_img, axis=0)
        vec_points = extract_peek(vec_vals, min_rect=0)
        borders = []
        for vect_point in vec_points:
            border = [(vect_point[0], hori_point[0]),(vect_point[1], hori_point[1])]
            borders.append(border)
        borders.sort(key=lambda x: x[0][0])
        if len(borders) == 10:
            rows.append(borders)
    
    rows.sort(key=lambda x: x[0][0][1])
    return rows

# Dilate kernal
kernel_size = (4, 4)
kernel = np.ones(kernel_size, np.uint8)

image_shape = (28, 28)

if __name__ == "__main__":
    folder_path = input("Image path:")

    logging.basicConfig(level=logging.INFO,format='%(asctime)s %(filename)s, line %(lineno)d %(levelname)s %(message)s',  \
        datefmt='%a, %d %b %Y %H:%M:%S')

    image_data = None
    labels = None

    for filename in os.listdir(folder_path):

        path = os.path.join(folder_path, filename)
        logging.info("Processing image: "+ path)

        img = cv2.imread(path)
        img = img[10:img.shape[0]-10, 10:img.shape[1]-10]
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        channels = cv2.split(img)
        key = channels[0]

        _, thresh = cv2.threshold(key, 50, 255, cv2.THRESH_BINARY_INV)
        binary = cv2.dilate(thresh, kernel, iterations=1)
        # cv2.imsave(os.path.join(os))

        rows = find_borders(binary)
        logging.info(f"Extracted {len(rows)} rows, {len(rows) * 10} samples")
        
        img_data = np.zeros((len(rows), 10, image_shape[0], image_shape[0], 1), dtype='uint8')
        for i, row in enumerate(rows):
            for j, border in enumerate(row):
                border_img = binary[border[0][1]:border[1][1], border[0][0]:border[1][0]]
                extend_piexl = (max(border_img.shape) - min(border_img.shape)) // 2
                target_img = cv2.copyMakeBorder(border_img, 7, 7, extend_piexl + 7, extend_piexl + 7, cv2.BORDER_CONSTANT)
                target_img = cv2.resize(target_img, image_shape)
                target_img = np.expand_dims(target_img, axis=-1)
                img_data[i, j] = target_img

        img_data = img_data.reshape((-1, 28, 28, 1))
        label_data = np.tile(np.array(range(10)), len(rows))

        if image_data is None:
            image_data = img_data
            labels = label_data
            continue

        image_data = np.concatenate((image_data, img_data), axis=0)
        labels = np.concatenate((labels, label_data), axis=0)

    shuffle_index = np.random.permutation(image_data.shape[0])
    image_data = image_data[shuffle_index]
    labels = labels[shuffle_index]

    np.save("image_data.npy", image_data)
    np.save("label_data.npy", labels)

