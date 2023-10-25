import fire
import multiprocessing as mp
import json
import googletrans
from tqdm import tqdm
import time 
translator = googletrans.Translator()
ALPACA_PATH = './data/alpaca/alpaca_en.json'

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

def translate_alpaca(target, num_workers=4):
    with open(ALPACA_PATH, 'r') as f:
        alpaca_ds = json.load(f)

    translated_alpaca = []
    params = []
    for entry in alpaca_ds:
        params.append((entry, target))
    
    with mp.Pool(num_workers) as p:
        results = list(tqdm(p.imap(translate_entry, params), total=len(params)))
    
    translated_alpaca = results
    assert len(translated_alpaca) == len(alpaca_ds)

    with open(f'./data/alpaca/alpaca_{target}.json', 'w') as f:
        json.dump(translated_alpaca, f, indent=1)

if __name__ == '__main__':
    fire.Fire(translate_alpaca)
