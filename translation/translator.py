import sys
import json
from tqdm import tqdm
import googletrans
import fire
import multiprocessing as mp

translator=googletrans.Translator()
import time

def translate_entry(args):
    entry, target = args
    success = False
    new_entry = None
    retry_count = 0
    while not success and retry_count < 10:
        try:
            new_entry = {}
            for key in entry.keys():
                if len(entry[key]) == 0 or not entry[key]:
                    new_entry[key] = entry[key]
                else:
                    new_entry[key] = translator.translate(entry[key], dest=target).text
            success = True
        except Exception as e:
            time.sleep(1)
            success=False
            retry_count += 1
    if not success:
        raise Exception('Cannot translate {} after retrying'.format(entry))

    return new_entry

def translate(source, target_lang, output_path, num_workers=4):
    with open(source, 'r') as f:
        ds = json.load(f)

    translated = []
    params = []
    for entry in alpaca_ds:
        params.append((entry, target_lang))
    
    with mp.Pool(num_workers) as p:
        results = list(tqdm(p.imap(translate_entry, params), total=len(params)))
    
    translated = results
    assert len(translated) == len(ds)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(translated, f, indent=1, ensure_ascii=False)

if __name__ == '__main__':
    fire.Fire(translate)