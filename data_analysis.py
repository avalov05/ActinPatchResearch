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
#functions-end


#main
def main():
    #print(graph_combinations("/Users/antonvalov/Documents/PatchData/data/240611_ySM329_A_005 - Denoised_patch001.csv"))
    read_csv(find_all_data("/Users/antonvalov/Documents/PatchData/data"), graph_combinations("/Users/antonvalov/Documents/PatchData/data/240611_ySM329_A_005 - Denoised_patch001.csv"))

#main call
if __name__ == "__main__":
    main()

