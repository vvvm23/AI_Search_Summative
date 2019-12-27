import os
import sys
import time
import random

def read_file_into_string(input_file, from_ord, to_ord):
    # take a file "input_file", read it character by character, strip away all unwanted
    # characters with ord < "from_ord" and ord > "to_ord" and return the concatenation
    # of the file as the string "output_string"
    the_file = open(input_file,'r')
    current_char = the_file.read(1)
    output_string = ""
    while current_char != "":
        if ord(current_char) >= from_ord and ord(current_char) <= to_ord:
            output_string = output_string + current_char
        current_char = the_file.read(1)
    the_file.close()
    return output_string

def stripped_string_to_int(a_string):
    # take a string "a_string" and strip away all non-numeric characters to obtain the string
    # "stripped_string" which is then converted to an integer with this integer returned
    a_string_length = len(a_string)
    stripped_string = "0"
    if a_string_length != 0:
        for i in range(0,a_string_length):
            if ord(a_string[i]) >= 48 and ord(a_string[i]) <= 57:
                stripped_string = stripped_string + a_string[i]
    resulting_int = int(stripped_string)
    return resulting_int

def get_string_between(from_string, to_string, a_string, from_index):
    # look for the first occurrence of "from_string" in "a_string" starting at the index
    # "from_index", and from the end of this occurrence of "from_string", look for the first
    # occurrence of the string "to_string"; set "middle_string" to be the sub-string of "a_string"
    # lying between these two occurrences and "to_index" to be the index immediately after the last
    # character of the occurrence of "to_string" and return both "middle_string" and "to_index"
    middle_string = ""              # "middle_string" and "to_index" play no role in the case of error
    to_index = -1                   # but need to initialized to something as they are returned
    start = a_string.find(from_string,from_index)
    if start == -1:
        flag = "*** error: " + from_string + " doesn't appear"
        #trace_file.write(flag + "\n")
    else:
        start = start + len(from_string)
        end = a_string.find(to_string,start)
        if end == -1:
            flag = "*** error: " + to_string + " doesn't appear"
            #trace_file.write(flag + "\n")
        else:
            middle_string = a_string[start:end]
            to_index = end + len(to_string)
            flag = "good"
    return middle_string,to_index,flag

def string_to_array(a_string, from_index, num_cities):
    # convert the numbers separated by commas in the file-as-a-string "a_string", starting from index "from_index",
    # which should point to the first comma before the first digit, into a two-dimensional array "distances[][]"
    # and return it; note that we have added a comma to "a_string" so as to find the final distance
    # distance_matrix = []
    if from_index >= len(a_string):
        flag = "*** error: the input file doesn't have any city distances"
        #trace_file.write(flag + "\n")
    else:
        row = 0
        column = 1
        row_of_distances = [0]
        flag = "good"
        while flag == "good":
            middle_string, from_index, flag = get_string_between(",", ",", a_string, from_index)
            from_index = from_index - 1         # need to look again for the comma just found
            if flag != "good":
                flag = "*** error: there aren't enough cities"
                # trace_file.write(flag + "\n")
            else:
                distance = stripped_string_to_int(middle_string)
                row_of_distances.append(distance)
                column = column + 1
                if column == num_cities:
                    distance_matrix.append(row_of_distances)
                    row = row + 1
                    if row == num_cities - 1:
                        flag = "finished"
                        row_of_distances = [0]
                        for i in range(0, num_cities - 1):
                            row_of_distances.append(0)
                        distance_matrix.append(row_of_distances)
                    else:
                        row_of_distances = [0]
                        for i in range(0,row):
                            row_of_distances.append(0)
                        column = row + 1
        if flag == "finished":
            flag = "good"
    return flag

def make_distance_matrix_symmetric(num_cities):
    # make the upper triangular matrix "distance_matrix" symmetric;
    # note that there is nothing returned
    for i in range(1,num_cities):
        for j in range(0,i):
            distance_matrix[i][j] = distance_matrix[j][i]

# read input file into string

