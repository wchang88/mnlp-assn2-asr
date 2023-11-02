# !/usr/bin/env bash
# Set bash to 'debug' mode, it will exit on :
# -e 'error', -u 'undefined variable', -o ... 'error in pipeline', -x 'print commands',
set -e
set -u
set -o pipefail
lm_config=conf/train_lm_transformer.yaml
./asr.sh \
    --stage 1 \
    --stop_stage 13 \
    --nj 4 \
    --ngpu 1 \
    --gpu_inference true \
    --inference_nj 1 \
    --use_lm true \
    --lm_config "${lm_config}" \
    --lang gn \
    --nbpe 100 \
    --asr_config conf/train_asr_guarani_hubert_frontend.yaml \
    --inference_args "--beam_size 20 --ctc_weight 0.5 --lm_weight 0.5" \
    --train_set train \
    --valid_set dev \
    --test_sets test \
    --bpe_train_text "data/train/text" \
    --lm_train_text "data/train/text" \
    --audio_format wav \
    --expdir exp_gn_branchformer_hubert_frontend "$@" \
    --dumpdir tmp_dump/dump_branchformer_hubert_frontend

