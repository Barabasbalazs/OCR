import math
import matplotlib.pyplot as plt
import numpy as np

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

#for calculating accuracy of each number
def get_results(images):
    model = [0] * 10 
    for line in images:
        model[line[64]] += 1
    return model


def knn(training_data, test_data, mode, k):
    # for storing the model accuracies
    model = [0] * 10 
    
    # learning error
    error_counter = 0
    for image in training_data:
        limit = (-1, 100000) if mode == "euclidean" else (-1,-2) 
        # first one is the number second is the similarity
        top_k = []
        counter = 0
        for test_image in test_data:
            if mode == "euclidean":
                diff = euclidean_diff(image[0: 64], test_image[0: 64])
                if diff <= limit[1]:
                    if counter >= k:
                        if k == 1:
                            top_k[0] = (test_image[64],diff)
                        else:
                            top_k.remove(limit)
                            top_k.append((test_image[64],diff))
                        limit = max(top_k, key = lambda x : x[1])
                    else:
                        counter += 1
                        limit = (test_image[64],diff)
                        top_k.append(limit)
            else :
                diff = cos_distance(image[0: 64], test_image[0: 64])
                if diff >= limit[1]:
                    if counter >= k:
                        if k == 1:
                            top_k[0] = (test_image[64],diff)
                        else:
                            top_k.remove(limit)
                            top_k.append((test_image[64],diff))
                        limit = min(top_k, key = lambda x : x[1])
                    else:
                        counter += 1
                        limit = (test_image[64],diff)
                        top_k.append(limit)
        result = get_most_common(top_k)
        # print(top_k)
        # print("result is {} and actually its {}".format(result, image[64]))
        if result == image[64]:
            error_counter += 1
            model[result] += 1

    return error_counter / len(training_data), model

        

def get_most_common(list):
    indexes = [0] * 10
    for i in list:
        indexes[i[0]] += 1
    return indexes.index(max(indexes))


def centroid(training_data, comparison_data):
    # model_arrays = [[0] * 64] * 10
    rows, cols = (10, 64)
    model_arrays = [[0 for i in range(cols)] for j in range(rows)]
    for training_image in training_data:
        current_number = training_image[64]
        for i in range(64):
            coordinate = training_image[i]
            # adds the same number to all of the indexes
            model_arrays[current_number][i] += coordinate
    for i in range(10):
        for j in range(64):
            model_arrays[i][j] /= comparison_data[i]
    return model_arrays


def write_results(training_error, training_numbers, training_euclidean, training_cos, 
                  test_error, test_numbers, test_euclidean, test_cos, k):
    file = open("output.txt","w")

    file.write("K is = {}\n".format(k))

    file.write("Training error on euclidean: {}\n".format(training_error[0]))
    file.write("Training error on models using euclidean\n")
    for i in range(10):
        file.write("{} - {}\n".format(i, training_euclidean[i] / training_numbers[i]))
    file.write("Training error on cos: {}\n".format(training_error[1]))
    file.write("Training error on models using cos\n")
    for i in range(10):
        file.write("{} - {}\n".format(i, training_cos[i] / training_numbers[i]))


    file.write("Test error on euclidean: {}\n".format(test_error[0]))
    file.write("Test error on models using euclidean\n")
    for i in range(10):
        file.write("{} - {}\n".format(i, test_euclidean[i] / test_numbers[i]))
    file.write("Training error on cos: {}\n".format(test_error[1]))
    file.write("Test error on models using cos\n")
    for i in range(10):
        file.write("{} - {}\n".format(i, test_cos[i] / test_numbers[i]))
    
    file.close()            


def visualize_number(data_of_image):
    number_matrix = []
    it = 0
    for i in range(8):
        number_matrix.append([])
        for j in range(8):
            number_matrix[i].append(data_of_image[it])
            it += 1

    np_number = np.array(number_matrix)

    plt.imshow(np_number)
    plt.show()


if __name__ == "__main__":
    training_data = read_input("optdigits.tra")
    test_data = read_input("optdigits.tes")
    # visualize_number(training_data[3])
    training_numbers = get_results(training_data)
    test_numbers = get_results(test_data)
    perfect_models = centroid(training_data, training_numbers)
    visualize_number(perfect_models[2])
    # print(perfect_models)
    # training_error = [0, 0]
    # test_error = [0, 0]
    # k = 1
    # training_error[0], training_euclidean = knn(training_data, training_data, "euclidean", k)
    # training_error[1], training_cos = knn(training_data, training_data, "euc", k)
    # test_error[0], test_euclidean = knn(training_data, test_data, "euclidean", k)
    # test_error[1], test_cos = knn(training_data, test_data, "euc", k)
    # write_results(training_error, training_numbers, training_euclidean, training_cos,
    #            test_error, test_numbers, test_euclidean, test_cos, k)
    