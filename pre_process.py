import cv2
import numpy as np
from matplotlib import pyplot as plt

def access_binary(img, roi=(0, 0, 0, 0), threshold=130, kernel_size=(2, 2)):
    # Crop
    x, y, w, h = roi
    if roi != (0, 0, 0, 0):
        img = img[y:y + h, x:x + w]

    # Grey
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    h = grey.shape[0]
    w = grey.shape[1]

    # Thresh
    _, thresh = cv2.threshold(grey, threshold, 255, cv2.THRESH_BINARY_INV)

    # Dilate
    kernel = np.ones(kernel_size, np.uint8)
    dilate = cv2.dilate(thresh, kernel, iterations=1)

    return dilate

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

def find_borders(img, length, min_size=0, max_size=float("inf")):
    # Extract the row
    hori_vals = np.sum(img, axis=1)
    hori_points = extract_peek(hori_vals)

    for hori_point in hori_points:
    # hori_point = hori_points[0]
        extract_img = img[hori_point[0]:hori_point[1], :]

        vec_vals = np.sum(extract_img, axis=0)
        vec_points = extract_peek(vec_vals, min_rect=5)
        borders = []

        size_of_border = lambda x: (x[1][1]-x[0][1]) * (x[1][0]-x[0][0])
        for vect_point in vec_points:
            border = [(vect_point[0], hori_point[0]), (vect_point[1], hori_point[1])]
            if size_of_border(border) >= min_size and size_of_border(border) <= max_size:
                borders.append(border)

        if len(borders) > length:
            borders.sort(key=size_of_border)
            borders = borders[:length]
        if len(borders) == length:
            return sorted(borders, key=lambda x: x[0][0])

def extract_numbers(bin, borders, size=(28, 28)):
    img_data = np.zeros((len(borders), size[0], size[0], 1), dtype='uint8')
    for i, border in enumerate(borders):
        border_img = bin[border[0][1]:border[1][1], border[0][0]:border[1][0]]
        extend_piexl = (max(border_img.shape) - min(border_img.shape)) // 2
        target_img = cv2.copyMakeBorder(border_img, 7, 7, extend_piexl + 7, extend_piexl + 7, cv2.BORDER_CONSTANT)
        target_img = cv2.resize(target_img, size)
        target_img = np.expand_dims(target_img, axis=-1)
        img_data[i] = target_img
    return img_data

def draw_border(img, borders):
    for i, border in enumerate(borders):
        cv2.rectangle(img, border[0], border[1], (0, 0, 255))
    return img

def process_image(image, length=5, min_size=0, max_size=float("inf"), roi=(0, 0, 0, 0)):
    binary = access_binary(image, roi=roi)
    borders = find_borders(binary, length=length, min_size=min_size, max_size=max_size)
    data = extract_numbers(binary, borders)
    return data

def trace_image(image, length=5, min_size=0, max_size=float("inf"), roi=(0, 0, 0, 0)):
    binary = access_binary(image, roi=roi)
    borders = find_borders(binary, length=length, min_size=min_size, max_size=max_size)
    with_boders = draw_border(image.copy(), borders)
    data = extract_numbers(binary, borders)
    return binary, with_boders, data

if __name__ == '__main__':
    length = 5

    # Open image
    path = input("Input path: ")
    image = cv2.imread(path)

    #
    binary, with_boders, data = trace_image(image)

    plt.subplot(2, 2, 1), plt.imshow(binary, "gray"), plt.title("Binary")
    plt.subplot(2, 2, 2), plt.imshow(with_boders, "gray"), plt.title("Borders")

    for i in range(length):
        plt.subplot(2, length, length + i + 1)
        plt.imshow(data[i]), plt.title("Number {}".format(i + 1))

    plt.show()
