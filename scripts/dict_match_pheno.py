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
import Levenshtein

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

def similar_lvst_ratio(str1, str2):#
    return Levenshtein.ratio(str1, str2)
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
#####HelpFormat#####
class HelpFormatter(argparse.RawDescriptionHelpFormatter, argparse.ArgumentDefaultsHelpFormatter):
    pass


def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=HelpFormatter, description=usage)
    parser.add_argument('-v', '--verbose', help='verbosely print information. -vv for printing debug information',
                        action="count", default=0)
    parser.add_argument('-p', '--pheno',
                        help='pheno',default="x00.txt", dest='pheno', type=str)
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

@timeit
def main():
    args = parse_args()
    
    print("filtering pheno")
    output= "output/"+os.path.basename(args.pheno).split(".")[0]+'_match.txt'
    with open("/data4/ywang/literate/dict/all_phenotype.txt",'rb') as f1,open(args.pheno,'r') as f2,open(output,'w') as f3:
        all_pheno_entity_list = {}
        for line in f2:
            line = line.strip()
            parts = line.split(" ")
            for e in parts:
                if e not in all_pheno_entity_list:
                    all_pheno_entity_list[e] = []
                all_pheno_entity_list[e].append(line)

        pheno_list = []
        dict_pheno_entity_list = []
        
        for line in f1:
            line = line.decode().strip()
            parts1 = line.split("\t")
            dict_entity = parts1[1].split(" ")
            for d in dict_entity:
                dict_pheno_entity_list.append(d)
            pheno_list.append(parts1[1])
        e_need_del=[]
        for e in all_pheno_entity_list:
            if e in dict_pheno_entity_list:
                continue
            else:
                e_need_del.append(e)
        for e in e_need_del:
            del all_pheno_entity_list[e]
        all_pheno_list = []
        for e in all_pheno_entity_list:
            all_pheno_list=all_pheno_list+all_pheno_entity_list[e]
        all_pheno_list= list(set(all_pheno_list))

        for g in all_pheno_list:
            ratio1 = 0
            for pheno_name in pheno_list:
                ratio = similar_lvst_ratio(g, pheno_name)
                if ratio>ratio1:
                    ratio1 = ratio
                if ratio1 ==1:
                    break
            g_parts = g.split(" ")
            if len(g_parts) == 1:
                if float(ratio1)<0.9:
                    continue
                else:
                    f3.write(g+"\n")
            else:
                if float(ratio1)<0.4:
                    continue
                else:
                    f3.write(g+"\n")
            



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.stderr.write("User interrupt me! ;-) See you!\n")
        sys.exit(0)
