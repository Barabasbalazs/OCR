import math

# this needs to be as low as possible if accurate
def euclidean_diff(x, y):
    difference = 0
    for i in range(len(x)):
        difference += (x[i] - y[i]) ** 2
    return difference

# this needs to be closer to 1
def cos_distance(x, y):
    x_dot_y = 0
    x_length = 0
    y_length = 0
    for i in range(len(x)):
        x_dot_y += x[i] * y[i]
        x_length += x[i] ** 2
        y_length += y[i] ** 2
    cos_x_and_y = x_dot_y / (math.sqrt(x_length) * math.sqrt(y_length))
    return cos_x_and_y

def get_most_common(list):
    indexes = [0] * 10
    for i in list:
        indexes[i[0]] += 1
    return indexes.index(max(indexes))

def sort_data(test_data):
    sorted_arr = [0] * 10
    
    for i in range(10):
        sorted_arr[i] = []

    for image in test_data:
        index = image[64]
        sorted_arr[index].append(image)
    
    tmp_arr = []

    for i in range(10):
        for curr_im in sorted_arr[i]:
            tmp_arr.append(curr_im)

    return tmp_arr