#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from operator import truth
import pandas as pd
import numpy as np
import os
import argparse
import re
import string
import nltk
import csv
#####Description####
usage = '''
Author : ywang
Email  : 1159455981@qq.com
Date   : 08:54 042722
Description:
	转换autoner格式
Example:
	python %s [-i abstract_dir]
Step:
	1:
''' % (__file__[__file__.rfind(os.sep) + 1:])
class HelpFormatter(argparse.RawDescriptionHelpFormatter,argparse.ArgumentDefaultsHelpFormatter):
    pass

def generate_raw_text(abs_filename, raw_filename):
    df = open(abs_filename)
    text = []#定义一个空列表，用于存储原有数据文件中的数据
    for line in df:#定义变量line用于实际遍历文件中每行的数据，然后依次将数据添加至列表中
        text.append(line.split('\t'))
    doc =[]
    word_label = []
    for line in text[1:]:

        title_abs = line[2] + ' ' + line[7]
        
        doc.append(title_abs)
        
        abs_replace = title_abs
        sent_text = nltk.sent_tokenize(abs_replace)

        for i in range(len(sent_text)):
        
            piece = re.split(r'([-+()/])', sent_text[i])
            sent_text_re= ''
            
            for p in piece:
                sent_text_re = sent_text_re + ' ' + p 
            sent_text[i] = sent_text_re
            
            words = nltk.word_tokenize(sent_text[i])

            for j in range(len(words)):
                #str1 = words[j] + '\t' + 'O\n'
                str1 = words[j] + '\n'
                word_label.append(str1)
            # word_label.append('\n')
            word_label.append('\n')
  
    with open(raw_filename, 'w') as f:
        for token in word_label:
            f.write(token)
    

if __name__ == "__main__":
    abstract_path = "raw_abstract.txt"
    raw_path = 'raw_text.txt'

    generate_raw_text(abstract_path, raw_path)