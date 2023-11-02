#!/bin/bash
#SBATCH --nodes=1
#SBATCH --job-name=train_quy_branchformer_bpe100_multilingual
#SBATCH --mem=50GB
#SBATCH --gres=gpu:A6000:1
#SBATCH --time=1-00:00:00
#SBATCH --partition=babel-shared-long
#SBATCH -o out/train_quy_branchformer_bpe100_multilingual.out
bash runners/run_branchformer_bpe100_multilingual.sh
