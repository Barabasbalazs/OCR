import matplotlib.pyplot as plt
from .calculations import sort_data, cos_distance

def centroid_visualization(test_data):
    rows, cols = (len(test_data), len(test_data))
    test_image = [[0 for i in range(cols)] for j in range(rows)]
    sorted_test = sort_data(test_data)
    
    for i in range(len(sorted_test)):
        for j in range(len(sorted_test)):
            test_image[i][j] = cos_distance(sorted_test[i][0: 64], sorted_test[j][0: 64])

    plt.imshow(test_image)
    #visaulize centroids
    plt.show()
    plt.savefig("plots/first.png")
    
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
    #save something
    plt.savefig("plots/second.png")
