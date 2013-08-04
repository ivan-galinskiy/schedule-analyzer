import urlparse
import re

from scrapy import log

from scrapy.spider import BaseSpider
from scrapy.http import FormRequest,Request
from scrapy.selector import HtmlXPathSelector
from scrapy.utils.response import get_base_url

from ciencias.items import CienciasItem
from ciencias.sched import *

import getpass

class CienciasSpider(BaseSpider):
    name = "ciencias"
    start_urls = ["https://web.fciencias.unam.mx/acceder"]
    
    def parse(self, response):
        return [FormRequest.from_response(response,
                    formdata={'username': str(raw_input("Username: ")), 
                    'password': getpass.getpass()},
                    callback=self.after_login)]
                    
    def after_login(self, response):
        if "incorrecta" in response.body:
            self.log("Login failed", level=log.ERROR)
            return
         
        #Physics   
        return Request("https://web.fciencias.unam.mx/docencia/horarios/indiceplan/20141/1081",
        callback=self.retrieve_subjects)
        
    def retrieve_subjects(self, response):
        base_url = get_base_url(response)
        hxs = HtmlXPathSelector(response)
        subjects = hxs.select(
        '//a[contains(./text(), "grupos") or contains(./text(), "un grupo")]')
        
        for subject in subjects:
            rel_url = subject.select("./@href")[0].extract()
            abs_url = urlparse.urljoin(base_url, rel_url)
            
            subj_name_full = subject.select("./text()")[0].extract()
            subj_name = u",".join(subj_name_full.split(",")[:-1])
            
            req = Request(abs_url, callback=self.retrieve_groups)
            req.meta["subject_name"] = subj_name.encode("utf-8").strip()
            
            yield req
            
    def retrieve_groups(self, response):
        hxs = HtmlXPathSelector(response)
        group_titles = hxs.select('//strong[contains(./text(), "Grupo")]')
        
        for group in group_titles:
            item = CienciasItem()
            num = re.search('Grupo (\d+)', 
                group.select('./text()').extract()[0]).group(1)
            
            item['group_id'] = int(num)
            item['subject_id'] = int(response.url.split('/')[-1])
            item['subject_name'] = response.meta["subject_name"]
            item['professors'] = []
            item['assistants'] = []
            item['matrix'] = sched_matr("","")
            item['sched_readable'] = []
            
            table = group.select(
            './parent::div[1]/following-sibling::table[1]')[0]
            
            rows = table.select('./tr')
            for row in rows:
                cols = row.select('./td')
                
                try:
                    prof_col = cols[0].select('./text()')[0].extract()
                    name_col = cols[1].select('./a/text()')[0].extract()
                    
                    if "Profesor" in prof_col or "Laboratorio" in prof_col:
                        item['professors'].append(name_col.strip())
                    elif "Ayud" in prof_col:
                        item['assistants'].append(name_col.strip())
                except IndexError:
                    pass
                    
                if len(cols) in range(3,5):
                    a = 0
                elif len(cols) == 5:
                    c = cols[-1].select('./a/text()')[0].extract()
                    item['classroom'] = c
                    a = -1
                else:
                    break
                    
                try:
                    days = cols[a-2].select('./text()')[0].extract().strip()
                    #print days.encode("utf-8")
                    hours = cols[a-1].select('./text()')[0].extract().strip()
                except IndexError:
                    print "!!!!!!!!!!!!!!Exception occured"
                    print item["subject_name"]
                    print item["professors"]
                #print hours
                item['matrix'] += sched_matr(days, hours)
                
                item['sched_readable'].append((days, hours))

            item['matrix'] = normalize_sched_matr(item['matrix'])
            #print item['group_id']
            #print item['subject_id']
            #print item['subject_name']
            #print item['matrix']
            #print
            
            yield item