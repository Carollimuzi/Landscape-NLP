# bash run_predict.sh
WORK_DIR="model_path"
CKPT_PATH="$WORK_DIR/epoch_10.pth"
DEVICE="cuda:0"
LOG_FILE="$WORK_DIR/test_epoch10_test.log"

# ====== Print info ======
echo "============================================"
echo " Running AdaSeq Test (epoch_10)"
echo " Work Dir : $WORK_DIR"
echo " Checkpoint: $CKPT_PATH"
echo " Device   : $DEVICE"
echo " Log File : $LOG_FILE"
echo "============================================"

# ====== Run test ======
python AdaSeq-master/scripts/test.py \
  -w "$WORK_DIR" \
  -d "$DEVICE" \
  -ckpt "$CKPT_PATH" \
  | tee "$LOG_FILE"
