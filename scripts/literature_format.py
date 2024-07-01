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
import nltk
import re
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
                        help='abstract',default="raw_abstract.txt", dest='abstract', type=str)
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

    with open(args.abstract,'r') as f1,open('token_reocrd.txt','r') as f2,open("record.txt",'w') as f3,open("gene_list.txt",'w') as f4, open("pheno_list.txt",'w') as f5:
        text = []#定义一个空列表，用于存储原有数据文件中的数据
        for line in f1:#定义变量line用于实际遍历文件中每行的数据，然后依次将数据添加至列表中
            text.append(line.split('\t'))
        token_reocrd=[]
        type_record = []
        for line in f2:
            line = line.strip()
            parts = line.split("\t")
            if len(parts)<2:
                token_reocrd.append("")
                type_record.append("none")
            else:
                token_reocrd.append(parts[0])
                type_record.append(parts[1])
        print(len(token_reocrd))
        f1_list = ['/','?','-','+']
        f2_list = ['{',"[","]","(",">","<"]
        f3_list = ["'",':','}',")"]
        abstract_record = {}
        word_cursor = 0
        gene_list =[]
        pheno_list = []
        for line in text[1:]:
            title_abs = line[2] + ' ' + line[7]
            abstract_record[line[0]] = {}
            abs_replace = title_abs
            sent_text = nltk.sent_tokenize(abs_replace)
            sentence_start = 0
            context_cursor = 0
            for i in range(len(sent_text)):
                for a in sent_text[i]:
                    r = title_abs.find(a,context_cursor)
                    if r > -1:
                        context_cursor = r+len(a)
                    else:
                        pass
                sentence_end = context_cursor
                abstract_record[line[0]][str(sentence_start+1)+":"+str(sentence_end)] = [title_abs[sentence_start:sentence_end+1].strip(),[],[]]
                #f4.write(title_abs[sentence_start:sentence_end+1]+"\n")
                
                piece = re.split(r'([-+()/])', sent_text[i])
                sent_text_re= ''
                for p in piece:
                    sent_text_re = sent_text_re + ' ' + p 
                sent_text[i] = sent_text_re
                words = nltk.word_tokenize(sent_text[i])
                gene_flag = 0
                pheno_flag =0
                gene_temp =''
                pheno_temp =''
                for w in words:
                    pos = token_reocrd.index(w,word_cursor)
                    word_cursor = pos+1
                    if type_record[pos]=='None' or type_record[pos]=='none':
                        #print(pheno_temp)
                        if gene_flag==1:
                            for f in f1_list:
                                gene_temp = gene_temp.replace(" "+f+" ",f)
                            for f in f2_list:
                                gene_temp = gene_temp.replace(f+" ",f)
                            for f in f3_list:
                                gene_temp = gene_temp.replace(" "+f,f)
                            abstract_record[line[0]][str(sentence_start+1)+":"+str(sentence_end)][1].append(gene_temp)
                            gene_list.append(gene_temp)
                            gene_temp =''
                            
                        else:
                            pass
                        if pheno_flag==1:
                            for f in f1_list:
                                pheno_temp = pheno_temp.replace(" "+f+" ",f)
                            for f in f2_list:
                                pheno_temp = pheno_temp.replace(f+" ",f)
                            for f in f3_list:
                                pheno_temp = pheno_temp.replace(" "+f,f)
                            abstract_record[line[0]][str(sentence_start+1)+":"+str(sentence_end)][2].append(pheno_temp)
                            #print(pheno_temp)
                            pheno_list.append(pheno_temp)
                            pheno_temp = ''
                            
                        else:
                            pass
                        gene_flag = 0
                        pheno_flag = 0

                    elif type_record[pos]=='gene':
                        if gene_flag == 1:
                            gene_temp = gene_temp+" "+w
                        else:
                            gene_temp = w
                        gene_flag = 1
                        if pheno_flag== 1:
                            for f in f1_list:
                                pheno_temp = pheno_temp.replace(" "+f+" ",f)
                            for f in f2_list:
                                pheno_temp = pheno_temp.replace(f+" ",f)
                            for f in f3_list:
                                pheno_temp = pheno_temp.replace(" "+f,f)
                            abstract_record[line[0]][str(sentence_start+1)+":"+str(sentence_end)][2].append(pheno_temp)
                            #print(pheno_temp)
                            pheno_list.append(pheno_temp)
                            pheno_temp = ''
                            pheno_flag = 0
                    elif type_record[pos]=='phenotype':
                        if pheno_flag == 1:
                            pheno_temp = pheno_temp+" " + w
                            #print(pheno_temp)
                        else:
                            pheno_temp = w
                        pheno_flag = 1
                        if gene_flag==1:
                            for f in f1_list:
                                gene_temp = gene_temp.replace(" "+f+" ",f)
                            for f in f2_list:
                                gene_temp = gene_temp.replace(f+" ",f)
                            for f in f3_list:
                                gene_temp = gene_temp.replace(" "+f,f)
                            abstract_record[line[0]][str(sentence_start+1)+":"+str(sentence_end)][1].append(gene_temp)
                            gene_list.append(gene_temp)
                            gene_temp =''
                            gene_flag = 0
                    else:
                        print(type_record[pos])
                sentence_start = sentence_end+1 
        for a in abstract_record:
            for p in abstract_record[a]:
                if len(abstract_record[a][p][1])==0:
                    abstract_record[a][p][1].append('-')
                if len(abstract_record[a][p][2])==0:
                    abstract_record[a][p][2].append('-')
                f3.write(a+"\t"+p+'\t'+abstract_record[a][p][0]+"\t"+",".join(abstract_record[a][p][1])+"\t"+",".join(abstract_record[a][p][2])+"\n")
            f3.write("\n")
        gene_list = list(set(gene_list))
        pheno_list = list(set(pheno_list))
        for g in gene_list:
            for f in f1_list:
                g = g.replace(" "+f+" ",f)
            for f in f2_list:
                g = g.replace(f+" ",f)
            for f in f3_list:
                g = g.replace(" "+f,f)
            f4.write(g+"\n")
        for p in pheno_list:
            for f in f1_list:
                p = p.replace(" "+f+" ",f)
            for f in f2_list:
                p = p.replace(f+" ",f)
            for f in f3_list:
                p = p.replace(" "+f,f)
            f5.write(p+"\n")
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.stderr.write("User interrupt me! ;-) See you!\n")
        sys.exit(0)
