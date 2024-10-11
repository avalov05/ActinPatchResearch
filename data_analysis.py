#!/usr/bin/env python3

#imports
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv


#constants

#functions 

def graph_combinations(file):
    combinations = []

    csv = pd.read_csv(file)
    for element1 in csv:
        for element2 in csv:
            if element1 != element2 and element1 != ' ' and element2 != ' ':
                combinations.append([element1, element2])

    return combinations

def list_all_columns(file):
    columns = []
    csv = pd.read_csv(file)
    for element in csv:
        if element != ' ':
            columns.append(element)
    return columns

def find_all_data(path):
    files = []
    for filename in os.listdir(path):
        f = os.path.join(path, filename)
        if os.path.isfile(f):
            files.append(f)
    return(files)


def read_csv(f_list, comb):
    for names in comb:
        for file in f_list:
            csv = pd.read_csv(file)
            try:
                print(names[0], names[1])
                plt.scatter(csv[names[0]], csv[names[1]])
            except KeyError:
                print("Was not able to find the key...")
        plt.title(names[0] + " VS " + names[1])
        plt.savefig("./graphed_data/" + names[0] + names[1] + ".png")
        plt.cla()

def make_time_graphs(f_list, columns, destination):
    for name in columns:
        if name != "Time" and name != "time":
            for file in f_list:
                csv = pd.read_csv(file)
                try:
                    print(name)
                    plt.scatter(csv["Time"], csv[name])
                except KeyError:
                    print("Was not able to find the key...")
        plt.title("Time VS " + name)
        plt.savefig(destination + "/Time" + name + ".png")

def find_column_index_by_name(name, file):
    with open(file) as csv_file:
        csv_data = csv.reader(csv_file)
        counter = 0
        index = None
        for line in csv_data:
            for column in line:
                if column == name:
                    index = counter
                counter += 1
            if index == None:
                print(name + " does not exist...")
        return index

def line_num_in_csv(file):
    with open(file) as csv_f:
        reader = csv.reader(csv_f)
        return len(list(reader))

def multiple_csv_to_fill_dict(f_list, columns):
    data_dict={}
    for name in columns:
        if name != "Time" and name != "time":
            data_dict[name] = []
            column_index = find_column_index_by_name(name, f_list[0])
            #print(line_num_in_csv(f_list[0]))
            for line_num in range(1,line_num_in_csv(f_list[0])):
                sum = 0
                min = None
                max = 0
                for file in f_list:
                    with open(file) as file:
                        line_count = 0
                        csv_f = csv.reader(file)
                        for line in csv_f:
                            if line_count == line_num:
                                item = float(line[column_index])
                                sum += item
                                if max < item:
                                    #print("max found")
                                    max = item
                                if min != None:
                                    if min > item:
                                        #print("min found")
                                        min = item
                                else:
                                    min = item
                            line_count += 1
                    #print(name, line_num, min, max)
                #print("------------")
                average = sum/len(f_list)
                #print(name, line_num, min, max, average)
                data_dict[name].append({"min": min, "average": average, "max": max})
    print(data_dict)
    # data_dict={}
    # for name in columns:
    #     data_dict[name] = {
            
    #     }
    #     if name != "Time" and name != "time":
    #         for file in f_list:
    #             file_items = []
    #             with open(file) as csv_file:
    #                 csv_data = csv.reader(csv_file)
    #                 counter = 0
    #                 index = None
    #                 header = True
    #                 for line in csv_data:
    #                     for column in line:
    #                         if column == name:
    #                             index = counter
    #                         counter += 1
    #                     if index == None:
    #                         print(name + " does not exist...")
    #                         break
    #                     if header != True:
    #                         file_items.append(line[index])
    #                     header = False
    #             data_dict[name].append(file_items)
    # print(data_dict)
    

        #         csv = pd.read_csv(file)
        #         try:
        #             #print(name)
        #             #plt.scatter(csv["Time"], csv[name])
        #             items.append(csv[name])
        #         except KeyError:
        #             print("Was not able to find the key...")
        #     print(items)
        # plt.title("Time VS " + name)
        # plt.savefig(destination + "/Time" + name + ".png")
        # plt.cla()

def plot_column_fill():
    print

#functions-end


#main
def main():
    time_graph_folder_path = "/Users/antonvalov/Documents/PatchData/time_graphs"
    csv_files_path = "/Users/antonvalov/Documents/PatchData/data"
    csv_for_column_search_path = "/Users/antonvalov/Documents/PatchData/data/240611_ySM329_A_005 - Denoised_patch001.csv"
    #print(graph_combinations("/Users/antonvalov/Documents/PatchData/data/240611_ySM329_A_005 - Denoised_patch001.csv"))
    #read_csv(find_all_data("/Users/antonvalov/Documents/PatchData/data"), graph_combinations("/Users/antonvalov/Documents/PatchData/data/240611_ySM329_A_005 - Denoised_patch001.csv"))
    multiple_csv_to_fill_dict(find_all_data(csv_files_path), list_all_columns(csv_for_column_search_path))

#main call
if __name__ == "__main__":
    main()

