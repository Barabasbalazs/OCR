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

    #the calculations are right, but the returned model is not

    return error_counter / len(training_data), model

        

def get_most_common(list):
    indexes = [0] * 10
    for i in list:
        indexes[i[0]] += 1
    return indexes.index(max(indexes))


def centroid_models(training_data, comparison_data):
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


def write_results(filename, training_error, training_numbers, training_euclidean, training_cos, 
                  test_error, test_numbers, test_euclidean, test_cos, k):
    file = open(filename ,"w")

    if k != -1:
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
    file.write("Test error on cos: {}\n".format(test_error[1]))
    file.write("Test error on models using cos\n")
    for i in range(10):
        file.write("{} - {}\n".format(i, test_cos[i] / test_numbers[i]))
    
    file.close()            


def visualize_number(data_of_image):
    _, ax_arr = plt.subplots(4, 3)

    x_index = 0
    y_index = 0
    for curr_image in data_of_image:
        number_matrix = []
        it = 0
        for i in range(8):
            number_matrix.append([])
            for j in range(8):
                number_matrix[i].append(curr_image[it])
                it += 1
        ax_arr[x_index, y_index].imshow(number_matrix)
        y_index += 1
        if y_index > 2:
            y_index = 0
            x_index += 1

    plt.show()


def knn_main_function(training_data, training_numbers, test_data, test_numbers, k):
    training_error = [0, 0]
    test_error = [0, 0]
    training_error[0], training_euclidean = knn(training_data, training_data, "euclidean", k)
    training_error[1], training_cos = knn(training_data, training_data, "euc", k)
    test_error[0], test_euclidean = knn(test_data, training_data, "euclidean", k)
    test_error[1], test_cos = knn(test_data, training_data, "euc", k)
    write_results("output_knn.txt", training_error, training_numbers, training_euclidean, training_cos,
                test_error, test_numbers, test_euclidean, test_cos, k)


def centroid_compare(data, model, mode):
    model_counter = [0] * 10 
    
    # learning error
    error_counter = 0
    for image in data:
        local_lim = (-1, 1000000) if mode == 'euclidean' else (-1, -2)
        for i in range(10):
            if mode == "euclidean":
                diff = euclidean_diff(model[i][0: 64], image[0: 64])
                if diff < local_lim[1]:
                    local_lim = (i ,diff)
            else:
                diff = cos_distance(model[i][0: 64], image[0: 64])
                if diff > local_lim[1]:
                    local_lim = (i ,diff)
        if local_lim[0] == image[64]:
            error_counter += 1
            model_counter[local_lim[0]] += 1
    
    return error_counter / len(data), model_counter


def centroid_main_function(training_data, training_numbers, test_data, test_numbers):
    training_error = [0, 0]
    test_error = [0, 0]
    training_models = centroid_models(training_data, training_numbers)
    training_error[0], training_euclidean = centroid_compare(training_data, training_models, "euclidean")
    training_error[1], training_cos = centroid_compare(training_data, training_models, "euc")
    test_error[0], test_euclidean = centroid_compare(test_data, training_models, "euclidean")
    test_error[1], test_cos = centroid_compare(test_data, training_models, "euc")
    write_results("output_centroid.txt", training_error, training_numbers, training_euclidean, training_cos,
                test_error, test_numbers, test_euclidean, test_cos, -1)
    visualize_number(training_models)


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


def centroid_visualization(test_data):
    rows, cols = (len(test_data), len(test_data))
    test_image = [[0 for i in range(cols)] for j in range(rows)]
    sorted_test = sort_data(test_data)
    
    for i in range(len(sorted_test)):
        for j in range(len(sorted_test)):
            test_image[i][j] = cos_distance(sorted_test[i][0: 64], sorted_test[j][0: 64])

    plt.imshow(test_image)
    plt.show()


if __name__ == "__main__":
    training_data = read_input("optdigits.tra")
    test_data = read_input("optdigits.tes")
    training_numbers = get_results(training_data)
    test_numbers = get_results(test_data)
    centroid_visualization(test_data)
    # knn_main_function(training_data, training_numbers, test_data, test_numbers, 2)
    # centroid_main_function(training_data, training_numbers, test_data, test_numbers)
    
    