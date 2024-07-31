def read_input(name_of_file):
    file = open(name_of_file, "r")
    arr = []
    for line in file:
        line_array = line.split(",")
        arr.append([int(element) for element in line_array])
    file.close()
    return arr

def write_results(filename, training_error, training_numbers, training_euclidean, training_cos, 
                  test_error, test_numbers, test_euclidean, test_cos, k):
    file = open(filename ,"w+")

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
