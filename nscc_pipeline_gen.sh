DATA_GROUP=$1
CARD_REQUIRED=$2
BS=$3
LR=$4

OUT_NAME=$DATA_GROUP.$BS.$LR
python generate_pipeline_job.py $DATA_GROUP /home/project/13003565/geyu/jobs/x-LLM-job/$OUT_NAME $CARD_REQUIRED /home/project/13003565/geyu/ x-LLM $OUT_NAME $BS $LR
