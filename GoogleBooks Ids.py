#!/usr/bin/env python
# coding: utf-8



import gzip
from glob import glob
from xml.etree.ElementTree import iterparse
import re
import requests
import json
import csv
from datetime import datetime



katalogfiles = glob('*.gz')


def getGBSid(OCLC): 
    try:
        res = requests.get(f"https://opacplus.bsb-muenchen.de/gbs/books?jscmd=viewapi&bibkeys=OCLC:{OCLC}", timeout = 20)
        google_url = list(json.loads(res.text[19:-1]).values())[0].get('info_url')
        google_id = re.search('books.google\S+\?id=(\S+)\&',google_url).group(1)
        return google_id
    except Exception as e:
        print(e,OCLC)
        print(f"[ERR] {datetime.now().isoformat()} {e} {OCLC}", file = LOG)
            
        return "-"



def parseRecord(elem):
    try:
        IDs = elem.findall('{http://www.loc.gov/MARC21/slim}datafield[@tag="035"]/{http://www.loc.gov/MARC21/slim}subfield[@code="a"]')
        tmp = {}
        for x in IDs:
            match = re.match(r'\((?P<pref>[^\)]+)\)(?P<id>\S+)',x.text).groupdict()
            tmp[match.get('pref')] = match.get('id')
        
        
    except Exception as e:
        print(e)
    try:
        yearOfPublication = elem.find('{http://www.loc.gov/MARC21/slim}datafield[@tag="264"]/{http://www.loc.gov/MARC21/slim}subfield[@code="c"]').text
        yearOfPublication = max([int(x) for x in re.findall(r'\d{4}',yearOfPublication)])
    except Exception as e:
        yearOfPublication = None
        
        
    try:
        urns = [x.text for x in elem.findall('{http://www.loc.gov/MARC21/slim}datafield[@tag="776"]/{http://www.loc.gov/MARC21/slim}subfield[@code="o"]')]
    except Exception as e:
        #print(e)
        pass
        
    try:
        resolving_links = [x.text for x in elem.findall('{http://www.loc.gov/MARC21/slim}datafield[@tag="856"]/{http://www.loc.gov/MARC21/slim}subfield[@code="u"]')]
    except Exception as e:
        #print(e)
        pass
    
    if yearOfPublication and yearOfPublication < 1801 and tmp.get('OCoLC') and len(urns) > 0:
        gb_id = getGBSid(tmp.get('OCoLC'))
        output = [tmp.get('OCoLC'),tmp.get('DE-599',""),gb_id]+urns
        print(output)
    
        return output


LOG = open("log.txt", "a")

with open('bvbgbs.csv', 'a', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter='\t')
    for kf in katalogfiles:
        with gzip.open(kf, 'rb') as fileo:
            print(f"[LOG] {datetime.now().isoformat()} open {kf}", file = LOG)
            for _, elem in iterparse(fileo, events=("end",)):
                if elem.tag.endswith("record"):
                    output = parseRecord(elem)
                    if output:
                        writer.writerow(output)
                    elem.clear()
                    
LOG.close()

