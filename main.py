import os
from utils.calculations import euclidean_diff, cos_distance, get_most_common
from utils.io import read_input, write_results
from utils.plotting import visualize_number, centroid_visualization

#for calculating accuracy of each number
def get_values(images):
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
        if result == image[64]:
            error_counter += 1
            model[result] += 1

    return error_counter / len(training_data), model


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


def knn_main_function(training_data, training_numbers, test_data, test_numbers, k):
    training_error = [0, 0]
    test_error = [0, 0]
    training_error[0], training_euclidean = knn(training_data, training_data, "euclidean", k)
    training_error[1], training_cos = knn(training_data, training_data, "euc", k)
    test_error[0], test_euclidean = knn(test_data, training_data, "euclidean", k)
    test_error[1], test_cos = knn(test_data, training_data, "euc", k)
    write_results("output/output_knn.txt", training_error, training_numbers, training_euclidean, training_cos,
                test_error, test_numbers, test_euclidean, test_cos, k)


def centroid_main_function(training_data, training_numbers, test_data, test_numbers):
    training_error = [0, 0]
    test_error = [0, 0]
    training_models = centroid_models(training_data, training_numbers)
    training_error[0], training_euclidean = centroid_compare(training_data, training_models, "euclidean")
    training_error[1], training_cos = centroid_compare(training_data, training_models, "euc")
    test_error[0], test_euclidean = centroid_compare(test_data, training_models, "euclidean")
    test_error[1], test_cos = centroid_compare(test_data, training_models, "euc")
    write_results("output/output_centroid.txt", training_error, training_numbers, training_euclidean, training_cos,
                test_error, test_numbers, test_euclidean, test_cos, -1)
    visualize_number(training_models)


if __name__ == "__main__":
    training_data = read_input("input/optdigits.tra")
    test_data = read_input("input/optdigits.tes")

    training_numbers = get_values(training_data)
    test_numbers = get_values(test_data)

    if not os.path.exists("plots"):
        os.makedirs("plots")
    centroid_visualization(test_data)

    if not os.path.exists("output"):
         os.makedirs("output")
    knn_main_function(training_data, training_numbers, test_data, test_numbers, 2)
    centroid_main_function(training_data, training_numbers, test_data, test_numbers)