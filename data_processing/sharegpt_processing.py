import numpy as np
import glob
import os
import json
import spacy
from collections import Counter
import spacy_fastlang
from tqdm import tqdm
nlp = spacy.load('en_core_web_lg')
nlp.add_pipe('language_detector')

TARGET_FOLDER = './data_raw/ShareGPT52K'
SPLITS = ['sg_90k_part1.json', 'sg_90k_part2.json']

def assign_lang(ds_lst):
    for i in tqdm(range(len(ds_lst))):
        language = nlp(ds_lst[i]['conversations'][0]['value'])._.language
        ds_lst[i]['lang'] = language
        
    return ds_lst

def count_num_of_turn(ds_lst):
    counter = list(map(lambda x: len(x['conversations']), ds_lst))
    print(np.histogram(counter, bins=[0, 2,4,8,16, 1000]))

combined_lst = []
for split in SPLITS:
    ds_split = os.path.join(TARGET_FOLDER, split)
    with open(ds_split, 'r') as f:
        data_lst = json.load(f)
    combined_lst += data_lst

print('Total data entries = {}'.format(len(combined_lst)))

processed_ds = assign_lang(combined_lst)

with open('./data/sharegpt/90k_w_lang', 'w') as f:
    json.dump(processed_ds, f)