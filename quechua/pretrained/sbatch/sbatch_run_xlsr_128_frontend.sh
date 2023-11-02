#!/bin/bash
#SBATCH --nodes=1
#SBATCH --job-name=train_quy_branchformer_xlsr_128_frontend
#SBATCH --mem=80GB
#SBATCH --gres=gpu:A6000:1
#SBATCH --time=1-00:00:00
#SBATCH --partition=babel-shared-long
#SBATCH -o out/train_quy_branchformer_xlsr_128_frontend.out
bash runners/run_xlsr_128_frontend.sh
