#!/usr/bin/python
# -*- coding: utf-8 -*-

import pickle
import numpy
import itertools

class GroupFinder(object):
    def __init__(self):
        f = open("data-22.50.13.pkl", "rb")
        subj_dict = pickle.load(f)
        f.close()
        
        self.groups_dict = {}
        
        for subj_key,subj in subj_dict.iteritems():
            for group in subj.groups:
                self.groups_dict[group.n_id] = (group, subj.subject_name)

# Find the starting and ending time of the schedule
def check_start(matr):
    matrix = numpy.array(matr)
    for i in range(0,matrix.shape[0]):
        for e in matrix[i]:
            if e > 0:
                return 7+i
                
def check_end(matr):
    matrix = numpy.array(matr)
    for i in range(0, matrix.shape[0]):
        for e in matrix[matrix.shape[0]-i-1]:
            if e > 0:
                return 1+7+matrix.shape[0]-i-1
            
def groups_valid(groups, allowed_groups):
    for g_tup in allowed_groups:
        if not _one_of_tuple_contained(groups, g_tup):
            return False
    return True

def _one_of_tuple_contained(groups, tup):
    for g in tup:
        if g in groups:
            return True
    return False
    
f = open("results.pkl", "rb")
res = pickle.load(f)
f.close()

b = sorted(res, key=lambda e: check_end(e[1]) - check_start(e[1]))

# The groups that must be included. Must be tuples to have multiple choices.
desired_groups = [
(8085,8086,8082,8081),  # Intro a física cuántica
(8090,8092,8093),       # Lab. de Óptica
(8098, 8100,8101,8102), # Óptica
(4180,4183,4185,4186),  # Variable Compleja
(8124,),                 # Relatividad
]

filtered_options = []

for e in b:
    if groups_valid(e[0], desired_groups):
        filtered_options.append(e)

max_out = 500

if len(filtered_options) > max_out:
    a = max_out
else:
    a = len(filtered_options)
    
gf = GroupFinder()
    
for i in range(0, a):
    e = filtered_options[i]
    
    g_list = []
    for g_id in e[0]:
        g_list.append(gf.groups_dict[g_id])
    g_list.sort(key=lambda group: check_start(group[0].matrix))
    
    for j in g_list:
        gr = j[0]
        print u"{0}: {1}".format(j[1].decode("utf-8"), gr.professors[0]).encode("utf-8")
        
        sched_list = list(set(gr.sched_readable))
        
        for sched in sched_list:
            print u"{0}, {1}".format(
            sched[0], sched[1]).encode("utf-8")
        print gr.classroom
        print
        
    #print
    #print e[1]
    print
    print "### From {0:02d} to {1:02d}".format(check_start(e[1]), check_end(e[1]))
    print
