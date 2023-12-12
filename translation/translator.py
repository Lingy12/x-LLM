import sys
import json
from tqdm import tqdm
import googletrans
import fire
import multiprocessing as mp

translator=googletrans.Translator()
import time

def unpack_translation(translate_result): 
    if isinstance(translate_result, list):
        return list(map(lambda x: x.text, translate_result))
    else:
        return translate_result.text

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
                    new_entry[key] = unpack_translation(translator.translate(entry[key], dest=target))
            success = True
        except Exception as e:
            # print(translator.translate(entry[key], dest=target)[0].extra_data)
            time.sleep(10)
            print(e)
            success=False
            retry_count += 1
    if not success:
        raise Exception('Cannot translate {} after retrying'.format(entry))

    return new_entry

def translate(source, target_lang, output_path, num_workers=16):
    with open(source, 'r') as f:
        ds = json.load(f)[-100:]

    translated = []
    params = []
    for entry in ds:
        params.append((entry, target_lang))
    
    with mp.Pool(num_workers) as p:
        results = list(tqdm(p.imap(translate_entry, params), total=len(params)))
    
    translated = results
    assert len(translated) == len(ds)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(translated, f, indent=1, ensure_ascii=False)

if __name__ == '__main__':
    fire.Fire(translate)
