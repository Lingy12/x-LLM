import os
import fire
from config import job_config
import itertools
import re
TEMPLATE = './training_job_template.sh'


with open(TEMPLATE, 'r') as f:
    template = f.read()
# print(template)

def get_place_holder(template):
    placeholders = re.findall(r'{{(.*?)}}', template)
    return list(placeholders)

def generate_jobs(data_group, dest_dir, gpu_num, home_path, xllm_path, project_name, wall_time=24):
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)
    
    if not os.path.exists(os.path.join(dest_dir, 'psb_runs/')):
        os.mkdir(os.path.join(dest_dir, 'psb_runs/'))
    conf_group = getattr(job_config, data_group)
    params = itertools.product(conf_group['data'], conf_group['prompt'], conf_group['base_model'])
    params_required = get_place_holder(template)
    
    for data, prompt, base_model in params:
        params = {"ngpu": str(gpu_num), "dataset_conf": str(data), "prompt":str(prompt), 
                  "script_dir": os.getcwd(), "model_name": base_model, "wall_time": str(wall_time), 
                  "home_path": home_path, "xllm_path": xllm_path, "project_name":project_name}
        
        missing_key = set(params_required) - set(params.keys())
        if len(missing_key) == 0:
            print('All key are valid')
        else:
            raise Exception('{} are missing from params. '.format(','.join(missing_key)))
        bash_script = template
        for param, value in params.items():
                placeholder = '{{' + param + '}}'
                bash_script = bash_script.replace(placeholder, value)
        
        with open(os.path.join(dest_dir, f'job_run_{base_model}_{data}_{prompt}.sh'), 'w') as f:
            f.write(bash_script)
            
if __name__ == '__main__':
    fire.Fire(generate_jobs)