import json
from collections import Counter

DATA_FILE='./data/sharegpt/90k_w_lang.json'

with open(DATA_FILE, 'r') as f:
    data = json.load(f)

lang_lst = list(map(lambda x: x['lang'], data)) 

counter = Counter(lang_lst)

print(counter)
