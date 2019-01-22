from NewNeuralMap import NewNeuralMap
import numpy as np
from PIL import Image
from timeit import default_timer as timer
import InputsGetter as ig
from matplotlib import pyplot as plt
import datetime
import ImageProcessor as ip


def main():
    print("Program started")
    myNewMain()
    print("Program finished")


def myNewMain():    # for images
    rows = 32
    cols = 32
    features = 1024
    number_of_classes = 5

    load_map_from_file = True
    learn_map = False
    build_classifier = False
    save_map_to_file = False

    number_of_threads_to_load_images = 45

    file_with_map = "main_map.txt"
    path = './Images/**/*.ppm'

    inputs = ig.get_all_images_vectors_mt(
        path, number_of_threads_to_load_images)

    if load_map_from_file:
        neural_map = load_map_from_file_func(file_with_map)
    else:
        neural_map = NewNeuralMap(rows, cols, features)

    if learn_map:
        learn_map_func(neural_map, inputs)

    if build_classifier:
        neural_map.build_classifier(number_of_classes, False)

    if save_map_to_file:
        save_map_to_file_func(neural_map, file_with_map)

    neural_map.print_classes()
    number_of_classes = neural_map.get_number_of_classes()
    print("Found %s classes" % number_of_classes)

    images = './Images/00012/*.ppm'
    images = ig.get_all_images_vectors_mt(
        images, 4)

    for i in range(len(images)):
        image_class = neural_map.get_winner_class(images[i])
        print(image_class)


def learn_map_func(neural_map, inputs):
    start = timer()
    print("Learning..")

    cycles = [1000, 2000, 3000, 4000, 5000, 7500, 10000, 15000]
    learning_rates = [1, 0.8, 0.7, 0.6, 0.5, 0.3, 0.2, 0.1]

    if len(cycles) != len(learning_rates):
        print("Learning parameters error")
        return

    print("cycles:")
    print(cycles)
    print("learning rates:")
    print(learning_rates)

    for i in range(len(cycles)):
        print(str(i+1) + " epoch of " + str(len(cycles)))
        neural_map.learn(inputs, cycles[i], learning_rates[i])

    end = timer()
    time_seconds = end - start

    print("Learning time: " + str(datetime.timedelta(seconds=time_seconds)))


def save_map_to_file_func(neural_map, path):
    neural_map.safe_to_file(path)


def load_map_from_file_func(path):
    neural_map = NewNeuralMap.read_from_file(path)
    return neural_map


def neural_network_test():
    rows = 32
    cols = 32
    features = 3
    elements = 5
    cycles = 1500
    learning_rate = 1
    number_of_classes = 3

    filename = "testmap.txt"

    # inputs = np.random.random((elements,features))

    inputs = np.array(([1, 0, 0], [0, 0, 1], [0, 1, 0]))

    inputs = np.vstack((inputs, [0.9, 0.1, 0.1]))
    inputs = np.vstack((inputs, [0.8, 0.15, 0.15]))
    inputs = np.vstack((inputs, [0.8, 0.2, 0.2]))

    inputs = np.vstack((inputs, [0.1, 0.9, 0.1]))
    inputs = np.vstack((inputs, [0.15, 0.8, 0.15]))
    inputs = np.vstack((inputs, [0.2, 0.8, 0.2]))

    inputs = np.vstack((inputs, [0.1, 0.1, 0.9]))
    inputs = np.vstack((inputs, [0.15, 0.15, 0.8]))
    inputs = np.vstack((inputs, [0.2, 0.2, 0.8]))

    newmap = NewNeuralMap(rows, cols, features)

    # print(inputs)

    # start = timer()
    # print("Learning..")

    # cycles = 1000
    # learning_rate = 1
    # newmap.learn(inputs, cycles, learning_rate)
    # cycles = 5000
    # learning_rate = 0.4
    # newmap.learn(inputs, cycles, learning_rate)

    # end = timer()
    # print("Learning time: %s seconds" %(end - start))
    # newmap.safe_to_file(filename)

    newmap = NewNeuralMap.read_from_file(filename)

    newmap.build_classifier(number_of_classes + 2, True)
    newmap.print()
    newmap.print_classes()

    number_of_classes = np.max(newmap.classes)
    print("Found %s classes" % number_of_classes)
    # newmap.print_classes()
    # newmap.safe_to_file(filename)


def images_loading_test(min_threads=35, max_threads=50):
    path = './Images/**/*.ppm'
    x = []
    y = []

    i = min_threads
    while i <= max_threads:
        print("%s threads running.." % (i))
        start = timer()
        inputs_mt = ig.get_all_images_vectors_mt(path, i)
        end = timer()

        x.append(i)
        y.append(end-start)
        i += 1

    min_time = min(y)
    optimum_number_of_threads = x[y.index(min(y))]

    print("************************")
    print("Best result:")
    print("%s threads " % optimum_number_of_threads)
    print("%s seconds" % min_time)
    print("************************")

    plt.plot(x, y)
    plt.title("Loading %s images time" % len(inputs_mt))
    plt.ylabel("Time in seconds")
    plt.xlabel("Number of threads")
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    main()
