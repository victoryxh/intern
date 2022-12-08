#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Parser for messages in email attachments. Individual file version. 
# Command line syntax: 'parser.py arg1 arg2' where arg1 is the file to be parsed,
# and arg2 selects which portion of the text to be viewed (0 for header and 1 for plain version of the content)

import nltk, re, pprint, sys, os
from nltk import word_tokenize

# convert the text to vocabulary
def to_vocab(text):
    return sorted(set(w.lower() for w in text if w.isalpha()))

filename = sys.argv[1]

tokens = word_tokenize(open(filename).read())

# message type identifier
mixed = 'multipart/mixed'
alternative = 'multipart/alternative'
ascii = 'us-ascii'
ascii_2 = 'charset=us-ascii'

# check if the message is multipart/mixed
if mixed in tokens: 
    print('MIXED')
    
    # type-specific way of determining boundary_id
    boundary_id = tokens[tokens.index(mixed) + 4]

    # locate where boundary_id appear in the list
    index_list = [ i for i in range(len(tokens)) if tokens[i] == boundary_id ]

    # calculate breakpoint where header and inner contents are separated
    breakpoint = index_list[1] + 1
    inner = tokens[breakpoint:]
    inner_boundary_id = tokens[tokens.index(alternative) + 4]
    inner_index_list = [ i for i in range(len(tokens)) if tokens[i] == inner_boundary_id ]
    inner_breakpoint_1 = inner_index_list[1] + 1
    inner_breakpoint_2 = inner_index_list[2] + 1

    # get header as vocabulary
    header = to_vocab(tokens[:breakpoint])

    # get inner plain content as vocabulary
    inner_plain = to_vocab(tokens[inner_breakpoint_1:inner_breakpoint_2])

    # get inner html (not used)
    inner_html = tokens[inner_breakpoint_2:]

    # output the result
    if sys.argv[2] == '0':
        print(header)
    elif sys.argv[2] == '1':
        print(inner_plain)
# check if the message only has alternative part
elif alternative in tokens:
    # print('ALTERNATIVE')
    
    # type-specific way of determining boundary_id
    boundary_id = tokens[tokens.index(alternative) + 4]

    # locate where boundary_id appear in the list
    index_list =  [ i for i in range(len(tokens)) if tokens[i] == boundary_id ]

    # calculate breakpoints where contents are separated
    breakpoint = index_list[0] + 5
    inner_breakpoint_1 = index_list[1] + 1
    inner_breakpoint_2 = index_list[2] + 1
    
    # get header as vocabulary  
    header = to_vocab(tokens[:breakpoint])

    # get inner plain content as vocabulary
    inner_plain = to_vocab(tokens[inner_breakpoint_1:inner_breakpoint_2])

    # get inner html (not used)
    inner_html = tokens[inner_breakpoint_2:]

    # output the result
    if sys.argv[2] == '0':
        print(header)
    elif sys.argv[2] == '1':
        print(inner_plain)
# check if the message has ascii encoding
elif ascii or ascii_2 in tokens:
    # print('ASCII')

    # locate content (there's no header since the message is not multipart)
    index = tokens.index('MIME-Version') + 3
    content = to_vocab(tokens[index:])

    # output the result
    print(content)
else:
    print('Error: message cannot be parsed.')