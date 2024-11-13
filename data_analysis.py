#!/usr/bin/env python3

#imports
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv
import json
from mpl_toolkits import mplot3d


#constants

#functions 

'''functions to make a dict(unefficient)
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
        plt.savefig("/Users/antonvalov/Documents/PatchData/graphed_data/" + names[0] + names[1] + ".png")
        plt.cla()

def make_time_graphs(f_list, columns, destination):
    for name in columns:
        if name[0] == "Time":
            if name[1] != "Time":
                print("Creating", name[0], "VS", name[1], "graph...")
                counter = 1
                for file in f_list:
                    csv = pd.read_csv(file)
                    try:
                        plt.scatter(csv["Time"], csv[name[1]], label = "File " + str(counter))
                    except KeyError:
                        print("Was not able to find the key...")
                    counter += 1
                print(counter)
                plt.subplots_adjust(right=0.78)
                plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
                plt.title("Time VS " + name[1])
                plt.ylabel(name[1])
                plt.xlabel("Time")
                plt.savefig(destination + "/Time" + name[1] + ".png")
                plt.cla()
        

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
    count = 0
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
                            print("Iteration", count)
                            count += 1
                            line_count += 1
                    #print(name, line_num, min, max)
                #print("------------")
                average = sum/len(f_list)
                #print(name, line_num, min, max, average)
                data_dict[name].append({"min": min, "average": average, "max": max})
    return data_dict'''

def list_files(path):
    files = []
    for filename in os.listdir(path):
        f = os.path.join(path, filename)
        if os.path.isfile(f):
            files.append(f)
    return(files)

# returns a list of the columns in the csv file excluding the time column
def list_columns_excluding_time(file):
    # try:

    with open(file) as csv_file:
        for line in csv_file:
            names = line.strip()
            names = names.split(",")  #get the header names
            if "time" not in names and "Time" not in names: #check that time is in it
                raise Exception("missing Time column!")
            if "time" in names:      #remove time from the list of column names
                names.remove("time")
            else:
                names.remove("Time")
            return names
    # except FileNotFoundError:
    #     print(file + " not found")
    # except:
    #     print("Missing Time column!")
    # else:
    #     print("Column names found...")
    #     return names
    
def csv_file_to_dict(file, column_list):
    #need to exclude time column
    file_data = {}
    for name in column_list:   #creates a dictionary with names:empty_list to fill later
        file_data[name] = []
    with open(file) as csv_file:
        next(csv_file)
        for line in csv_file:
            line = line.strip().split(",")[1:]
            index = 0
            for name in column_list:
                file_data[name].append(line[index])
                index += 1
        return file_data
    
def folder_to_dict_list(folder, column_names):
    unorganized_data = []
    files = list_files(folder)
    column_names = list_columns_excluding_time(files[0])
    for file in files:
        dict = csv_file_to_dict(file, column_names)
        unorganized_data.append(dict)
    return unorganized_data

def dict_list_to_data(unorganized_data, column_names, max_lines):
    data = {}
    time_min_data = []
    time_max_data = []
    time_average_data = []
    min_t = {}
    max_t = {}
    average_t = {}
    for name in column_names:
        min_t[name] = True
        max_t[name] = 0
        average_t[name] = []
    for time in range(max_lines):
        min = min_t.copy()
        max = max_t.copy()
        average = {name: [] for name in column_names}
        for dict in unorganized_data:
            for name in column_names:
                try:
                    if min[name] == True:
                        min[name] = float(dict[name][time])
                    if min[name] > float(dict[name][time]):
                        min[name] = float(dict[name][time])
                    if max[name] < float(dict[name][time]):
                        max[name] = float(dict[name][time])
                    average[name].append(float(dict[name][time]))
                except:
                    #print("EXCEPTED")
                    continue
        for name in column_names:
            average[name] = sum(average[name])/len(average[name])
        # print("TIME", time)
        # print("MIN", min)
        # print("MAX",max)
        # print("AVERAGE",average)
        time_min_data.append(min)
        time_max_data.append(max)
        time_average_data.append(average)
    for name in column_names:
        data[name] = []
        for time in range(max_lines):
            data[name].append({})
            data[name][time]["min"] = time_min_data[time][name]
            data[name][time]["average"] = time_average_data[time][name]
            data[name][time]["max"] = time_max_data[time][name]
    return data

            
                    
                    



def dict_to_json(dict):
    with open("data.json", "w") as outfile: 
        json.dump(dict, outfile)

def json_to_dict(file):
    with open(file) as json_file:
        dict = json.load(json_file)
    return dict


def plot_column_fill(dict, name, destination):
    min = []
    max = []
    average = []
    t = []
    time = 1.0
    for t_data in dict[name]:
        min.append(t_data["min"])
        max.append(t_data["max"])
        average.append(t_data["average"])
        t.append(time)
        time += 1.0
    plt.plot(t, average, color="orange")
    plt.legend([name + ' average'])
    plt.fill_between(t, max, min, color="gray")
    plt.title("Time VS " + name)
    plt.ylabel(name)
    plt.xlabel("Time")
    plt.savefig(destination + "/Time" + name + ".png")
    plt.cla()
    return average

