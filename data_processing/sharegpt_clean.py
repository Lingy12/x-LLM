import json
from tqdm import tqdm
with open('./data/sharegpt/90k_mix.json', 'r') as f:
    data = json.load(f)
    
id = 0
cleaned_data = []

for entry in tqdm(data):
    conversations = entry['conversations']
    lang = entry['lang']
    if len(conversations) < 2:
        continue
    if lang != 'en':
        continue

    target_conversations = conversations[:2]
    new_entry = {"instruction": target_conversations[0]['value'], 
                 "input": '', 
                 "target": target_conversations[1]['value']}
    cleaned_data.append(new_entry)

with open('./data/sharegpt/90k_en.json', 'w', encoding='utf-8') as f:
    json.dump(cleaned_data, f, ensure_ascii=False, indent=1)
