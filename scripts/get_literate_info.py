#!/usr/bin/env python
# -*- coding: utf-8 -*-

#####Import Module#####
import logging
import sys
import os
import math
import time
import argparse
import glob
#####Description####
usage = '''
Author : ywang
Email  : 1159455981@qq.com
Date   : 07:45 02152022
Description:
	生成文献信息
Example:
	python %s [-i fai]
Step:
	1:
''' % (__file__[__file__.rfind(os.sep) + 1:])


#####HelpFormat#####
class HelpFormatter(argparse.RawDescriptionHelpFormatter, argparse.ArgumentDefaultsHelpFormatter):
    pass

def show_info(text):
    now_time = time.time()
    logging.info(text)
    return now_time

def fmt_time(spend_time):
    spend_time = int(spend_time)
    day = 24 * 60 * 60
    hour = 60 * 60
    min = 60
    if spend_time < 60:
        return "%ds" % math.ceil(spend_time)
    elif spend_time > day:
        days = divmod(spend_time, day)
        return "%dd%s" % (int(days[0]), fmt_time(days[1]))
    elif spend_time > hour:
        hours = divmod(spend_time, hour)
        return '%dh%s' % (int(hours[0]), fmt_time(hours[1]))
    else:
        mins = divmod(spend_time, min)
        return "%dm%ds" % (int(mins[0]), math.ceil(mins[1]))

def main():
    parser = argparse.ArgumentParser(
        formatter_class=HelpFormatter, description=usage)
    parser.add_argument('-a', '--abstract',
                        help='abstract',default="Ailuropoda_melanoleuca_out_abstract.txt", dest='abstract', type=str)
    parser.add_argument('-s', '--species',
                        help='species',default="Ailuropoda melanoleuca", dest='species', type=str)  
    args = parser.parse_args()
    with open(args.abstract,'r') as f1, open("3.1literature.txt",'w') as f2:
        f2.write("pubmedid"+"\t"+"title"+"\t"+"journal"+"\t"+"author"+"\t"+"species"+"\t"+"abstract"+"\n")
        for line in f1:
            line = line.strip()
            if line.startswith("ID"):
                continue
            parts = line.split("\t")
            if len(parts) !=8:
                continue
            f2.write(parts[1]+"\t"+parts[2]+"\t"+parts[4]+"\t"+parts[3]+"\t"+args.species+"\t"+parts[7]+"\n")
if __name__ == '__main__':
    try:
        t1 = time.time()
        time1 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t1))
        print ('Start at :' + str(time1))

        main()
        t2 = time.time()
        time2 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t2))
        print ('End at :' + str(time2))
        t3 = t2 - t1
        print ('Spend time :' + str(t3))
    except KeyboardInterrupt:
        sys.stderr.write("User interrupt me! ;-) See you!\n")
        sys.exit(0)
