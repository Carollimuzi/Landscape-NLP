# ICASSP2023 MUG Challenge Track4 Keyphrase Extraction Baseline

This tutorial shows how to train a baseline model for the Keyphrase Extraction track in the ICASSP2023 MUG Challenge.

## Table of Contents:
- [5 Steps to Train a Model](#5-steps-to-train-a-model)
- [Just Give Me a Command to Run Everything](#just-give-me-a-command-to-run-everything)
- [Benchmarks](#benchmarks)


## 5 Steps to Train a Model

We model KPE as a sequence-labeling problem and apply the Bert-CRF model implemented in [AdaSeq](https://github.com/modelscope/adaseq) to solve it.

> AdaSeq is an easy-to-use library, built on ModelScope, which provides plenty of cutting-edge models, training methods and useful toolkits for sequence understanding tasks.

#### Step 1: Requirements & Installation
Python version >= 3.7
```
git clone https://github.com/modelscope/adaseq.git
pip install -r requirements.txt -f https://modelscope.oss-cn-beijing.aliyuncs.com/releases/repo.html
```

#### Step 2: Download & Preprocess Data
1. Download and put `train.json` `dev.json` `except_TS_test1_without_label.csv` to `${root_dir}/examples/ICASSP2023_MUG_track4/dataset/`. `${root_dir}` is the absolute path of the AdaSeq repository.

2. Preprocess the downloaded data by splitting it into splits of 128 characters (or longer) and reformat data into CoNLL format.
```
cd examples/ICASSP2023_MUG_track4
python preprocess.py
```

#### Step 3: Start Training
1. Modify the config file
Change the `${root_dir}` in `configs/bert_crf_sbert.yaml` to your own ABSOLUTE path of this repo.

2. Start training
Let’s train a Bert-CRF model using the preset script as an example.
```
cd ${root_dir}
python scripts/train.py -c examples/ICASSP2023_MUG_track4/configs/bert_crf_sbert.yaml
```

Also, there are many methods other than Bert-CRF implemented in AdaSeq, such as RaNER, Global-Pointer, etc.

What's more, a [grid search tool](../../docs/tutorials/hyperparameter_optimization.md) is provided for efficient tuning.

#### Step 4: Evaluate Your Model
First install some requirements in the evaluation script.
```
pip install jieba rouge yake
```

Use `evaluate_kw.py` to evaluate the predictions. For KPE, the union of the labels from the three annotators is used as the final manual labels for training and evaluation.

There are 4 necessary parameters:
- `<data_path>`: the source test data. e.g. dev.json.
- `<pred_path>`: the prediction file output by your model.
- `<doc_split_path`>:  the file recording where documents are split, which is output by preprocessing.
- `<out_path>`: the file path in which the evaluation log will be.

For example:

```shell
cd examples/ICASSP2023_MUG_track4
python evaluate_kw.py dataset/dev.json ${root_dir}/experiments/kpe_sbert/outputs/${datetime}/pred.txt dataset/split_list_dev.json evaluation.log
```

#### Step 5: Make predictions on test files
First use your trained model to make predictions on the test file.

```shell
cd ${root_dir}
python scripts/test.py -c examples/ICASSP2023_MUG_track4/configs/bert_crf_sbert.yaml -cp ${model_path}
```
The output file is pred.txt in your current path.

Then use `get_keywords.py` to make predictions on test file. There are 4 necessary parameters as same as those in `Step 4`.

For example:

```shell
cd examples/ICASSP2023_MUG_track4
python get_keywords.py dataset/test.json ../../pred.txt dataset/split_list_test.json ${out_path}
```

Now you can submit `${out_path}` to the competition!

## Just Give Me a Command to Run Everything
Here you go:
```commandline
sh ./examples/ICASSP2023_MUG_track4/end2end.sh ${your_sdk_token}
```

The `${your_sdk_token}` should be replaced with [your ModelScope sdk token](https://modelscope.cn/my/myaccesstoken).

After all finished, a `submit.json` file will be generated, which can be used to submit for the competition.

## Benchmarks

| Split |  Model   |               Backbone                | Exact/Partial F1 @10 | Exact/Partial F1 @15 | Exact/Partial F1 @20 |                                                           Checkpoint                                                            |
|:-----:|:--------:|:-------------------------------------:|:--------------------:|:--------------------:|:--------------------:|:-------------------------------------------------------------------------------------------------------------------------------:|
|  Dev  |   yake   |                   -                   |      15.0/24.3       |      19.8/30.4       |      20.4/32.1       |                                                                -                                                                |
|  Dev  | Bert-CRF |         sijunhe/nezha-cn-base         |      35.6/43.2       |      38.1/49.5       |      37.2/48.1       |                                                                -                                                                |
|  Dev  | Bert-CRF | damo/nlp_structbert_backbone_base_std |      35.9/47.7       |      40.1/52.2       |      39.4/51.1       | [ModelScope](https://modelscope.cn/models/damo/nlp_structbert_keyphrase-extraction_base-icassp2023-mug-track4-baseline/summary) |
