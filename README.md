# 🌿 Landscape-NLP

This repository provides the codebase for the paper:

> **Associations among park features, physical activities, and sensory perceptions from online reviews: a domain-specific named entity recognition model**

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
    
- Model training & prediction scripts are built on top of [AdaSeq](https://github.com/modelscope/AdaSeq).

---

## 📦 Data Availability
To comply with platform fair-use policies, we do not release the full dataset. Instead, we provide a representative sample of 100 annotated sentences (test100.json) for demonstration purposes.

Feature1023.csv is also included as the lexicon used in our experiments.

---

## 🧩 Reproducibility Checklist
The unified script run_all.sh installs the environment, executes grid search training based on the specified YAML configuration, and logs results for full reproducibility. Dataset splits follow a GroupKFold-by-park strategy to prevent lexical leakage across folds.

| **Category**        | **Item**        | **Description**                                                                                                                                 |
| ------------------- | --------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| **Dataset**         | Source          | Google Maps and TripAdvisor reviews (314 parks, Singapore)                                                                                      |
| **Dataset**         | Access          | 1% anonymized sample provided (`test100.json`)                                                                                                  |
| **Model**           | Architecture    | DeBERTa-large + GlobalPointer                                                                                                                   |
| **Training**        | Seeds           | [41, 42, 43, 44, 45]                                                                                                                            |
| **Training**        | Hardware        | NVIDIA GeForce RTX 4090 (24 GB) × 2; Intel Core i9-14900K CPU (24 cores, 32 threads); 128 GB RAM; Ubuntu 22.04.4 LTS; CUDA 12.4 + PyTorch 2.5.0 |
| **Code**            | Environment     | `environment.yml` included                                                                                                                      |
| **Reproducibility** | Data split      | `datasets_split.py` (train/validation/test with GroupKFold by park)                                                                             |
| **Reproducibility** | Training script | `run_all.sh` (environment setup + model training + logging)                                                                                     |

## 🚀 Quick Start

```bash
## 🔧 Installation
# Option 1: Install in editable (development) mode
pip install -e .

# Option 2: Install AdaSeq dependencies via requirements.txt
pip install -r requirements.txt -f https://modelscope.oss-cn-beijing.aliyuncs.com/releases/repo.html

# Option 3: Create a Conda environment from environment.yml (recommended)
conda env create -f environment.yml
conda activate adaseq

## 🏋️‍♂️ Train a Model
python scripts/train.py -c paper_configs/gp_xlmroberta_large.yaml

## 🧪 Predict or Evaluate
bash run_predict.sh # Run inference using the models released with this paper.
### Make sure your input data follows the expected format (json-spans or jsonlines depending on your task).
