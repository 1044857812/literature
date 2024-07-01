from stat import SF_APPEND
from turtle import title
# -*- coding: utf-8 -*-
# python >= 2.7


#####Import Module#####
import logging
import sys
import os
import math
import time
import argparse
import glob
import re
from functools import wraps

#####Description####
usage = '''
@Date    : 2022-06-24 16:07:16
@Author  : Your Name (you@example.org)
@Link    : http://example.org
@Version : $Id$
Description:

Example:
    python {} [-i input] [-o output]
Step:

'''.format(__file__[__file__.rfind(os.sep) + 1:])


#####decorator#####
def timeit(function):
    '''
    用装饰器实现函数计时
    :param function: 需要计时的函数
    :return: None
    '''
    @wraps(function)
    def function_timer(*args, **kwargs):
        print('[Function: {name} start...]'.format(name = function.__name__))
        t0 = time.time()
        result = function(*args, **kwargs)
        t1 = time.time()
        print('[Function: {name} finished, spent time: {time:.2f}s]'.format(name = function.__name__,time = t1 - t0))
        return result
    return function_timer
#####HelpFormat#####
class HelpFormatter(argparse.RawDescriptionHelpFormatter, argparse.ArgumentDefaultsHelpFormatter):
    pass


def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=HelpFormatter, description=usage)
    parser.add_argument('-v', '--verbose', help='verbosely print information. -vv for printing debug information',
                        action="count", default=0)
    parser.add_argument('-a', '--abstract',
                        help='abstract',default="Anser_cygnoides_out_abstract.txt", dest='abstract', type=str)
    parser.add_argument('-g', '--gene',
                        help='gene',default="output/gene_list_match.txt", dest='gene', type=str)
    parser.add_argument('-p', '--pheno',
                        help='pheno',default="output/Anser_cygnoides_pheno.txt", dest='pheno', type=str)
    args = parser.parse_args()
    
    # logging level
    if args.verbose >= 2:
        level = logging.DEBUG
    elif args.verbose == 1:
        level = logging.INFO
    else:
        level = logging.WARNING
    logging.basicConfig(level=level, format='%(asctime)s [line:%(lineno)d][%(levelname)s:] %(message)s',
                        datefmt='%Y-%m-%d  %H:%M:%S'
                        )
    return args


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
@timeit
def main():
    args = parse_args()
    with open(args.abstract,'r') as f1, open('record.txt','r') as f2,open('3.2abstract_entity_info.txt','w') as f3,\
        open(args.gene,'r') as f4,open(args.pheno,'r') as f5:
        text = []#定义一个空列表，用于存储原有数据文件中的数据
        for line in f1:#定义变量line用于实际遍历文件中每行的数据，然后依次将数据添加至列表中
            text.append(line.split('\t'))
        title_flag =1
        entity_record = {}
        gene_list = []
        pheno_list = []
        for line in f4:
            line = line.strip()
            gene_list.append(line)
        for line in f5:
            line = line.strip()
            pheno_list.append(line)
        f3.write("\t".join(['pumedid','entity_id','entity','entity_type','correct','not_an_entity','wrong_border','entity_position'])+"\n")
        for line in f2:
            line = line.strip()
            if line == '':
                n = 0
                for e in entity_record:
                    n+=1
                    entity_id =dec2base(n).rjust(3,"0")
                    f3.write("\t".join([text[int(parts[0])][1],entity_id,e,"0","0","0",",".join(entity_record[e])])+"\n")
                title_flag =1
                entity_record = {}
                continue
            parts = line.split("\t")
            if title_flag==1:
                ab_index = parts[0]
                title_flag =0
                title_lenth = len(text[int(parts[0])][2])
                if len(parts[2])==title_lenth:
                    cat_flag = 0
                elif len(parts[2])<title_lenth:
                    cat_flag = 1
                    print('cat1:' +parts[0])
                else:
                    cat_flag = 2
                    print('cat2:' +parts[0])
            else:
                gene=[]
                pheno = []
                if cat_flag ==0:
                    if parts[3]!='-':
                        gene= parts[3].split(",")
                    else:
                        pass
                    if parts[4]!='-':
                        pheno = parts[4].split(",")
                    else:
                        pass
                    if len(gene)!=0:
                        for g in gene:
                            if g not in gene_list:
                                continue
                            entity_name = g+"\t"+'gene'
                            if entity_name not in entity_record:
                                entity_record[entity_name]=[]
                            index = find_all(parts[2],g)
                            if len(index)==0:
                                del entity_record[entity_name]
                                continue
                            entity_pos = []
                            for i in range(len(index)):
                                sentence_start = int(parts[1].split(":")[0])
                                entity_start = sentence_start+index[i]-title_lenth-1
                                entity_end = entity_start+len(g)-1
                                e_pos = str(entity_start)+":"+str(entity_end)
                                entity_pos.append(e_pos)
                            entity_record[entity_name].append(",".join(entity_pos))
                            
                            
                            #f3.write("\t".join([text[int(parts[0])][1],entity_id,g,"gene","0","0","0",",".join(entity_pos)])+"\n")
                    if len(pheno)!=0:
                        for p in pheno:
                            if p not in pheno_list:
                                continue
                            entity_name = p+"\t"+'phenotype'
                            if entity_name not in entity_record:
                                entity_record[entity_name]=[]
                            index = find_all(parts[2],p)
                            if len(index)==0:
                                del entity_record[entity_name]
                                continue
                            entity_pos = []
                            for i in range(len(index)):
                                sentence_start = int(parts[1].split(":")[0])
                                entity_start = sentence_start+index[i]-title_lenth-1
                                entity_end = entity_start+len(p)-1
                                e_pos = str(entity_start)+":"+str(entity_end)
                                entity_pos.append(e_pos)
                            entity_record[entity_name].append(",".join(entity_pos))
                            
                            #f3.write("\t".join([text[int(parts[0])][1],entity_id,p,"phenotype","0","0","0",",".join(entity_pos)])+"\n")
                    else:
                        pass
                if cat_flag==1:
                    head_line_length = int(parts[1].split(":")[1])
                    if head_line_length<=title_lenth:
                        continue
                    if parts[3]!='-':
                        gene= parts[3].split(",")
                    else:
                        pass
                    if parts[4]!='-':
                        pheno = parts[4].split(",")
                    else:
                        pass
                    if len(gene)!=0:
                        for g in gene:
                            if g not in parts[2]:
                                continue
                            if g not in gene_list:
                                continue
                            entity_name = g+"\t"+'gene'
                            if entity_name not in entity_record:
                                entity_record[entity_name]=[]
                            index = find_all(parts[2],g)
                            if len(index)==0:
                                del entity_record[entity_name]
                                continue
                            entity_pos = []
                            for i in range(len(index)):
                                sentence_start = int(parts[1].split(":")[0])-title_lenth-2
                                entity_start = sentence_start+index[i]
                                entity_end = entity_start+len(g)-1
                                e_pos = str(entity_start)+":"+str(entity_end)
                                entity_pos.append(e_pos)
                            entity_record[entity_name].append(",".join(entity_pos))
                            
                            #f3.write("\t".join([text[int(parts[0])][1],entity_id,g,"gene","0","0","0",",".join(entity_pos)])+"\n")
                    if len(pheno)!=0:
                        for p in pheno:
                            if p not in parts[2]:
                                continue
                            if p not in pheno_list:
                                continue
                            entity_name = p+"\t"+'phenotype'
                            if entity_name not in entity_record:
                                entity_record[entity_name]=[]
                            index = find_all(parts[2],p)
                            if len(index)==0:
                                del entity_record[entity_name]
                                continue
                            entity_pos = []
                            for i in range(len(index)):
                                sentence_start = int(parts[1].split(":")[0])-title_lenth-1
                                entity_start = sentence_start+index[i]
                                entity_end = entity_start+len(p)-1
                                e_pos = str(entity_start)+":"+str(entity_end)
                                entity_pos.append(e_pos)
                            entity_record[entity_name].append(",".join(entity_pos))
                            
                            #f3.write("\t".join([text[int(parts[0])][1],entity_id,p,"phenotype","0","0","0",",".join(entity_pos)])+"\n")
                    else:
                        pass
                if cat_flag == 2:
                    if parts[3]!='-':
                        gene= parts[3].split(",")
                    else:
                        pass
                    if parts[4]!='-':
                        pheno = parts[4].split(",")
                    else:
                        pass
                    if len(gene)!=0:
                        for g in gene:
                            if g not in gene_list:
                                continue
                            entity_name = g+"\t"+'gene'
                            if entity_name not in entity_record:
                                entity_record[entity_name]=[]
                            index = find_all(parts[2],g)
                            if len(index)==0:
                                del entity_record[entity_name]
                                continue
                            entity_pos = []
                            for i in range(len(index)):
                                sentence_start = int(parts[1].split(":")[0])
                                entity_start = sentence_start+index[i]-title_lenth-1
                                entity_end = entity_start+len(g)-2
                                e_pos = str(entity_start)+":"+str(entity_end)
                                entity_pos.append(e_pos)
                            entity_record[entity_name].append(",".join(entity_pos))
                            
                            #f3.write("\t".join([text[int(parts[0])][1],entity_id,g,"gene","0","0","0",",".join(entity_pos)])+"\n")
                    if len(pheno)!=0:
                        for p in pheno:
                            if p not in pheno_list:
                                continue
                            entity_name = p+"\t"+'phenotype'
                            if entity_name not in entity_record:
                                entity_record[entity_name]=[]
                            index = find_all(parts[2],p)
                            if len(index)==0:
                                del entity_record[entity_name]
                                continue
                            entity_pos = []
                            for i in range(len(index)):
                                sentence_start = int(parts[1].split(":")[0])
                                entity_start = sentence_start+index[i]-title_lenth
                                entity_end = entity_start+len(p)-1
                                e_pos = str(entity_start)+":"+str(entity_end)
                                entity_pos.append(e_pos)
                            entity_record[entity_name].append(",".join(entity_pos))
                            
                            #f3.write("\t".join([text[int(parts[0])][1],entity_id,p,"phenotype","0","0","0",",".join(entity_pos)])+"\n")
                    else:
                        pass
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.stderr.write("User interrupt me! ;-) See you!\n")
        sys.exit(0)
           