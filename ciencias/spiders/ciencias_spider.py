#!/usr/bin/python
# -*- coding: utf-8 -*-

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
        return Request("https://web.fciencias.unam.mx/docencia/horarios/indiceplan/20162/1081",
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
            item['classroom'] = ""
            
            table = group.select(
            './parent::div[1]/following-sibling::table[1]')[0]
            
            rows = table.select('./tr')
            for row in rows:
                cols = row.select('./td')
               
                days = ""
                hours = ""
                
                for col in cols:
                    if col.select('./text()'):
                        col_text = col.select('./text()')[0].extract()
                    else:
                        col_text = u" ".join(col.select('./node()').extract())
                    
                    col_num = cols.index(col)
                    
                    
                    if re.search("profesor|laboratorio", col_text, \
                    re.IGNORECASE) and not col.select('./a'):
                        try:
                            name = cols[col_num+1].select('./a/text()')[0].extract()
                        except IndexError:
                            name = ""
                        item['professors'].append(name.strip())
                    elif re.search("ayud", col_text, \
                    re.IGNORECASE) and not col.select('./a'):
                        try:
                            name = cols[col_num+1].select('./a/text()')[0].extract()
                        except IndexError:
                            name = ""
                        item['assistants'].append(name.strip())
                    elif re.search(u"(?:^|\-|\s)(lu|ma|mi|ju|vi|sá)(?:$|\-|\s)",
                    col_text):
                        days = col_text.strip()
                    elif re.search("[\d:]+ a [\d:]+", col_text):
                        hours = col_text.strip()
                    #elif col.select('./a') and col_num == len(cols)-1:
                        #clrm = col.select('./a/text()')[0].extract()
                        #item['classroom'] += " " + clrm
                    else:
                        pass
                
                if days and hours:
                    item['sched_readable'].append((days, hours))
                item['matrix'] += sched_matr(days, hours)

            item['matrix'] = normalize_sched_matr(item['matrix'])
            
            yield item
