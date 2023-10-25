BASE_MODEL=$1
DATASET=$2
CUDA_DEVICES=$3
NUM_PROC=$4
METHOD=${5:-"finetune"}

# ensure number of CUDA_DEVICES is more than NUM_PROC
export CUDA_VISIBLE_DEVICES=$CUDA_DEVICES

PORT=$(( $RANDOM % 1000 + 32768 ))
CPFS_PATH=/home/geyu
PROJECT_PATH=$CPFS_PATH/projects/multi-lang/x-LLM
OUTPUT_NAME=$BASE_MODEL.$DATASET.$METHOD
FSDP_CONFIG=$PROJECT_PATH/fsdp_conf.json

export HF_HOME=$CPFS_PATH/.cache/huggingface
export WANDB_API_KEY="450f5f137524092429c1579743d3941e8d31ac5d"
export WANDB_PROJECT="mt_instruction_tuning"
export WANDB_NAME=$OUTPUT_NAME
export WANDB_NOTES="FSDP on 4 A100 40"
export WANDB_DIR="$CPFS_PATH/log"

MODEL_ARGS=()
case $BASE_MODEL in  
	"llama-2-7b-hf")
		MODEL_ARGS+=("--num_train_epochs 3")
		MODEL_ARGS+=("--learning_rate 2e-5")
        FSDP="full_shard auto_wrap"
		;;  
	"llama-13b-hf")
		MODEL_ARGS+=("--num_train_epochs 5")
		MODEL_ARGS+=("--learning_rate 1e-5")
        FSDP="full_shard offload auto_wrap"
		;;  
	"bloom-7b1")
		MODEL_ARGS+=("--num_train_epochs 3")
		MODEL_ARGS+=("--learning_rate 2e-5")
        FSDP="full_shard offload auto_wrap"
		;;  
	*)  
		MODEL_ARGS+=("--num_train_epochs 3")
		MODEL_ARGS+=("--learning_rate 2e-5")
        FSDP="full_shard auto_wrap"
		;;  
esac

METHOD_ARGS=()
case $METHOD in  
	"finetune")
		;;  
	*)  
		;;  
esac

# source $CPFS_PATH/miniconda3/bin/activate $PROJECT_PATH/.env
echo "Start training"
# assume batch 128
torchrun --nproc_per_node=$NUM_PROC --master_port=$PORT \
    $PROJECT_PATH/train.py \
	${METHOD_ARGS[@]} \
	${MODEL_ARGS[@]} \
    --data_path "$PROJECT_PATH/data/$DATASET" \
    --model_name_or_path "$PROJECT_PATH/model/$BASE_MODEL" \
    --output_dir "$PROJECT_PATH/model/$OUTPUT_NAME" \
    --bf16 True \
    --per_device_train_batch_size 2 \
    --per_device_eval_batch_size 2 \
    --gradient_accumulation_steps 32 \
    --lora_r 8\
    --lora_alpha 16 \
    --lora_dropout 0.05 \
    --lora_target_modules "[q_proj, v_proj]" \
    --lora_bias 'none'\
    --lora_task '"CAUSAL_LM"'\
    --lr_scheduler_type "cosine" \
    --weight_decay 0. \
    --warmup_ratio 0.03 \
    --evaluation_strategy "no" \
    --save_strategy "no" \
    --save_steps 2000 \
    --save_total_limit 1 \
    --load_best_model_at_end True \
    --model_max_length 512\
    --optim "adamw_torch" \
    --logging_steps 1 \
    --report_to wandb tensorboard \
    --remove_unused_columns False \
    --logging_dir "$CPFS_PATH/log/tensorboard/$OUTPUT_NAME"

