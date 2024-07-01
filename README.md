# literature
Analysis code for literature data

## Data processing

### 1.Transform raw abstract
```bash
python make_data.py -i raw_abstract -s 'Species'
```

### 2.AutoNER prediction （https://shangjingbo1226.github.io/AutoNER/）
```bash
export CUDA_LAUNCH_BLOCKING=1
MODEL_NAME="Mouse"
GPU_ID=0
RAW_TEXT="raw_text.txt"

green=`tput setaf 2`
reset=`tput sgr0`

MODEL_ROOT=./models/$MODEL_NAME
CHECKPOINT=$MODEL_ROOT/checkpoint/autoner/

python preprocess_partial_ner/encode_test.py --input_data $RAW_TEXT --checkpoint_folder $CHECKPOINT --output_file $MODEL_ROOT/encoded_test.pk

python test_partial_ner.py --input_corpus $MODEL_ROOT/encoded_test.pk --checkpoint_folder $CHECKPOINT --output_text $MODEL_ROOT/AutoNer_result.txt --hid_dim 300 --droprate 0.5 --word_dim 200
```

### 3.BioBERT prediction （https://github.com/dmis-lab/biobert）
```bash
export CUDA_VISIBLE_DEVICES=1
python run_ner.py \
    --data_dir . \
    --labels labels.txt \
    --model_name_or_path /biobert-pytorch/named-entity-recognition/output/model \
    --output_dir . \
    --max_seq_length 192 \
    --num_train_epochs 30 \
    --per_device_train_batch_size 16 \
    --per_device_eval_batch_size 8 \
    --save_steps 1000 \
    --seed 2 \
    --do_predict \
    --overwrite_output_dir
```

### 4.Combine result of AutoNER and BioBERT
```bash
python3 compare_result.py -d AutoNer_result.txt -r BioBert_result.txt
```

### 5.Extract sentences，pheonotypes, genes (get gene_list.txt and pheno_list.txt)
```bash
python3 literature_format.py -a raw_abstract.txt
```

### 6.Filter for false positives based on similarity (get gene_list_match.txt and pheno_list_match.txt)
```bash
python3 dict_match.py -g gene_list.txt
python3 dict_match_pheno.py -p pheno_list.txt
```

### 7.Get abstract entity form 3.2abstract_entity_info.txt
```bash
python3 get_abstract_entity_info.py -a raw_abstract.txt -g gene_list_match.txt -p pheno_list_match.txt
```

### 8.Get sentence form 2.1sentence_info.txt
```bash
python3 get_sentence_info.py -d  -a raw_abstract.txt -g gene_list_match.txt -p pheno_list_match.txt -s 'Species' -b sp
geneid_name.txt: (Gene id and name extract form gff and gtf)
```

### 9.Get sentence entity form 2.2sentence_entity_info.txt
```bash
python3 get_sentence_entity_info.py -s 2.1sentence_info.txt
```

### 10.Get abstract information form 3.1literature.txt
```bash
python3 get_literate_info.py -a raw_abstract.txt -s 'Species'
```