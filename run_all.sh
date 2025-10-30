#!/bin/bash

# ==== 1. Environment Setup ====
echo "=== [1/3] Setting up environment ==="
ENV_NAME="lcner_env"

# Check if conda is installed
if ! command -v conda &> /dev/null
then
    echo "Conda not found. Please install Miniconda or Anaconda first."
    exit 1
fi

# Create environment if not exists
if conda env list | grep -q "$ENV_NAME"; then
    echo "Environment '$ENV_NAME' already exists. Skipping creation."
else
    echo "Creating new conda environment '$ENV_NAME'..."
    conda env create -f environment.yml -n "$ENV_NAME"
fi

# Activate environment
echo "Activating environment..."
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate "$ENV_NAME"

echo "Environment ready."

# ==== 2. Grid Search / Training ====
echo "=== [2/3] Starting grid search training ==="

# Define paths
CONFIG_PATH="/paper_configs/grid_search.yaml"
LOG_FILE="log.txt"

# Run training
python scripts/grid_search.py tune \
    -c "$CONFIG_PATH" \
    -y \
    -g 0 \
    -to "$LOG_FILE"

if [ $? -ne 0 ]; then
    echo "Grid search training failed. Check $LOG_FILE for details."
    exit 1
else
    echo "Grid search training completed successfully."
fi

# ==== 3. Completion Message ====
echo "=== [3/3] Workflow completed successfully ==="
echo "Logs saved to: $LOG_FILE"
