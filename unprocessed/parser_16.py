#!/usr/bin/env python
# -*- coding: utf-8 -*- 
#
# Parser for messages in email attachments. Individual file version. 
# Command line syntax: 'parser.py arg1 arg2' where arg1 is the file to be parsed,
# and arg2 selects which portion of the text to be viewed (0 for header and 1 for plain version of the content)
# This version of the parser is built specifically for f16.txt in the unprocessed folder.

import nltk, re, pprint, sys, os
from nltk import word_tokenize

# convert the text to vocabulary
def to_vocab(text):
    return sorted(set(w.lower() for w in text if w.isalpha()))

filename = sys.argv[1]

tokens = word_tokenize(open(filename).read())

# get header as vocabulary
header = to_vocab(tokens[:1340])

# get inner plain content as vocabulary
inner = to_vocab(tokens[1359:2099])

# output the result
print(inner)