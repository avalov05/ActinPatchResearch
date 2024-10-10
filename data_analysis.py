#!/usr/bin/env python3

#imports
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


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
        plt.cla()

#functions-end


#main
def main():
    time_graph_folder_path = "/Users/antonvalov/Documents/PatchData/time_graphs"
    csv_files_path = "/Users/antonvalov/Documents/PatchData/data"
    csv_for_column_search_path = "/Users/antonvalov/Documents/PatchData/data/240611_ySM329_A_005 - Denoised_patch001.csv"
    #print(graph_combinations("/Users/antonvalov/Documents/PatchData/data/240611_ySM329_A_005 - Denoised_patch001.csv"))
    #read_csv(find_all_data("/Users/antonvalov/Documents/PatchData/data"), graph_combinations("/Users/antonvalov/Documents/PatchData/data/240611_ySM329_A_005 - Denoised_patch001.csv"))
    make_time_graphs(find_all_data(csv_files_path), list_all_columns(csv_for_column_search_path), time_graph_folder_path)

#main call
if __name__ == "__main__":
    main()

