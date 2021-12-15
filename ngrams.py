# Application to generate n number of next words
# Andrew Flores
# Subset of ECE528 Final Project FA21
# Last modified: 12/14/21

import re
import time
import pandas as pd
import json

start_time = time.time()

# File formatted with {word: key, word2: key, ...}
with open('everygrams5000_dict.txt', 'r') as inFile:
    n_dict = json.load(inFile)

# Joins list of words into string
def join_words(l):
    result = ''
    for w in l:
        result += w + ' '
    # Return string without trailing spaces
    return result.strip()


# Gets last 3 words of string, or two or one
def get_last_three(str, seed):
    words = str.strip(' ,.()\'\"').split(' ')
    length = len(words)
    subset = []
    # Truncate phrase to look at 'seed' number of words, and initialize subset list
    if length >= seed:
        subset = words[-seed:]
    elif length == 0:
        return [key.strip() for key in n_dict[:3]]
    else:
        subset = words

    subset_str = join_words(subset)
    # If subset is in a dict key, missing a word
    suggestions = []
    # Search for 3 suggestions
    offset_length = 0
    # Get 3 suggestions, or stop if looking for 
    while len(suggestions) < 3 and length + offset_length <= 7:
        offset_length += 1
        for key in n_dict:
            if len(suggestions) == 3:
                break
            if n_dict[key] == length + offset_length:
                # if subset is found in the FIRST part of the key
                if re.search(r'\b' + subset_str + r'\b', key) and key.find(subset_str) == 0:
                    suggestions.append(key.strip())

    # Suggestions are formed with original prompt still included
    pared_suggestions = []
    for e in suggestions:
        pared_suggestions.append(e.removeprefix(subset_str).strip())
    return pared_suggestions
    


# if largest subset of words is noticed in top5000, return next words in sequence
prompt = 'if you are '
seed_length = 5
print(get_last_three(prompt, seed_length))

end_time = time.time()
print(f'Execution time: {1000 * round(end_time - start_time, 8)}ms')
