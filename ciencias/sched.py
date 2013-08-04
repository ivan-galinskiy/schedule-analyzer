#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import numpy

def sched_matr(days, hours):
    days_templ = ["lu", "ma", "mi", "ju", "vi", u"sá"]
    
    days_array = [0 for day in range(0,6)]
    hours_array = [0 for hour in range(7, 23)]
    
    if days and hours:
        if " a " in days:
            init_day,last_day = re.search("(.+) a (.+)", days).group(1, 2)
            for i in range(days_templ.index(init_day), days_templ.index(last_day)+1):
                days_array[i] = 1
        
        else:
            for day in days.split(" "):
                if day in days_templ:
                    days_array[days_templ.index(day)] = 1
                    
        init_hour,last_hour = re.search("(.+) a (.+)", hours).group(1, 2)
        
        if ":" in init_hour: init_hour = init_hour.split(":")[0]
        if ":" in last_hour: last_hour = int(last_hour.split(":")[0])+1
        
        for i in range(int(init_hour)-7, int(last_hour)-7):
            hours_array[i] = 1
        
    sched_array = numpy.zeros((len(hours_array),len(days_array)), dtype=numpy.int8)
    for a in range(0, len(hours_array)):
        for b in range(0, len(days_array)):
            sched_array[a, b] = hours_array[a]*days_array[b]
            
    return sched_array
    
def normalize_sched_matr(matr):
    a,b = matr.shape
    
    for i in range(0,a):
        for j in range(0, b):
            if matr[i, j]:
                matr[i, j] = 1
    return matr
