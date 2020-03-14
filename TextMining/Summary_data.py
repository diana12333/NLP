#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 11:26:57 2020

@author: dianshen
"""


import xml.etree.ElementTree as ET 
import xml.dom.minidom
import numpy as np
import re
from lxml import etree
import glob
import unicodedata as ud
import pandas as pd

latin_letters= {}

def is_latin(uchr):
    try: return latin_letters[uchr]
    except KeyError:
         return latin_letters.setdefault(uchr, 'LATIN' in ud.name(uchr))
def only_roman_chars(unistr):
    if  all(is_latin(uchr)
           for uchr in unistr
           if uchr.isalpha()):
        return re.sub(r"^[0-9a-z]+\.", "", unistr)
    else:
        return ''
content ='./{http://www.tei-c.org/ns/1.0}text/{http://www.tei-c.org/ns/1.0}body/{http://www.tei-c.org/ns/1.0}div/{http://www.tei-c.org/ns/1.0}p'
content ='./{http://www.tei-c.org/ns/1.0}text/{http://www.tei-c.org/ns/1.0}body/{http://www.tei-c.org/ns/1.0}div'
files = glob.glob("/Users/dianshen/Desktop/paper/out_full/*.xml")
contents = []
titles = []
i = 1
for file in files:
    print(i)
    i +=1
    title = []
    con = []
    with open(file,'rb') as fobj:
        lxml = fobj.read()
    root = etree.fromstring(lxml)
    test = root.findall(content)
    for node in test:
        con.append(' '.join([only_roman_chars(str(i).lower()) for i in node.xpath("./*[substring(name(),string-length(name())-4) = 'head']/text()")]))
        #con.append(' '.join(node.xpath("./head")))
        title.append(' '.join(node.xpath("./*[substring(name(),string-length(name())-1) = 'p']/text()|.//*[substring(name(),string-length(name())-1) = 'ref']/text()")).lower())
    contents.append(title)
    titles.append(con)



df = pd.DataFrame()
for i in range(len(titles)):
    content = pd.DataFrame(contents[i])
    title = pd.DataFrame(titles[i])
    ind = pd.DataFrame([i]*(len(titles[i])))
    df_temp = pd.concat([ind, title,content], axis=1)
    df = pd.concat([df, df_temp], axis=0)

df.columns = ['index','sectitle','text']

df['text'].replace('', np.nan, inplace=True)
df.dropna(subset=['text'], inplace=True)

# remove title empty and content empty
# delete void columns for text and background 
# delete not english ones arbaic 
# delete punctuation
# delete the formula can't be tokenized(undone) 
# meaningless title 
# index-sectitle - content 
df.to_csv('output.csv')



 