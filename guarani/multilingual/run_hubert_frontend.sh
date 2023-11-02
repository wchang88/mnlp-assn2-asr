# !/usr/bin/env bash
# Set bash to 'debug' mode, it will exit on :
# -e 'error', -u 'undefined variable', -o ... 'error in pipeline', -x 'print commands',
set -e
set -u
set -o pipefail


# ./asr.sh --train_set train --valid_set dev --test_sets test --bpe_train_text "data/train/text" --lm_train_text "data/train/text" --asr_config conf/train_asr_guarani_branchformer.yaml

# ./asr.sh \
#     --stage 10 \
#     --stop_stage 13 \
#     --nj 2 \
#     --ngpu 1 \
#     --gpu_inference true \
#     --inference_nj 1 \
#     --use_lm false \
#     --lang gn \
#     --token_type word \
#     --asr_config conf/train_asr_guarani_branchformer.yaml \
#     --inference_args "--beam_size 10 --ctc_weight 0.3" \
#     --train_set train \
#     --valid_set dev \
#     --test_sets test \
#     --bpe_train_text "data/train/text" \
#     --lm_train_text "data/train/text" "$@" \
#     --audio_format wav \
#     --expdir exp_wandb_with_lm_beam_test

asr_config=conf/train_asr_guarani_hubert_frontend.yaml

inference_config=conf/decoder_asr.yaml
lm_config=conf/train_lm_transformer.yaml
# --inference_config "${inference_config}" \

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
    --asr_config "${asr_config}" \
    --inference_args "--beam_size 20 --ctc_weight 0.5 --lm_weight 0.5" \
    --train_set train \
    --valid_set dev \
    --test_sets test \
    --bpe_train_text "data/train/text" \
    --lm_train_text "data/train/text" \
    --audio_format wav \
    --expdir exp_wandb_with_hubert_fused_frontend \
    --speed_perturb_factors "0.9 1.0 1.1" \
    --ignore_init_mismatch "true" \
    --bpe_train_text "data/train/text" "$@"
    