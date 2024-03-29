import gzip
import os.path

try:
    import urllib.request
except ImportError:
    raise ImportError('Please use Python 3.x')

import pickle
import os
import numpy as np


def load_mnist(normalize=True, flatten=True, one_hot_label=False, shapedinto=False, shapedcnn=False):
    with open(save_file, 'rb') as f:
        dataset = pickle.load(f)

    if normalize:
        for key in ('train_img', 'test_img'):
            dataset[key] = dataset[key].astype(np.float32)
            dataset[key] /= 255.0

    if one_hot_label:
        dataset['train_label'] = _change_one_hot_label(dataset['train_label'])
        dataset['test_label'] = _change_one_hot_label(dataset['test_label'])

    if not flatten:
        for key in ('train_img', 'test_img'):
            dataset[key] = dataset[key].reshape(-1, 1, 28, 28)

    if shapedinto:
        for key in ('train_img', 'test_img'):
            dataset[key] = dataset[key].reshape(-1, 28, 28)

    if shapedcnn:
        for key in ('train_img', 'test_img'):
            dataset[key] = dataset[key].reshape(-1, 28, 28, 1)

    return (dataset['train_img'], dataset['train_label']), (dataset['test_img'], dataset['test_label'])


url_base = 'http://yann.lecun.com/exdb/mnist/'
key_file = {
    'train_img': 'train-images-idx3-ubyte.gz',
    'train_label': 'train-labels-idx1-ubyte.gz',
    'test_img': 't10k-images-idx3-ubyte.gz',
    'test_label': 't10k-labels-idx1-ubyte.gz'
}

dataset_dir = os.path.dirname(os.path.abspath(__file__))
save_file = dataset_dir + "/mnist.pkl"

train_num = 60000
test_num = 10000
img_dim = (1, 28, 28)
img_size = 784


def _download(file_name):
    file_path = dataset_dir + "/" + file_name

    if os.path.exists(file_path):
        return

    print("Downloading " + file_name + " ... ")
    urllib.request.urlretrieve(url_base + file_name, file_path)
    print("Done")


def download_mnist():
    for v in key_file.values():
        _download(v)


def _load_label(file_name):
    file_path = dataset_dir + "/" + file_name
    with gzip.open(file_path, 'rb') as f:
        labels = np.frombuffer(f.read(), np.uint8, offset=8)
    print("label就绪")
    return labels


def _load_img(file_name):
    file_path = dataset_dir + "/" + file_name
    with gzip.open(file_path, 'rb') as f:
        data = np.frombuffer(f.read(), np.uint8, offset=16)
    data = data.reshape(-1, img_size)
    print("img就绪")
    return data


def _convert_numpy():
    dataset = {'train_img': _load_img(key_file['train_img']), 'train_label': _load_label(key_file['train_label']),
               'test_img': _load_img(key_file['test_img']), 'test_label': _load_label(key_file['test_label'])}
    return dataset


# 下载数据集
def init_mnist():
    # download_mnist()
    dataset = _convert_numpy()
    with open(save_file, 'wb') as f:
        pickle.dump(dataset, f, -1)
    print("下载完成")


def _change_one_hot_label(x):
    t = np.zeros((x.size, 10))
    for idx, row in enumerate(t):
        row[x[idx]] = 1
    return t
