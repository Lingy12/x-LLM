import fire
import json
import googletrans
from tqdm import tqdm
import time 
translator = googletrans.Translator()
ALPACA_PATH = './data/alpaca/alpaca_en.json'

def translate_alpaca(target):
    with open(ALPACA_PATH, 'r') as f:
        alpaca_ds = json.load(f)

    translated_alpaca = []
    for entry in tqdm(alpaca_ds):
        success = False
        retry_count = 0
        while not success and retry_count < 10:
            try:
                new_entry = {}
                for key in entry.keys():
                    if len(entry[key]) == 0 or not entry[key]:
                        new_entry[key] = entry[key]
                    else:
                        new_entry[key] = translator.translate(entry[key], dest=target).text
                translated_alpaca.append(new_entry)
                success = True
            except Exception as e:
                time.sleep(1)
                success=False
                retry_count += 1
        if not success:
            raise Exception('Cannot translate {} after retrying with {}'.format(entry, e))
    
    assert len(translate_alpaca) == len(alpaca_ds)

    with open(f'./data/alpaca/alpaca_{target}.json', 'w') as f:
        json.dump(translate_alpaca, f, indent=1)

if __name__ == '__main__':
    fire.Fire(translate_alpaca)
