#!/usr/bin/python
# -*- coding: utf-8 -*-

import pickle
import numpy
import itertools

class GroupFinder(object):
    def __init__(self):
        f = open("data-08.30.57.pkl", "rb")
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
# DinMedDef
(
8231, # Naumis, 7.5
8232, # Stern, 7.9, talacha
8233, # Málaga, 8.5, recomm
#8235, # Mandujano, 6.5, Louis
8236 # Farias, 8.5
),

# FisAtom
(
8237, # Cabrera, 8.6, aburrido
8238, # Mier-Terán, ?
8239, # Chumin Chen, 8.5
),

# FisStat
(
8241, # Ruiz, 6.9, 2 tareas/semana, puntualidad enferma
8242, # Zepeda, 9.0
8244, # Paredes, 7.2 (tareas != examenes)
),

# LabFisCon I
(
#8245,
#8246,
8247,
#8248,
#8249,
#8250
),

# LabFisCon II
(
8254,
8255,
8256,
8257,
8258
)
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

# For simplicity, print the HTML opening right here
print '''
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">

<html lang="sp">

<head>
<meta http-equiv="content-type" content="text/html; charset=utf-8">

<title>Horarios</title>

<style>
@media all {
    .page-break { display: none; }
}

@media print {
    .page-break { display: block; page-break-before: auto; }
}

.nobreak { 
    page-break-inside:avoid; }


</style>

</head>

<body>
'''

for i in range(0, a):
    e = filtered_options[i]

    g_list = []
    for g_id in e[0]:
        g_list.append(gf.groups_dict[g_id])
    g_list.sort(key=lambda group: check_start(group[0].matrix))

    print '<div class="nobreak">'
    print u"<center><h3>Option {0}</h3></center><br>".format(i)


    for j in g_list:
        gr = j[0]

        print u"<h3><b>{0}</b>: {1}</h3>".format(j[1].decode("utf-8"), ", ".join(gr.professors)).encode("utf-8")

        sched_list = list(set(gr.sched_readable))

        for sched in sched_list:
            print u"{0}, {1}".format(
            sched[0], sched[1]).encode("utf-8")
            print "<br>"
        print u"<b>{0}</b>".format(gr.classroom).encode("utf-8")
        print u"<br>"

    #print
    for linee in e[1]:
    	print linee
    	print "<br>"
    print
    print "<i>From {0:02d} to {1:02d}</i>".format(check_start(e[1]), check_end(e[1]))
    print '<hr></div>'

# And print the HTML closure here as well
print '''
</body>
</html>
'''