def plot_approximate_graph(name, data, destination, choose_accurate = False, degree = 3):
    x = np.array([i for i in range(len(data))])
    y = np.array(data)
    if choose_accurate:
        degrees = range(1,100)
        difference = {}
        for degree in degrees:
            difference[degree] = 0
            coefficients = np.polyfit(x, y, degree)
            poly_func = np.poly1d(coefficients)
            y_fit = poly_func(x)
            plt.plot(x, y, 'o', label='Original Data')
            plt.plot(x, y_fit, label=f'Degree {degree}')
            plt.subplots_adjust(right=0.78)
            plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
            plt.title("Time VS " + name)
            plt.ylabel(name)
            plt.xlabel("Time")
            plt.savefig(destination + "/all_degree_graphs/TimeAverage" + name + "DegreeOf" + str(degree) + ".png")
            plt.cla()
            for index in range(len(data)):
                org_instance = data[index]
                new_instance = y_fit[index]
                difference[degree] += abs(org_instance - new_instance)
                difference[degree] = float(difference[degree])
        min = True
        most_accurate_degree = 0
        for key in difference:
            if min == True:
                min = difference[key]
                most_accurate_degree = key
            if min > difference[key]:
                min = difference[key]
                most_accurate_degree = key
        print(most_accurate_degree)
        coefficients = np.polyfit(x, y, most_accurate_degree)
        poly_func = np.poly1d(coefficients)
        y_fit = poly_func(x)
        plt.plot(x, y, 'o', label='Original Data')
        plt.plot(x, y_fit, label=f'Degree {most_accurate_degree}')
        plt.subplots_adjust(right=0.78)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
        plt.title("Time VS " + name)
        plt.ylabel(name)
        plt.xlabel("Time")
        plt.savefig(destination + "/TimeAverage" + name + "DegreeOf" + str(most_accurate_degree) + ".png")
        plt.cla()
        return difference
    else:
        coefficients = np.polyfit(x, y, degree)
        poly_func = np.poly1d(coefficients)
        y_fit = poly_func(x)
        plt.plot(x, y, 'o', label='Original Data')
        plt.plot(x, y_fit, label=f'Degree {degree}')
        plt.subplots_adjust(right=0.78)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
        plt.title("Time VS Average_" + name)
        plt.ylabel(name)
        plt.xlabel("Time")
        plt.savefig(destination + "/TimeAverage" + name + "DegreeOf" + str(degree) + ".png")
        plt.cla()
        degree_count = degree
        print("Equation: y = ", end="")
        for coefficient in coefficients[:-1]:
            print(str(coefficient) +"x^" + str(degree_count) + " + ", end="")
            degree_count -= 1
        print(coefficients[-1])


    
        
    


def test_filereading_with_open(test_file):
    with open(test_file) as file:
        count = 0
        for line in file:
            print(count)
            count += 1

def longest_file(files):
    max = 0
    for file in files:
        line = 0
        with open(file) as file_f:
            for lines in file_f:
                line += 1
        if max < line:
            max = line
    return max


#functions-end


#main
def main():
    time_graph_folder_path = "/Users/antonvalov/Documents/PatchData/time_graphs"
    csv_files_path = "/Users/antonvalov/Documents/PatchData/data"
    csv_for_column_search_path = "/Users/antonvalov/Documents/PatchData/data/240611_ySM329_A_005 - Denoised_patch001.csv"
    graphs_path = "/Users/antonvalov/Documents/PatchData/graphed_data/"
    #print(graph_combinations("/Users/antonvalov/Documents/PatchData/data/240611_ySM329_A_005 - Denoised_patch001.csv"))
    ### make_time_graphs(find_all_data("/Users/antonvalov/Documents/PatchData/data"), graph_combinations("/Users/antonvalov/Documents/PatchData/data/240611_ySM329_A_005 - Denoised_patch001.csv"), "/Users/antonvalov/Documents/PatchData/time_graphs")
    files = list_files(csv_files_path)

    
    """tests""" 
    columns = list_columns_excluding_time(csv_for_column_search_path)
    unorganized_data = folder_to_dict_list(csv_files_path, columns)
    dict = dict_list_to_data(unorganized_data, columns, longest_file(files) - 1)


    # csv_file_to_dict(csv_for_column_search_path, list_columns_excluding_time(csv_for_column_search_path))
    # for name in list_columns_excluding_time(csv_for_column_search_path):
    #     print(name)
    # test_filereading_with_open(csv_for_column_search_path)
    # dict_to_json(multiple_csv_to_fill_dict(find_all_data(csv_files_path), list_all_columns(csv_for_column_search_path)))
    # for name in columns:
    #     if name != "Time":
    #         print("Creating", name, "graph...")
    #         plot_column_fill(dict, name, graphs_path)

    for name in columns:
        if name == "Area":
            print("Creating", name, "graph...")
            average = plot_column_fill(dict, name, graphs_path)
    
    plot_approximate_graph("Area", average, graphs_path)

    # csv = pd.read_csv("/Users/antonvalov/Documents/PatchData/data/240611_ySM329_A_005 - Denoised_patch001.csv")
    # fig = plt.figure()
    # ax = plt.axes(projection = "3d")
    # ax.plot_surface(csv["FeretX"], csv["FeretY"], csv["Time"], vmin=csv["Time"].min() * 2)
    # plt.show()


#main call
if __name__ == "__main__":
    main()

