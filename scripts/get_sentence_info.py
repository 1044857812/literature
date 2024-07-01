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
from stat import SF_APPEND
from turtle import title
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
    parser.add_argument('-d', '--geneid', default='Anser_cygnoides_geneid_name.txt',help= 'geneid',dest = 'geneid',type = str)
    parser.add_argument('-a', '--abstract',
                        help='abstract',default="Anser_cygnoides_out_abstract.txt", dest='abstract', type=str)
    parser.add_argument('-g', '--gene',
                        help='gene',default="output/gene_list_match.txt", dest='gene', type=str)
    parser.add_argument('-p', '--pheno',
                        help='pheno',default="output/Anser_cygnoides_pheno.txt", dest='pheno', type=str)
    parser.add_argument('-s', '--species',
                        help='species',default="Anser cygnoides", dest='species', type=str)
    parser.add_argument('-b', '--abb',
                        help='abb',default="ACY", dest='abb', type=str)
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
    f1_list = ['/','?','-','+']
    f2_list = ['{',"[","]","(",">","<"]
    f3_list = ["'",':','}',")"]
    with open(args.abstract,'r') as f1, open('record.txt','r') as f2,open(args.geneid,'r') as f3,open(args.gene,'r') as f4,\
        open(args.pheno,'r') as f5,open("all_sentence_info.txt",'w') as f6:
        f6.write("species"+"\t"+"gene_id"+"\t"+"gene_name"+"\t"+"gene"+"\t"+"trait_ontology"+"\t"+"trait"\
                +"\t"+"sentence"+'\t'+"pubmed_id"+"\t"+"relevant"+"\t"+"irrelevant"+"\t"+"sentence_id"+"\n")
        text = []#定义一个空列表，用于存储原有数据文件中的数据
        for line in f1:#定义变量line用于实际遍历文件中每行的数据，然后依次将数据添加至列表中
            text.append(line.split('\t'))
        gene_record = []
        for line in f3:
            line = line.strip()
            parts = line.split("\t")
            i = (parts[0],parts[1],parts[2])
            gene_record.append(i)
        gene_list = []
        pheno_list = []
        for line in f4:
            line = line.strip()
            gene_list.append(line)
        for line in f5:
            line = line.strip()
            pheno_list.append(line)
        n = 0
        for line in f2:
            line = line.strip()
            if line == '':
                n=0
                continue
            parts = line.split("\t")
            if parts[-2]=='-' or parts[-1]=='-':
                continue
            sentence_gene = parts[-2].split(",")
            sentence_pheno = parts[-1].split(",")
            for g in sentence_gene:
                if g not in gene_list:
                    sentence_gene.remove(g)
                    if '-' in sentence_gene:
                        sentence_gene.remove('-')
            if len(sentence_gene)==0:
                continue
            for p in sentence_pheno:
                if p not in pheno_list:
                    sentence_pheno.remove(p)
                    if '-' in sentence_pheno:
                        sentence_pheno.remove('-')
            if len(sentence_pheno)==0:
                continue
            n+=1
            sentence_id = args.abb+text[int(parts[0])][1].rjust(8,"0")+str(n).rjust(3,"0")
            
            for g in sentence_gene:
                for f in f1_list:
                    if f in g:
                        g = g.replace(" "+f+" ",f)
                for f in f2_list:
                    g = g.replace(f+" ",f)
                for f in f3_list:
                    g = g.replace(" "+f,f)
                        
                geneid = '-'
                gene_name = '-'
                for i in gene_record:
                    if g == i[0]:
                        geneid = i[0]
                        gene_name = i[1]
                    if g == i[1]:
                        geneid = i[0]
                        gene_name = i[2]
                    if g == i[2]:
                        geneid = i[0]
                        gene_name = i[1]
                for p in sentence_pheno:
                    for f in f1_list:
                        if f in p:
                            p = p.replace(" "+f+" ",f)
                        for f in f2_list:
                            p = p.replace(f+" ",f)
                        for f in f3_list:
                            p = p.replace(" "+f,f)
                            
                    f6.write("\t".join([args.species,geneid,gene_name,g,'-',p,parts[2],text[int(parts[0])][1],'0','0',sentence_id])+"\n")
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.stderr.write("User interrupt me! ;-) See you!\n")
        sys.exit(0)
           