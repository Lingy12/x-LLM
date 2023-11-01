import os
import json

MODEL_DIR = 'model'

models = os.listdir(MODEL_DIR)

m_dict = {}
for model in models:
    m_dict[model] = os.path.join(os.getcwd(), 'model', model)

print(json.dumps(m_dict, indent=1))
print('\n'.join(models))

