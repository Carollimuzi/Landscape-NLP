# 🌿 Landscape-NLP

This repository provides the codebase for the paper:

> **LCNER: A Named Entity Recognition Dataset and Model for Landscape and Urban Planning**

It includes tools for preprocessing landscape-related online reviews, training NER models, and evaluating predictions within the domain of landscape and urban planning.

---

## 📁 Repository Structure & Functionality

- `Data_process.ipynb`  
  A complete walkthrough for:
  - Converting raw `.csv` files (with review sentences) into JSON Lines format for model input
  - Parsing model predictions back to `.csv` for **manual verification**
  - Converting manually corrected `.csv` files into `json-spans` format for **model training**

- Model training & prediction scripts are built on top of [AdaSeq](https://github.com/modelscope/AdaSeq).

---

## 📦 Data Availability
To comply with platform fair-use policies, we do not release the full dataset. Instead, we provide a sample of 100 annotated sentences for demonstration purposes.

---

## 🚀 Quick Start

```bash
## 🔧 Installation
pip install -e . ## install adaseq
pip install -r requirements.txt -f https://modelscope.oss-cn-beijing.aliyuncs.com/releases/repo.html

## 🏋️‍♂️ Train a Model
python scripts/train.py -c paper_configs/gp_xlmroberta_large.yaml

## 🧪 Predict or Evaluate
python scripts/predict.py
### Make sure your input data follows the expected format (json-spans or jsonlines depending on your task).
