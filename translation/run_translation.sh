DATASET=$1

python translation/translator.py ./data/$DATASET/"$DATASET"_en.json zh-CN ./data/$DATASET/"$DATASET"_zh.json &
python translation/translator.py ./data/$DATASET/"$DATASET"_en.json es ./data/$DATASET/"$DATASET"_es.json &
python translation/translator.py ./data/$DATASET/"$DATASET"_en.json vi ./data/$DATASET/"$DATASET"_vi.json &
