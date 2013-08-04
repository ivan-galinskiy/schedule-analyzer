#!/usr/bin/python
# -*- coding: utf-8 -*-

import pickle
import numpy
import itertools

# Check if matrix doesn't have values greater than 1
def matrix_valid(matrix):
    for e in matrix.flat:
        if e > 1: return False
    return True


f = open("data-22.50.13.pkl", "rb")
subj_dict = pickle.load(f)
f.close()

desired_subjects = [
582, 
583, 
584,
840, 
718
]

subjects = [subj_dict[i] for i in desired_subjects]
     
# Preprocess the matrices
for subject in subjects:
    for group in subject.groups:
        group.matrix = numpy.array(group.matrix, dtype=numpy.int8)
        
group_options = [subject.groups for subject in subjects]

# The possible choices of groups
possible_groups = []

# Now check all the possible combinations
a = 0
for comb in itertools.product(*group_options):
    matrix_result = numpy.zeros(group.matrix.shape)
    for group in comb:
        matrix_result += group.matrix
        
    if matrix_valid(matrix_result): 
        possible_groups.append(([g.n_id for g in comb], matrix_result))
    
    print a
    
    a += 1
    
res_f = open("results.pkl", "wb")
pickle.dump(possible_groups, res_f)
res_f.close()
