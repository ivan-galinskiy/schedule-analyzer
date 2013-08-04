import pickle
from time import gmtime, strftime

from scrapy import signals

class Subject(object):
    def __init__(self):
        self.n_id = 0
        self.subject_name = ""
        self.groups = []

class Group(object):
    def __init__(self):
        self.n_id = 0
        self.professors = []
        self.assistants = []
        self.matrix = []
        self.sched_readable = ()
        self.classroom = ""

class CienciasPipeline(object):
    def __init__(self):
        self.subjects_dict = {}
    
    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline
    
    def process_item(self, item, spider):
        sid = item["subject_id"]
        if sid not in self.subjects_dict:
            subj = Subject()
            subj.n_id = sid
            subj.subject_name = item["subject_name"]
            
            self.subjects_dict[sid] = subj
        
        group = Group()
        group.n_id = item["group_id"]
        group.professors = item["professors"]
        group.assistants = item["assistants"]
        group.matrix = item["matrix"].tolist()
        group.sched_readable = item["sched_readable"]
        group.classroom = item["classroom"]
        
        self.subjects_dict[sid].groups.append(group)
        
        print len(self.subjects_dict[sid].groups)
        
        return item

    def spider_opened(self, spider):
        return
        
    def spider_closed(self, spider):
        filename = "data-{0}.pkl".format(strftime("%H.%M.%S", gmtime()))
        f = open(filename, "wb")
        pickle.dump(self.subjects_dict, f)
        f.close()
        
        return
