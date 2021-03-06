import argparse
import os
import numpy as np
import pandas as pd
from os.path import dirname, basename, abspath, join, exists
from scipy.signal import argrelextrema

# Internals
from utils import load_train, load_csv, ACTI_GRAPH
from analyze import eval_preds

def get_labeled_preds(limit=10):
    indices = []
    preds = []
    for name in os.listdir(ACTI_GRAPH)[:limit]:
        indices.append(int(basename(name).split(".csv")[0]))
        preds.append(calc_steps(name))
    data = np.array((indices, preds)).T
    return pd.DataFrame(data=data, columns=['PID', 'PRED'])

def eval_ours():
    labeled_preds = get_labeled_preds(121)
    eval_preds(labeled_preds, "WALKER_AID_6MWT", "aid", "OURS")

def eval_naive():
    tr = load_train()
    valid_ids = tr['PID'].values
    preds = np.zeros(len(valid_ids))
    data = np.array((valid_ids, preds)).T
    labeled_preds =  pd.DataFrame(data=data, columns=['PID', 'PRED'])
    eval_preds(labeled_preds, "WALKER_AID_6MWT", "aid", "NAIVE")

def main():
    parser = argparse.ArgumentParser(description="Main")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-n', '--naive', action='store_true')
    group.add_argument('-o', '--ours', action='store_true')
    args = parser.parse_args()
    if args.naive:
        eval_naive()
    else:
        eval_ours()

if __name__ == '__main__':
    main()