#######################################################################################################
############ now we read an input file to obtain the number of cities, "num_cities", and a ############
############ symmetric two-dimensional list, "distance_matrix", of city-to-city distances. ############
############ the default input file is given here if none is supplied via a command line   ############
############ execution; it should reside in a folder called "city-files" whether it is     ############
############ supplied internally as the default file or via a command line execution.      ############
############ if your input file does not exist then the program will crash.                ############

input_file = "AISearchfile175.txt"

#######################################################################################################

# you need to worry about the code below until I tell you; that is, do not touch it!

if len(sys.argv) == 1:
    file_string = read_file_into_string("../city-files/" + input_file,44,122)
else:
    input_file = sys.argv[1]
    file_string = read_file_into_string("../city-files/" + input_file,44,122)
file_string = file_string + ","         # we need to add a final comma to find the city distances
                                        # as we look for numbers between commas
print("I'm working with the file " + input_file + ".")
                                        
# get the name of the file

name_of_file,to_index,flag = get_string_between("NAME=", ",", file_string, 0)

if flag == "good":
    print("I have successfully read " + input_file + ".")
    # get the number of cities
    num_cities_string,to_index,flag = get_string_between("SIZE=", ",", file_string, to_index)
    num_cities = stripped_string_to_int(num_cities_string)
else:
    print("***** ERROR: something went wrong when reading " + input_file + ".")
if flag == "good":
    print("There are " + str(num_cities) + " cities.")
    # convert the list of distances into a 2-D array
    distance_matrix = []
    to_index = to_index - 1             # ensure "to_index" points to the comma before the first digit
    flag = string_to_array(file_string, to_index, num_cities)
if flag == "good":
    # if the conversion went well then make the distance matrix symmetric
    make_distance_matrix_symmetric(num_cities)
    print("I have successfully built a symmetric two-dimensional array of city distances.")
else:
    print("***** ERROR: something went wrong when building the two-dimensional array of city distances.")

#######################################################################################################
############ end of code to build the distance matrix from the input file: so now you have ############
############ the two-dimensional "num_cities" x "num_cities" symmetric distance matrix     ############
############ "distance_matrix[][]" where "num_cities" is the number of cities              ############
#######################################################################################################

# now you need to supply some parameters ...

#######################################################################################################
############ YOU NEED TO INCLUDE THE FOLLOWING PARAMETERS:                                 ############
############ "my_user_name" = your user-name, e.g., mine is dcs0ias                        ############

my_user_name = "vvvm23"

############ "my_first_name" = your first name, e.g., mine is Iain                         ############

my_first_name = "Alexander"

############ "my_last_name" = your last name, e.g., mine is Stewart                        ############

my_last_name = "McKinney"

############ "alg_code" = the two-digit code that tells me which algorithm you have        ############
############ implemented (see the assignment pdf), where the codes are:                    ############
############    BF = brute-force search                                                    ############
############    BG = basic greedy search                                                   ############
############    BS = best_first search without heuristic data                              ############
############    ID = iterative deepening search                                            ############
############    BH = best_first search with heuristic data                                 ############
############    AS = A* search                                                             ############
############    HC = hilling climbing search                                               ############
############    SA = simulated annealing search                                            ############
############    GA = genetic algorithm                                                     ############

alg_code = "AS"

############ you can also add a note that will be added to the end of the output file if   ############
############ you like, e.g., "in my basic greedy search, I broke ties by always visiting   ############
############ the first nearest city found" or leave it empty if you wish                   ############

added_note = ""

############ the line below sets up a dictionary of codes and search names (you need do    ############
############ nothing unless you implement an alternative algorithm and I give you a code   ############
############ for it when you can add the code and the algorithm to the dictionary)         ############

codes_and_names = {'BF' : 'brute-force search',
                   'BG' : 'basic greedy search',
                   'BS' : 'best_first search without heuristic data',
                   'ID' : 'iterative deepening search',
                   'BH' : 'best_first search with heuristic data',
                   'AS' : 'A* search',
                   'HC' : 'hilling climbing search',
                   'SA' : 'simulated annealing search',
                   'GA' : 'genetic algorithm'}

