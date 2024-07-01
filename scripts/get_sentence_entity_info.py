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
import re
#####Description####
usage = '''
Author : ywang
Email  : 1159455981@qq.com
Date   : 07:45 02152022
Description:
	生成句子实体信息
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
def dec2base(dec_numbeer,base=36):
    base_dict=[str(x) for x in range(0,10)]+[chr(x) for x in range(65,91)]
    code=[]
    while True:
        s=dec_numbeer//base#向下取整
        y=dec_numbeer%base#取余数
        code.insert(0,base_dict[y])#insert将对象插入到列表的指定位置，list.insert(index,number),将number插入到list列表的index位置。
        if s==0:
            break
        dec_numbeer=s
    return "".join(code)
def find_all(string, sub):
    start = 0
    pos = []
    while True:
        start = string.find(sub, start)
        if start == -1:
            return pos
        pos.append(start)
        start += len(sub)
def main():
    parser = argparse.ArgumentParser(
        formatter_class=HelpFormatter, description=usage)
    parser.add_argument('-s', '--sentence',
                        help='sentence',default="sentence_with_gene_pheno.txt", dest='sentence', type=str)

    
    args = parser.parse_args()
    output = '2.2sentence_entity_info.txt'
    with open(args.sentence,'r',encoding = 'utf-8') as f1, open(output,'w',encoding = 'utf-8') as f2:
        title = ["sentence_id","entity_id","entity","entity_type","correct","not_an_entity","wrong_border","entity_position"]
        f2.write("\t".join(title)+"\n")
        entity_record = {}
        de_record = {}
        for line in f1:
            line = line.strip()
            if line.startswith("species"):
                continue
            parts = line.split("\t")
            if parts[-1] not in entity_record:
                entity_record[parts[-1]] = []
                de_record[parts[-1]] = []
            ty_1= "\t".join([parts[3],"gene"])
            ty_2 = "\t".join([parts[5],"phenotype"])
            if ty_1 not in de_record[parts[-1]]:
                inddex = find_all(parts[6],parts[3])
                pos = []
                if len(inddex) != 0:
                    for i in range(len(inddex)):
                        pos.append(str(inddex[i]+1)+":"+str(inddex[i]+len(parts[3])))
                entity_record[parts[-1]].append(("\t".join([parts[3],"gene"]),",".join(pos)))
                de_record[parts[-1]].append(ty_1)
            if ty_2 not in de_record[parts[-1]]:
                inddex = find_all(parts[6],parts[5])
                pos = []
                if len(inddex) != 0:
                    for i in range(len(inddex)):
                        pos.append(str(inddex[i]+1)+":"+str(inddex[i]+len(parts[5])))
                entity_record[parts[-1]].append(("\t".join([parts[5],"phenotype"]),",".join(pos)))
                de_record[parts[-1]].append(ty_2)
        for id in entity_record:
            for i in range(0,len(entity_record[id])):
                entity_id = id+str(i+1).rjust(2,"0")
                entity_type = entity_record[id][i][0]
                entity_position = entity_record[id][i][1]
                f2.write(id+"\t"+entity_id+"\t"+entity_type\
                    +"\t"+"0"+"\t"+"0"+"\t"+"0"+"\t"+entity_position+"\n")
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
