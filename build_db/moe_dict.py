#!/usr/bin/env python3

import json
import re
from pprint import pprint

def moe_dict():
    with open('moe-dict.json') as data_file:    
        moe = json.load(data_file)

    end = r'([-\s\)\*\.\?,\/]|$)'
    conversion = [(r'A3', 'À'), (r'A2', 'Á'), (r'A5', 'Â'), (r'A7', 'Ā'),
                 (r'E3', 'È'), (r'E2', 'É'), (r'E5', 'Ú'), (r'E7', 'Ē'),
                 (r'I3', 'Ì'), (r'I2', 'Í'), (r'I5', 'Î'), (r'I7', 'Ī'),
                 (r'O3', 'Ò'), (r'O2', 'Ó'), (r'O5', 'Ô'), (r'O7', 'Ō'),
                 (r'U3', 'Ù'), (r'U2', 'Ú'), (r'U5', 'Û'), (r'U7', 'Ū'),
                 (r'a3', 'à'), (r'a2', 'á'), (r'a5', 'â'), (r'a7', 'ā'),
                 (r'e3', 'è'), (r'e2', 'é'), (r'e5', 'ê'), (r'e7', 'ē'),
                 (r'i3', 'ì'), (r'i2', 'í'), (r'i5', 'î'), (r'i7', 'ī'),
                 (r'o3', 'ò'), (r'o2', 'ó'), (r'o5', 'ô'), (r'o7', 'ō'),
                 (r'u3', 'ù'), (r'u2', 'ú'), (r'u5', 'û'), (r'u7', 'ū'),
                 (r'2', '\u0301'), (r'3', '\u0300'), (r'5', '\u0302'), 
                 (r'7', '\u0304'), (r'8', '\u030D'), (r'o+', 'oo'), 
                 (r'*\1', r'nn' + end), (r'ch', 'ts'), (r'Ch', 'Ts'),
                 (r'e\1k', 'i([2-8]*)k'), (r'E\1k', 'I([2-8]*)k'),
                 (r'e\1ng', 'i([2-8]*)ng'), (r'E\1ng', 'I([2-8]*)ng'),
                 (r'o\2\1', 'u([2-8]*)([ea])'), (r'O\2\1', 'U([2-8]*)([ea])')]
                 # Note that the tone number is moved in the last two tuples

    moe_list = []

    for i in moe:
        word = re.sub(r'\s?\(...\.\)\s?', r'', i['tailo'])
        english =  i['english'].replace('/', ', ')
        mandarin = i['mandarin']
        taiwanese = i['taiwanese']
        for c in conversion:
            word = re.sub(c[1], c[0], word)
        if english != '': 
            moe_list.append([None, word, mandarin, english, taiwanese])
            
            try:
                for e in i['examples']:
                    word = '::' + re.sub(r'\s?\(...\.\)\s?', r'', e['tailo'])
                    english = ''
                    mandarin = e['mandarin']
                    taiwanese = e['taiwanese']
                    for c in conversion:
                        word = re.sub(c[1], c[0], word)
                    moe_list.append([None, word, mandarin, english, taiwanese])
            except KeyError:
                pass

    return moe_list
