# 🌿 Landscape-NLP

This repository provides the codebase for the paper:

> **Measuring environment-human interactions using a named entity recognition model**

It includes tools for preprocessing landscape-related online reviews, applying stage-specific prompts, training NER models, and evaluating predictions within the domain of landscape and urban planning.

---

## 📁 Repository Structure & Functionality


- `Data_process.ipynb`  
  A complete walkthrough for:
  - Converting raw `.csv` files (with review sentences) into JSON Lines format for model input
  - Parsing model predictions back to `.csv` for **manual verification**
  - Converting manually corrected `.csv` files into `json-spans` format for **model training**

- `Main prompts.ipynb`  
  A collection of few-shot prompts for:
  - Automatic annotation using GPT-4
  - Enhancing lexicon-based classification performance
  - Selecting sentences that contain underrepresented entities
  
- `Grid-search-results.ipynb`  
  - Contains the loss and F1-score curves for each hyperparameter combination, with the optimal early-stopping point (patience = 5) clearly marked.
    
- Model training & prediction scripts are built on top of [AdaSeq](https://github.com/modelscope/AdaSeq).

---

## 📦 Data Availability
To comply with platform fair-use policies, we do not release the full dataset. Instead, we provide a representative sample of 100 annotated sentences (test100.json) for demonstration purposes.

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
