DATASET=$1

python translation/translator.py ./data/$DATASET/"$DATASET"_en.json zh-CN ./data/$DATASET/$DATASET_zh.json &
python translation/translator.py ./data/$DATASET/"$DATASET"_en.json es ./data/$DATASET/$DATASET_es.json &
python translation/translator.py ./data/$DATASET/"$DATASET"_en.json vi ./data/$DATASET/$DATASET_vi.json &
