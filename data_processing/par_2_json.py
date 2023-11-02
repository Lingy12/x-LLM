import pandas as pd
import fire

def to_json(source, dest):
    df = pd.read_parquet(source)

    df.to_json(dest, index=False, indent=1, orient='records')

if __name__ == '__main__':
    fire.Fire(to_json)