import os
import shutil

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


class logger:
    def __init__(self, dir_name, path_to_source_image, path_to_style_image):
        self.data_array = []
        # self.data_array_header = ['iteration_number', 'total_loss', 'content_loss', 'style_loss', 'iteration_time']
        self.data_array_header = 'iteration_number, total_loss, content_loss, style_loss, iteration_time'

        # Create output dir, if exist delete
        self.dir_name = dir_name
        # self.path = os.getcwd()
        self.path = dir_name + '/'

        if os.path.isdir(self.path):
            shutil.rmtree(self.path)

        os.mkdir(self.path)

        # Create dir for images from processing
        self.path_process = self.path + 'processing_images/'
        os.mkdir(self.path_process)

        # Create dir for plots
        self.path_plots = self.path + 'plots/'
        os.mkdir(self.path_plots)

        # Copy files
        self.__copy_file__(path_to_source_image, self.path, 'content')
        self.__copy_file__(path_to_style_image, self.path, 'style')

    def __copy_file__(self, source, destination_dir, name):
        file_path, file_extension = os.path.splitext(source)
        shutil.copy2(source, destination_dir + name + file_extension)

    # image ma typ Image
    def iteration_data(self, iteration_number, total_loss, content_loss, style_loss, iteration_time, image=None):
        # imgae == none => obrazek nie jest zapisywany do pliku
        # image!= None => obrazek jest zapisywany do pliku

        self.data_array.append(np.array([iteration_number, total_loss, content_loss, style_loss, iteration_time]))
        if image is not None:
            image.save(self.path_process + str(iteration_number) + '.jpg')
            
    def save_image_jpg(self, iteration_number=-1, image=None):
        if image is not None:
            if iteration_number >= 0:
                image.save(self.path_process + str(iteration_number) + '.jpg')
            else:
                image.save(self.path + 'output.jpg')
        else:
            print('Saving image failed! No Image provided.')

    def save_data_to_csv(self):
        # Zapisuje zebrane dane o iteracjach do pliku
        data = np.asarray(self.data_array)
        header = self.data_array_header
        np.savetxt(self.path + 'data.csv', data, delimiter=',', header=self.data_array_header, fmt='%1.10f')

    def draw_plots(self):
        # Ryzuje wykresy z danych oraz zapisuje je do plików
        iteration_array = []
        total_loss_array = []
        content_loss_array = []
        style_loss_array = []
        iteration_time_array = []

        for i in range(len(self.data_array)):
            iteration_array.append(self.data_array[i][0])
            total_loss_array.append(self.data_array[i][1])
            content_loss_array.append(self.data_array[i][2])
            style_loss_array.append(self.data_array[i][3])
            iteration_time_array.append(self.data_array[i][4])

        self.__draw_plot(iteration_array, total_loss_array, 'Iteration', 'Total loss', 'Total loss')
        self.__draw_plot(iteration_array, content_loss_array, 'Iteration', 'Content loss', 'Content loss')
        self.__draw_plot(iteration_array, style_loss_array, 'Iteration', 'Style loss', 'Style loss')
        self.__draw_plot(iteration_array, iteration_time_array, 'Iteration', 'Iteration time (s)', 'Iteration time')

    def __draw_plot(self, x_data, y_data, x_label, y_label, title):
        plt.plot(x_data, y_data)
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)

        plt.savefig(self.path_plots + title + '.png')
        plt.clf()
        # plt.show()
