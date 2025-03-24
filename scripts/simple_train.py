# Copyright (c) Alibaba, Inc. and its affiliates.
"""
launch command: python scripts/train.py -c paper_configs/global_roberta.yaml
"""
import argparse
import os
import sys
import warnings

parent_folder = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent_folder)

from adaseq.commands.train import train_model_from_args, train_model  # noqa # isort:skip
from datasets_preprocess import csv_to_custom_json, update_config  # noqa # isort:skip
warnings.filterwarnings('ignore')

if __name__ == '__main__':
    parser = argparse.ArgumentParser('train.py')
    parser.add_argument(
        '-c', '--config_path', type=str, required=True, help='configuration YAML file'
    )
    parser.add_argument(
        '-w',
        '--work_dir',
        type=str,
        default=None,
        help='directory to save experiment logs and checkpoints',
    )
    parser.add_argument('-n', '--run_name', type=str, default=None, help='trial name')
    parser.add_argument(
        '-f', '--force', default=None, help='overwrite the output directory if it exists.'
    )
    parser.add_argument('-ckpt', '--checkpoint_path', default=None, help='model checkpoint to load')
    parser.add_argument('--seed', type=int, default=None, help='random seed for everything')
    parser.add_argument('-d', '--device', type=str, default='gpu', help='device name')
    parser.add_argument('--use_fp16', action='store_true', help='whether to use mixed precision')
    parser.add_argument('--local_rank', type=str, default='0')

    # put your datasets here
    train_path, test_path = csv_to_custom_json("paper_datasets/1206check_modified.csv")
    valid_path = test_path  # 使用测试集作为验证集
    print(f"\nTrain JSON saved at: {train_path}")
    print(f"\nTest JSON saved at: {test_path}")
    args = parser.parse_args()
    config_path = os.path.abspath(args.config_path)  
    print(f"\nUsing config file: {config_path}\n")
    update_config(config_path, train_path, valid_path, test_path)

    train_model_from_args(args)

