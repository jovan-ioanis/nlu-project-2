# NLU Project 2: Beyond seq2seq Dialog Systems
This repository contains the submission for the student project in the "Natural Language Understanding" course at ETH Zürich in spring 2017. The goal of the project was to train a conversational agent using sequence-to-sequence recurrent neural networks and further improve performance by extending the baseline seq2seq model.

### Authors

* [Florian Chlan](https://github.com/flock0)
* [Samuel Kessler](https://github.com/skezle)
* [Jovan Nikolic](https://github.com/jovan-ioanis)
* [Jovan Andonov](https://github.com/ac1dxtrem)

### Project Report
Can be found [here](https://github.com/skezle/ethz-nlu-seq2seq/blob/master/report/nlu-project-2.pdf)

### Requirements

* Python 3.x
* tensorflow 1.1
* tqdm
* gensim

### Training the model

The model can be trained using `main.py`. `python main.py -h` shows which parameters we expect:
```
main.py -n <num_cores> -x <experiment>
num_cores = Number of cores requested from the cluster. Set to -1 to leave unset
experiment = experiment setup that should be executed. e.g 'baseline' or 'attention'
tag = optional tag or name to distinguish the runs, e.g. 'bidirect3layers'
```
We expect training data triples and the cornell dataset to be in the `./data/` subdirectory with their original filenames.

Detailed configuration parameters may be changed in `config.py`.

Model checkpoints, summaries and the configuration are regularly stored in the `./logs/` folder (and its subdirectories).

### Predicting words from the model

Model predictions may be done with `predict.py`. `python predict.py -h` shows which parameters we expect:
```
predict.py -n <num_cores> -x <experiment> -o <output file> -c <checkpoint>
num_cores = Number of cores requested from the cluster. Set to -1 to leave unset
experiment = experiment setup that should be executed. e.g 'baseline'
checkpoint = Path to the checkpoint to load parameters from. e.g. './logs/baseline-ep4-500'
output = where to write the prediction outputs to. e.g './predictions.out'
```
We will predict sentence tuples from the `./data/Validation_Shuffled_Dataset.txt` conversation triples.
The predictions are not printed on screen, but written to disk. (see the `--output` parameter).

### Calculating perplexities from the model

Perplexity calculation may be done with `perplexity.py`. `python perplexity.py -h` shows which parameters we expect:
```
perplexity.py -n <num_cores> -x <experiment> -i <input file> -c <checkpoint>
num_cores = Number of cores requested from the cluster. Set to -1 to leave unset
experiment = experiment setup that should be executed. e.g 'baseline'
input = what dialogs to predict from. e.g './Dialog_Triples.txt'
checkpoint = Path to the checkpoint to load parameters from. e.g. './logs/baseline-ep4-500'
```

We also provide the `./run-test.sh` script which prints perplexities using our provided checkpoint `final_checkpoint.ckpt`

### Attributions

* Our baseline model is based on [ematvey/tensorflow-seq2seq-tutorials](https://github.com/ematvey/tensorflow-seq2seq-tutorials).
* The idea for anti-lm has been taken from [Marsan-Ma/tf_chatbot_seq2seq_antilm](https://github.com/Marsan-Ma/tf_chatbot_seq2seq_antilm).
