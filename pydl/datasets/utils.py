import collections
import os
import pandas
import numpy as np


Dataset = collections.namedtuple('Dataset', ['x', 'y'])
Datasets = collections.namedtuple('Datasets', ['train', 'test', 'validation'])


def load_csv(filename, dtype=None, has_header=True, usecols=None, index_col=None):
    return pandas.read_csv(filename,
                           skiprows=0 if has_header else None,
                           index_col=index_col,
                           usecols=usecols,
                           dtype=dtype)


def load_npy(filename):
    return np.load(filename) if filename != '' else None


def load_data_file(filename, **kwargs):
    if filename is '':
        return None
    elif os.path.splitext(filename)[1] == '.csv':
        return load_csv(filename=filename, **kwargs)
    else:
        return load_npy(filename)


def load_dataset(x_path, y_path='', y_dtype=np.float64, has_header=True):
    x = load_data_file(filename=x_path, has_header=has_header)
    y = load_data_file(filename=y_path, dtype=y_dtype, has_header=has_header)
    return Dataset(x=x, y=y)


def load_datasets(train_x,
                  train_y='',
                  test_x='',
                  test_y='',
                  valid_x='',
                  valid_y='',
                  labels_dtype=np.float64,
                  has_header=True):

    """
    """

    assert train_x != ''

    return Datasets(train=load_dataset(train_x, train_y, labels_dtype, has_header),
                    test=load_dataset(test_x, test_y, labels_dtype, has_header),
                    validation=load_dataset(valid_x, valid_y, labels_dtype, has_header))