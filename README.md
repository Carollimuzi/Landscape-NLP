# Landscape-NLP

This repository hosts the code for the paper LCNER: A Named Entity Recognition Dataset and Model for Landscape and Urban Planning.

The Data_process.ipynb notebook provides a demonstration of how to convert a CSV file containing online review sentences into a JSON Lines format compatible with our model for prediction. It also illustrates how to transform the predicted output into a CSV format that facilitates manual verification and annotation, as well as how to convert the annotated CSV file into a json-spans format for model training.

Our training process follows the procedure and tutorials outlined in [AdaSeq](https://github.com/modelscope/AdaSeq).

Note: To comply with platform data fair use policies, we do not provide the complete dataset. Instead, we offer a sample of 100 sentences. You can directly use our model for predictions or create your own dataset.
