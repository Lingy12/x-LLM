import pandas as pd
import fire
import json
def to_json(source, dest):
    with open(source, 'r') as f:
        data = json.load(f)

    with open(dest, 'w', encoding='utf-8') as f:
        json.dump(data,f, ensure_ascii=False)
    # df.to_json(dest, index=False, indent=1, orient='records')

if __name__ == '__main__':
    fire.Fire(to_json)