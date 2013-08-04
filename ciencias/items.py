#!/usr/bin/python
# -*- coding: utf-8 -*-

from scrapy.item import Item, Field

class CienciasItem(Item):
    # Name of the subject, e.g. "Álgebra lineal"
    subject_name = Field()
    
    # Group number, e.g. 8081
    group_id = Field()
    
    # Subject number, e.g. 100
    subject_id = Field()
    
    # List of the professors
    professors = Field()
    
    # List of the assistants
    assistants = Field()
    
    # Schedule in easy to read form, days = [("lu mi vi", "9-10"), ...]
    sched_readable = Field()
    
    # Classroom
    classroom = Field()
    
    # Schedule matrix
    matrix = Field()
