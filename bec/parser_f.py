#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Parser for messages in email attachments. 
# Command line syntax: 'parser.py arg1 arg2' where arg1 is the directory to be parsed,
# and arg2 selects which portion of the text to be viewed (0 for header and 1 for plain version of the content)

import nltk, re, pprint, sys, os
from nltk import word_tokenize

# convert the text to vocabulary
def to_vocab(text):
    return sorted(set(w.lower() for w in text if w.isalpha()))

filename = sys.argv[1]

tokens = word_tokenize(open(filename).read())

mixed = 'multipart/mixed'
alternative = 'multipart/alternative'
ascii = 'us-ascii'
ascii_2 = 'charset=us-ascii'

# check if the message is multipart/mixed
if mixed in tokens: 
    print('MIXED')
    
    boundary_id = tokens[tokens.index(mixed) + 4]

    # locate where boundary_id appeared in the list
    index_list = [ i for i in range(len(tokens)) if tokens[i] == boundary_id ]

    # calculate breakpoint where header and inner contents are separated
    breakpoint = index_list[1] + 1

    header = to_vocab(tokens[:breakpoint])

    inner = tokens[breakpoint:]
    inner_boundary_id = tokens[tokens.index(alternative) + 4]
    inner_index_list = [ i for i in range(len(tokens)) if tokens[i] == inner_boundary_id ]
    inner_breakpoint_1 = inner_index_list[1] + 1
    inner_breakpoint_2 = inner_index_list[2] + 1

    inner_plain = to_vocab(tokens[inner_breakpoint_1:inner_breakpoint_2])
    inner_html = tokens[inner_breakpoint_2:]

    # output the result
    if sys.argv[2] == '0':
        print(header)
    elif sys.argv[2] == '1':
        print(inner_plain)
# check if the message only has alternative part
elif alternative in tokens:
    print('ALTERNATIVE')
    
    boundary_str = tokens[tokens.index(alternative) + 2]
    print(boundary_str)
    
    boundary_id = boundary_str[9:]
    index_list =  [ i for i in range(len(tokens)) if tokens[i] == boundary_id ]

    breakpoint_1 = index_list[0] + 1
    breakpoint_2 = index_list[1] - 2
    
    header = to_vocab(tokens[:breakpoint_1])
    inner_plain = to_vocab(tokens[breakpoint_1:breakpoint_2])
    inner_html = tokens[breakpoint_2:]

    if sys.argv[2] == '0':
        print(header)
    elif sys.argv[2] == '1':
        print(inner_plain)

# check if the message has ascii encoding
elif ascii or ascii_2 in tokens:
    print('ASCII')

    index = tokens.index('MIME-Version') + 3
    content = to_vocab(tokens[index:])

    print(content)
else:
    print('Error: message cannot be parsed.')