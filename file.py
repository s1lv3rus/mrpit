import re

with open('words.txt', 'r') as f:
    for line in f:
        for word in re.split("\w+ ", line):
            print(word)
