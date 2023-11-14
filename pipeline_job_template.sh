#!/bin/bash
#PBS -q normal
#PBS -l select=1:ncpus=64:ngpus={{ngpu}}:mem=110gb
#PBS -l walltime={{wall_time}}:00:00
#PBS -j oe
#PBS -k oed
#PBS -P 13003565
#PBS -N {{dataset_conf}}.{{prompt}}
#PBS -o psb_runs/{{model_name}}.{{dataset_conf}}.{{prompt}}.log

################################################# 
echo PBS: qsub is running on $PBS_O_HOST
echo PBS: executing queue is $PBS_QUEUE
echo -e "Work folder is $PWD\n\n"

echo PBS: working directory is $PBS_O_WORKDIR
echo PBS: job identifier is $PBS_JOBID
echo PBS: job name is $PBS_JOBNAME
echo PBS: node file is $PBS_NODEFILE
echo PBS: current home directory is $PBS_O_HOME
echo PBS: PATH = $PBS_O_PATH
#################################################
cd $PBS_O_WORKDIR
echo -e "Work folder is $PWD\n\n"

#################################################
# source /data/projects/13003565/geyu/anaconda3/etc/profile.d/conda.sh
source /data/projects/13003565/geyu/miniconda3/etc/profile.d/conda.sh 
conda activate xllm
echo "Virtual environment activated"

#################################################
#################################################
cd {{script_dir}}

bash script/pipeline.sh {{model_name}} {{dataset_conf}} {{ngpu}} 2 {{batch_size}} {{prompt}} {{home_path}} {{xllm_path}} {{project_name}} {{learning_rate}}
#################################################
#################################################
echo "Finished"