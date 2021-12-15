# Application to generate n number of next words
# Andrew Flores
# Subset of ECE528 Final Project FA21
# Last modified: 12/14/21

# ** TODO: Return list < 3 words if not enough matches

import re
import time
import pandas as pd
import json

start_time = time.time()

class TextGeneration(object):
    n_dict = {}
    def __init__(self, ngrams_path):
        with open(ngrams_path, 'r') as inFile:
            self.n_dict = json.load(inFile)

    # Joins list of words into string
    def join_words(self, l):
        result = ''
        for w in l:
            result += w + ' '
        # Return string without trailing spaces
        return result.strip()

    # Find best match first (longest seed match with length >= words.len() + 1)
    # Gets last 3 words of string, or two or one
    def get_last_three(self, str, seed):
        words = str.strip(' ,.()\'\"').split(' ')
        subset = []
        suggestions = []
        # Get 3 suggestions, or stop if looking if no matches
        while len(suggestions) < 3 and seed > 0:
            subset = words[-seed:]
            subset_str = self.join_words(subset)
            for key in self.n_dict:
                if len(suggestions) == 3:
                    break
                if self.n_dict[key] == seed + 1:
                    # if subset is found in the FIRST part of the key
                    if re.search(r'\b' + subset_str + r'\b', key) and key.find(subset_str) == 0:
                        suggestions.append(key.strip())
            seed -= 1
        # Suggestions are formed with original prompt still included
        pared_suggestions = []
        for e in suggestions:
            pared_suggestions.append(e.removeprefix(subset_str).strip())
        return pared_suggestions

# if largest subset of words is noticed in top5000, return next words in sequence
prompt = 'andrew mallory he is she is i will'
seed_length = 4

generate = TextGeneration('everygrams15000_dict.txt')
print(generate.get_last_three(prompt, seed_length))

end_time = time.time()
print(f'Execution time: {1000 * round(end_time - start_time, 8)}ms')
