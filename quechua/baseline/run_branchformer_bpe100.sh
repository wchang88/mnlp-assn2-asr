# !/usr/bin/env bash
# Set bash to 'debug' mode, it will exit on :
# -e 'error', -u 'undefined variable', -o ... 'error in pipeline', -x 'print commands',
set -e
set -u
set -o pipefail

./asr.sh \
    --stage 1 \
    --stop_stage 13 \
    --nj 4 \
    --ngpu 1 \
    --gpu_inference true \
    --inference_nj 1 \
    --use_lm false \
    --lang quy \
    --token_type bpe \
    --nbpe 100 \
    --asr_config conf/train_asr_quechua_branchformer_bpe100.yaml \
    --inference_args "--beam_size 10 --ctc_weight 0.3" \
    --train_set train \
    --valid_set dev \
    --test_sets test \
    --bpe_train_text "data/train/text" \
    --lm_train_text "data/train/text" \
    --audio_format wav \
    --expdir exp_quy_branchformer_bpe100 "$@" 

