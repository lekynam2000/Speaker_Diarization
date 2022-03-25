# Speaker_Diarization
The Callhome dataset contains 500 .wav files.

## Preparing dataset

The notebook **EEND makecallhome.ipynb** will:

1. Download the dataset from the server
2. Save the dataset inside your Drive
3. Split into 2 equal part callhome1 (250 .wav files) and callhome2 (250 .wav files)

## Make inference

Checkout **EEND infer from train CALLHOME.ipynb** and modify **pretrained_model** variable to infer your model on full Callhome.

## Adaption and inference

Checkout **EEND adapt CALLHOME.ipynb** and modify **pretrained_model** variable for adaption on Callhome.

## Infer the Dihard dataset

For Dihard dataset, you must prepare the dataset yourself in the Drive then run the **EEND infer from train DIHARD.ipynb**. 