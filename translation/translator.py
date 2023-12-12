import sys
import json
from tqdm import tqdm
import googletrans
import fire
import multiprocessing as mp
import google_trans_new
from deep_translator import GoogleTranslator
# translator=googletrans.Translator()
# translator = google_trans_new.google_translator()
import time

# def unpack_translation(translate_result): 
#     if isinstance(translate_result, list):
#         return ''.join(list(map(lambda x: x.text, translate_result)))
#     else:
#         return translate_result.text
#
def translate_entry(args):
    entry, translator = args
    # success = False
    new_entry = None
    # retry_count = 0

    new_entry = {}
    for key in entry.keys():
        # print(key)
        success = False
        retry_count = 0
        while not success and retry_count < 10:
            try:
                if len(entry[key].strip()) == 0 or not entry[key]:
                    new_entry[key] = entry[key]
                else:        
                    if len(entry[key]) > 4000:
                        chunks = [entry[key][i:i + 4000] for i in range(0, len(entry[key]), 4000)]
                    else:
                        chunks = [entry[key]]
                # print(chunks)
                    new_entry[key] = ''.join([translator.translate(chunk) for chunk in chunks])

            # new_entry[key] = ''.join([unpack_translation(translator.translate(chunk, lang_tgt=target)) for chunk in chunks])
                success = True
            except Exception as e:
                print(entry)
                time.sleep(10)
                print(e)
                success=False
                retry_count += 1
        if not success:
                # raise e
                # raise Exception('Cannot translate {} after retrying'.format(entry))
            new_entry[key] = entry[key]
    # print(new_entry)
    return new_entry

def translate(source, target_lang, output_path, num_workers=16):
    with open(source, 'r') as f:
        ds = json.load(f)[-40:]
    # print(ds[-40:][:2])
    translated = []
    translator = GoogleTranslator(source='auto', target=target_lang)
    params = []
    for entry in ds:
        params.append((entry, translator))
    
    with mp.Pool(num_workers) as p:
        results = list(tqdm(p.imap(translate_entry, params), total=len(params)))
    
    translated = results
    assert len(translated) == len(ds)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(translated, f, indent=1, ensure_ascii=False)

if __name__ == '__main__':
    fire.Fire(translate)
