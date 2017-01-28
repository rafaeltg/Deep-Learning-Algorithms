import os

import numpy as np

from pydl.models.autoencoder_models.deep_autoencoder import DeepAutoencoder


def run_deep_ae():

    """
        Deep Autoencoder example
    """

    # Create fake dataset
    input_dim = 20
    train_size = 2000
    test_size = 200
    x_train = np.random.normal(loc=0, scale=1, size=(train_size, input_dim))
    x_test = np.random.normal(loc=0, scale=1, size=(test_size, input_dim))

    print('Creating Deep Autoencoder')
    hidden_size = 15
    deep_ae = DeepAutoencoder(
        n_hidden=[30, 20, hidden_size],
        num_epochs=400
    )

    print('Training')
    deep_ae.fit(x_train=x_train)

    train_score = deep_ae.score(data=x_train)
    print('Reconstruction loss for training dataset = {}'.format(train_score))

    test_score = deep_ae.score(data=x_test)
    print('Reconstruction loss for test dataset = {}'.format(test_score))

    print('Transforming data')
    x_test_tr = deep_ae.transform(data=x_test)
    print('Transformed data shape = {}'.format(x_test_tr.shape))
    assert x_test_tr.shape == (test_size, hidden_size)

    print('Reconstructing data')
    x_test_rec = deep_ae.reconstruct(x_test_tr)
    print('Reconstructed data shape = {}'.format(x_test_rec.shape))
    assert x_test_rec.shape == x_test.shape

    print('Saving model')
    deep_ae.save_model('/home/rafael/models/dae.h5')
    assert os.path.exists('/home/rafael/models/dae.h5')

    print('Loading model')
    deep_ae_new = DeepAutoencoder(
        n_hidden=[30, 20, hidden_size],
        num_epochs=400
    )

    deep_ae_new.load_model('/home/rafael/models/dae.h5')

    print('Transforming data')
    x_test_tr_new = deep_ae_new.transform(data=x_test)
    assert np.array_equal(x_test_tr, x_test_tr_new)

    print('Reconstructing data')
    x_test_rec_new = deep_ae_new.reconstruct(x_test_tr_new)
    assert np.array_equal(x_test_rec, x_test_rec_new)

    print('Calculating training set score')
    train_score_new = deep_ae_new.score(data=x_train)
    assert train_score == train_score_new

    print('Calculating testing set score')
    test_score_new = deep_ae_new.score(data=x_test)
    assert test_score == test_score_new


if __name__ == '__main__':
    run_deep_ae()