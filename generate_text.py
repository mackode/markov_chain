#!/usr/bin/python3

from nltk.tokenize import word_tokenize
from collections import deque
import re
import random

re_special=re.compile("^[,.:]$")
re_word=re.compile("^\w+$")

def token_feed(file):
    string = open(file, 'r').read()

    for i in word_tokenize(string):
        if re_special.match(i) or re_word.match(i):
            yield(i)

def tokens_to_text(tokens):
    out=""
    for word in tokens:
        if(not re_special.match(word)):
            out += " "
        out += word
    return out

def window(seq, n):
    it = iter(seq)
    win = deque(
        (next(it, None) for _ in range(n)),
        maxlen=n)
        
    yield win
    append = win.append
    for e in it:
        append(e)
        yield win

def statemap_gen(file):
    statemap={}
    tokens=token_feed(file)
    for state in window(tokens, 4):
        key = list(state)
        value = key.pop()
        key = tuple(key)

        if key in statemap:
            statemap[key].append(value)
        else:
            statemap[key] = [value]
    return statemap

def generate_from(file):
    statemap=statemap_gen(file)
    key=list(random.choice(list(statemap.keys())))
    words_new=list(key)

    for i in range(200):
        if not tuple(key) in statemap:
            continue
        
        next_token = random.choice(statemap[tuple(key)])
        words_new.append(next_token)
        key.append(next_token)
        key.pop(0)

    return tokens_to_text(words_new)

print(generate_from('sample.txt'))