#######################################################################################################
############    now the code for your algorithm should begin                               ############
#######################################################################################################

'''
    A* Search Algorithm

    Structure:
        Some kind of State class that acts as a node in the search tree.
        It Should contain the current State (list of cities already visited)
        and the f cost to visit the node. Other information may be stored there.
        It should also have the capability to produce all possible child states
        from the current state by checking all actions. So we can add them to
        the fringe.

    Algorithm:
        1)  Randomly pick, or pick the first, city to visit. Generate an initial state
            from this.
        2)  Get all child states from this initial state and compute path cost to visit
            plus heuristic cost.
        3)  Add all these child states to the fringe.
        4)  Select the state in the fringe with the lowest combined path cost and heuristic cost.
        5)  Repeat by expanding the selected state and considering all on fringe.
        6)  Halt when there is a goal state in the fringe that has the lowest f cost.

    Possible Heuristics:
        Greedy Search from current node. ie. continue tour picking lowest at each point.
        Take average of path costs leading from this state.
        Lower score longer/shorter the current path is.
        Lower score for more balanced exploration
        A weird mix of many.
'''

import bisect

true_start = time.time()
NB_CITIES = len(distance_matrix)

class State:
    def __init__(self, current_city, cities=[], path_cost_from_root=0, nb_cities=None, nb_remaining=None):
        global NB_CITIES
        self.cities = cities
        self.nb_cities = len(cities) if nb_cities == None else nb_cities
        self.current_city = current_city
        self.remaining_cities = list(set(range(NB_CITIES)) - set(cities))
        self.nb_remaining = len(self.remaining_cities) if nb_remaining == None else nb_remaining
        self.path_cost_from_root = path_cost_from_root
        self.is_goal = nb_cities == (NB_CITIES + 1)
        self.total_cost = path_cost_from_root + self.heuristic()

    # greedy continuation heuristic
    def heuristic(self):
        if self.is_goal:
            return 0

        total = 0
        g_remaining_cities = [x for x in self.remaining_cities]
        g_current_city = self.current_city

        g_nb_remaining = self.nb_remaining

        while g_nb_remaining:
            g_current_costs = [(distance_matrix[g_current_city][x], x) for x in g_remaining_cities]
            total_add, g_current_city = min(g_current_costs)
            total += total_add
            g_remaining_cities.remove(g_current_city)
            g_nb_remaining -= 1

        total += distance_matrix[g_current_city][self.cities[0]]

        return total

    def state_from_action(self, action):
        '''
            Inputs:
                action - (next_city, path_cost)
            Outputs:
                Next state given the action
        '''
        next_cities = [i for i in self.cities]
        next_cities.append(action[0])
        return State(action[0], cities=next_cities, 
                    path_cost_from_root=self.path_cost_from_root+action[1],
                    nb_cities=self.nb_cities+1,
                    nb_remaining=self.nb_remaining-1)

    def get_child_states(self):
        child_states = [] # Changing to a generator does little for performance.
        if self.nb_remaining:
            for possible_city in self.remaining_cities:
                path_cost = distance_matrix[self.current_city][possible_city]
                child_states.append(self.state_from_action((possible_city, path_cost)))
        else:
            path_cost = distance_matrix[self.current_city][self.cities[0]]
            child_states.append(self.state_from_action((self.cities[0], path_cost)))

        return child_states

    def __lt__(self, other):
        return self.total_cost < other.total_cost

# given a state, move to completion in greedy manner
def continue_greedily(state):
    total = state.path_cost_from_root
    g_remaining_cities = [x for x in state.remaining_cities]
    g_current_city = state.current_city
    g_cities = [x for x in state.cities]

    nb_remaining = len(g_remaining_cities)

    while nb_remaining:
        g_current_costs = [(distance_matrix[g_current_city][x], x) for x in g_remaining_cities]
        total_add, g_current_city = min(g_current_costs)
        total += total_add
        g_remaining_cities.remove(g_current_city)
        g_cities.append(g_current_city)
        nb_remaining -= 1

    total += distance_matrix[g_current_city][state.cities[0]]
    g_cities.append(state.cities[0])
    return g_cities, total

