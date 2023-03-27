import math

# this needs to be as low as possible
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


def read_input(name_of_file):
    file = open(name_of_file, "r")
    arr = []
    for line in file:
        line_array = line.split(",")
        arr.append([int(element) for element in line_array])
    file.close()
    return arr

if __name__ == "__main__":
    training_data = read_input("optdigits.tra")
    test_data = read_input("optdigits.tes")