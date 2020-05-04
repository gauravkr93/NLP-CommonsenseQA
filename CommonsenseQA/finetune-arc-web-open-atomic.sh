#!/bin/bash

## Write the finetuning part to a bash script file
# Modified following from the original script to get it to run on Google AI platform and Colab
# - Set MAX_SENTENCES=8
# - Added --update-freq 4

MAX_UPDATES=3000      # Number of training steps.
WARMUP_UPDATES=150    # Linearly increase LR over this many steps.
LR=1e-05              # Peak LR for polynomial LR scheduler.
MAX_SENTENCES=2      # Batch size.
SEED=23                # Random seed.

BASEDIR=/home/jupyter
# CQA_PATH=/content/CommonsenseQA # For Google Colab
CQA_PATH=$BASEDIR/CommonsenseQA # For Kaggle
ROBERTA_PATH=${BASEDIR}/roberta.large/model.pt
DATA_DIR=${CQA_PATH}/data/CommonsenseQA/arc-web-open-atomic

# we use the --user-dir option to load the task from
# the examples/roberta/commonsense_qa directory:
FAIRSEQ_PATH=${CQA_PATH}/fairseq
FAIRSEQ_USER_DIR=${FAIRSEQ_PATH}/examples/roberta/commonsense_qa_with_kb

cd $FAIRSEQ_PATH
CUDA_VISIBLE_DEVICES=0 fairseq-train --fp16 --ddp-backend=no_c10d \
    $DATA_DIR \
    --update-freq 4 \
    --save-dir ./checkpoints \
    --user-dir $FAIRSEQ_USER_DIR \
    --restore-file $ROBERTA_PATH \
    --reset-optimizer --reset-dataloader --reset-meters \
    --no-epoch-checkpoints --no-last-checkpoints --no-save-optimizer-state \
    --best-checkpoint-metric accuracy --maximize-best-checkpoint-metric \
    --task commonsense_qa_with_kb --init-token 0 --bpe gpt2 \
    --arch roberta_large --max-positions 512 \
    --dropout 0.1 --attention-dropout 0.1 --weight-decay 0.01 \
    --criterion sentence_ranking --num-classes 5 \
    --optimizer adam --adam-betas '(0.9, 0.98)' --adam-eps 1e-06 --clip-norm 0.0 \
    --lr-scheduler polynomial_decay --lr $LR \
    --warmup-updates $WARMUP_UPDATES --total-num-update $MAX_UPDATES \
    --max-sentences $MAX_SENTENCES \
    --max-update $MAX_UPDATES \
    --log-format simple --log-interval 25 \
    --seed $SEED