def as_search(ran_start=True):
    '''
        Inputs:
            distance_matrix - Symmetric matrix of distances between cities
            ran_start - Whether to choose random start or from node 0. Default 0.
        Outputs:
            tour - List of cities visited in order
            tour_length - Total cost of the tour
    '''

    KILL_TIME_MAX = 50.0 # Ensure this is less than 60.0 including time to finish.

    kill_time_start = time.time()

    initial_city = random.randint(0, NB_CITIES-1) if ran_start else 0
    initial_state = State(initial_city, cities=[initial_city])

    fringe = initial_state.get_child_states()
    fringe.sort()

    while True:
        min_state = fringe.pop(0)
        
        if time.time() - kill_time_start > KILL_TIME_MAX:
            # if time exceeds, greedily finish.
            print("Kill time exceeded. Terminating.")
            print("Calculating Greedily from current minimum.")
            tour, tour_length = continue_greedily(min_state)
            break

        if min_state.is_goal:
            tour = min_state.cities
            tour_length = min_state.path_cost_from_root
            break
        child_states = min_state.get_child_states()
        
        for s in child_states:
            bisect.insort_left(fringe, s)

    return tour, tour_length

start_time = time.time()
tour, tour_length = as_search(ran_start=False)
end_time = time.time()
true_end = time.time()
print(f"A* search took \t{end_time - start_time}")
print(f"Program time \t{true_end - true_start}")

#######################################################################################################
############ the code for your algorithm should now be complete and you should have        ############
############ computed a tour held in the list "tour" of length "tour_length"               ############
#######################################################################################################

# you do not need to worry about the code below; that is, do not touch it

#######################################################################################################
############ start of code to verify that the constructed tour and its length are valid    ############
#######################################################################################################


check_tour_length = 0
for i in range(0,num_cities-1):
    check_tour_length = check_tour_length + distance_matrix[tour[i]][tour[i+1]]
check_tour_length = check_tour_length + distance_matrix[tour[num_cities-1]][tour[0]]
flag = "good"
if tour_length != check_tour_length:
    flag = "bad"
if flag == "good":
    print("Great! Your tour-length of " + str(tour_length) + " from your " + codes_and_names[alg_code] + " is valid!")
else:
    print("***** ERROR: Your claimed tour-length of " + str(tour_length) + "is different from the true tour length of " + str(check_tour_length) + ".")

#######################################################################################################
############ start of code to write a valid tour to a text (.txt) file of the correct      ############
############ format; if your tour is not valid then you get an error message on the        ############
############ standard output and the tour is not written to a file                         ############
############                                                                               ############
############ the name of file is "my_user_name" + mon-dat-hr-min-sec (11 characters);      ############
############ for example, dcs0iasSep22105857.txt; if dcs0iasSep22105857.txt already exists ############
############ then it is overwritten                                                        ############
#######################################################################################################

if flag == "good":
    local_time = time.asctime(time.localtime(time.time()))   # return 24-character string in form "Tue Jan 13 10:17:09 2009"
    output_file_time = local_time[4:7] + local_time[8:10] + local_time[11:13] + local_time[14:16] + local_time[17:19]
                                                             # output_file_time = mon + day + hour + min + sec (11 characters)
    output_file_name = my_user_name + output_file_time + ".txt"
    f = open(output_file_name,'w')
    f.write("USER = " + my_user_name + " (" + my_first_name + " " + my_last_name + ")\n")
    f.write("ALGORITHM = " + alg_code + ", FILENAME = " + name_of_file + "\n")
    f.write("NUMBER OF CITIES = " + str(num_cities) + ", TOUR LENGTH = " + str(tour_length) + "\n")
    f.write(str(tour[0]))
    for i in range(1,num_cities):
        f.write("," + str(tour[i]))
    if added_note != "":
        f.write("\nNOTE = " + added_note)
    f.close()
    print("I have successfully written the tour to the output file " + output_file_name + ".")
