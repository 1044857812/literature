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
@Author  : ywang (1159455981@qq.com)
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
    parser.add_argument('-d', '--decoded',
                        help='decoded',default="Equus_caballus_decoded.txt", dest='decoded', type=str)
    parser.add_argument('-r', '--ref',
                        help='ref',default="Equus_caballus_raw_text.txt", dest='ref', type=str)
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
    with open(args.decoded,'r') as f1, open("test_predictions.txt",'r') as f2,open(args.ref,'r') as f3,open("token_reocrd.txt",'w') as f4:
        ref_record = []
        index_record = {}
        auto_record = []
        bert_record =[]
        for line in f3:
            line = line.strip()
            ref_record.append(line)
        for line in f1:
            line = line.strip()
            parts = line.split("\t")
            if len(parts)> 1:
                token_type = parts[-1]
                token = parts[2].split(" ")
            else:
                token = ['']
                token_type = 'None'
            for i in token:
                auto_record.append((i,token_type))
        for line in f2:
            line = line.strip()
            parts = line.split(" ")
            if len(parts)> 1:
                if 'gene' in parts[-1]:
                    token_type = 'gene'
                elif 'phenotype' in parts[-1]:
                    token_type = 'phenotype'
                else:
                    token_type = 'None'
            else:
                token_type = 'None'
            bert_record.append((parts[0],token_type))
        print('comparing biobert')
        cursor=0
        index = 0
        for i in range(len(bert_record)):
            print(index)
            token_type = 'None'
            if bert_record[i][0]=='':
                continue
            index = ref_record.index(bert_record[i][0],cursor,cursor+100)
            if bert_record[i][1]=='gene':
                token_type = 'gene'
            elif bert_record[i][1] == 'phenotype':
                token_type = 'phenotype'
            else:
                token_type = 'None'
            index_record[index]=token_type
            cursor = index+1       
        print("comparing auto")
        cursor=0
        index = 0
        for i in range(len(auto_record)):
            token_type = 'None'
            index = ref_record.index(auto_record[i][0],cursor)
            if auto_record[i][1]=='gene':
                token_type = 'gene'
            elif auto_record[i][1] == 'phenotype':
                token_type = 'phenotype'
            else:
                token_type = 'None'
            index_record[index]=token_type
            cursor = index+1
        
        print('wring token_record.txt')
        for i in range(len(ref_record)):
            if i =='':
                f4.write("\n")
            else:
                if i in index_record:
                    f4.write(ref_record[i]+"\t"+index_record[i]+"\n")
                else:
                    f4.write(ref_record[i]+"\t"+"None"+"\n")
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.stderr.write("User interrupt me! ;-) See you!\n")
        sys.exit(0)
