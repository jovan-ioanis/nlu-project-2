import gensim
import logging
import os
import cornell_loading
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from config import Config as conf

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def load_sentences(train_path, validation_path=None):
    sentences = []

    f = open(train_path, 'r')
    for line in f:
        conversation = line.strip().split('\t')
        for i in range(3):
            sentence = []
            for word in conversation[i].split():
                sentence.append(word)
            sentences.append(sentence)

    if validation_path is not None:
        f = open(validation_path, 'r')
        for line in f:
            conversation = line.strip().split('\t')
            for i in range(3):
                sentence = []
                for word in conversation[i].split():
                    sentence.append(word)
                sentences.append(sentence)

    return sentences

def load_sentences_from_tuples(train_path_tuples, validation_path=None):
    sentences = []

    f = open(train_path_tuples, 'r')
    for line in f:
        conversation = line.strip().split('\t')
        sentence = conversation[0].split()              # only first sentence, since they repeat!
        sentences.append(sentence)

    if validation_path is not None:
        f = open(VALIDATION_FILE, 'r')
        for line in f:
            conversation = line.strip().split('\t')
            for i in range(3):
                sentence = conversation[i].split()
                sentences.append(sentence)

    print("{} sentences used to build word2vec model!".format(len(sentences)))
    return sentences

def train_embeddings(save_to_path, embedding_size, minimal_frequency, train_tuples_path, validation_path=None, num_workers=4):
    print("Training word2vec model with following parameters: ")
    print("\t base dataset: {}, validation set used: {}".format(train_tuples_path, validation_path))
    print("\t Cornell dataset used: " + str(conf.use_CORNELL_for_word2vec))
    print("\t word embeddings size: " + str(embedding_size))
    print("\t word embeddings saved on path: {}".format(save_to_path))
    trainingset = train_tuples_path
    if conf.use_CORNELL_for_word2vec:
        trainingset = conf.both_datasets_tuples_filepath

    model = gensim.models.Word2Vec(load_sentences_from_tuples(trainingset, None),
                                   size=embedding_size,
                                   min_count=minimal_frequency,
                                   workers=num_workers)
    model.save(save_to_path)


def evaluate(path):

    print("Loading word2vec model from {}".format(path))
    model = gensim.models.Word2Vec.load(path)
    print('Vocabulary size is: {}'.format(len(model.wv.vocab)))
    print(model.most_similar(
        positive=['woman', 'king'], negative=['man'], topn=5))
    print(model.most_similar(
        positive=['girl', 'man'], negative=['boy'], topn=5))
    print(model.most_similar(
        positive=['head', 'eye', 'lips', 'nose'], negative=['toes'], topn=5))
    print(model.most_similar(
        positive=['pain'], topn=10))
    print(model.most_similar(
        positive=['pain'], negative=['happy'], topn=10))

    x = model[model.wv.vocab]
    pca = PCA(n_components=2)
    x_pca = pca.fit_transform(x[:5000,:])

    tsne = TSNE(n_components=2, random_state=0)
    x_tsne = tsne.fit_transform(x[:5000, :])

    plt.scatter(x_pca[:, 0], x_pca[:, 1])
    for label, x, y in zip(model.wv.vocab, x_pca[:, 0], x_pca[:, 1]):
        plt.annotate(label, xy=(x, y), xytext=(0, 0), textcoords='offset points')
    plt.show()

    plt.scatter(x_tsne[:, 0], x_tsne[:, 1])
    for label, x, y in zip(model.wv.vocab, x_tsne[:, 0], x_tsne[:, 1]):
        plt.annotate(label, xy=(x, y), xytext=(0, 0), textcoords='offset points')
    plt.show()


def main():
    # train_embeddings(WORD2VEC)
    evaluate(WORD2VEC)

if __name__ == "__main__":
    main()
