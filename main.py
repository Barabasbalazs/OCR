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

            
            

if __name__ == "__main__":
    training_data = read_input("optdigits.tra")
    test_data = read_input("optdigits.tes")
    training_numbers = get_results(training_data)
    test_numbers = get_results(test_data)
    training_error, model = knn(training_data, test_data, "euclidean", 1)
    print(training_error)
    for i in range(10):
        print(i, " - ", model[i] / training_numbers[i])