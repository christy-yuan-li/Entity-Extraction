#!/usr/bin/python
# -*- coding: utf-8 -*-

from subprocess import call
import glob
import io


def call_stanfardnlp_parse(text):

    inputpath = './text_temp.txt'
    inputfile = io.open(inputpath, 'w', encoding='utf-8')
    inputfile.write(text)
    inputfile.close()

    call(["java", "-cp", "stanford-corenlp-full-2016-10-31/*",  "-Xmx2g",  "edu.stanford.nlp.pipeline.StanfordCoreNLP",
          "-annotators",  "tokenize,ssplit,parse",  "-file", inputpath, "-outputFormat",  "text"])
    outputpath = inputpath + '.out'
    parsed_text = io.open(outputpath, 'r', encoding='utf-8').read()

    return parsed_text





