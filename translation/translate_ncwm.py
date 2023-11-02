import os
import googletrans
import multiprocessing as mp
import time
import shutil
from tqdm import tqdm
import fire

NCWM_PATH = "data/translation/ncwm/en-ar/train.en"
translator = googletrans.Translator()

def translate_sentence(args):
    sentence, target = args
    if len(sentence) == 0:
        return sentence
    success = False
    retry_count = 0
    result = None
    while not success and retry_count <= 10:
        try:
            result = translator.translate(sentence, dest=target).text
            success = True
        except:
            retry_count += 1
            time.sleep(2)
    if result is None:
        raise Exception('Cannot translate some of the sentence')
    return result

def translate_ncwm(target:str, num_workers:int=4):
    data_path = 'data/translation/ncwm'
    new_target_path = os.path.join(data_path, f'en-{target}')

    if not os.path.exists(new_target_path):
        os.mkdir(new_target_path)
    
    ori_file = os.path.join(new_target_path, 'train.en')
    if not os.path.exists(ori_file):
        shutil.copy(NCWM_PATH, new_target_path)

    with open(ori_file, 'r') as f:
        lines = f.readlines()

    params = list(map(lambda x: (x.strip(), target), lines))

    with mp.Pool(num_workers) as p:
        results = list(tqdm(p.imap(translate_sentence, params), total=len(params)))
    
    output_file = os.path.join(new_target_path, f'train.{target}')

    if os.path.exists(output_file):
        os.remove(output_file)
    with open(output_file, 'a') as f:
        for res in results:
            if res is None:
                raise Exception('Some not translated')
            f.write(res + "\n")

if __name__ == "__main__":
    fire.Fire(translate_ncwm) 
