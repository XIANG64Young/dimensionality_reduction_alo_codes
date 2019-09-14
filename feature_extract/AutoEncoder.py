# coding:utf-8
import numpy as np
import tensorflow as tf

'''
author: heucoder
email: 812860165@qq.com
date: 2019.9.12
update: 2019.9.12
'''

def reset_graph(seed=42):
    '''
    reset deafault graph
    :param seed: random seed
    :return:
    '''
    tf.reset_default_graph()
    tf.set_random_seed(seed)
    np.random.seed(seed)

def AutoEncoder(data,
                hidden_layers = None,
                noise = 0,
                drop_rate = 0,
                n_epochs = 301,
                learning_rate = 0.01,
                optimizer_type = 'adam',
                verbose = 1):
    '''

    :param data: (n_samples, n_features)
    :param hidden_layers: list hidden layers units num
    :param noise: normal noise
    :param drop_rate:
    :param n_epochs:
    :param learning_rate:
    :param optimizer_type:
    :param verbose:
    :return:
    '''


    reset_graph()
    n_inputs = data.shape[1]
    n_outputs = n_inputs

    X = tf.placeholder(tf.float32, shape=[None, n_inputs])

    # add noise
    X_noise = X + noise * tf.random_normal(tf.shape(X))

    # dropout
    training = tf.placeholder_with_default(False, shape=(), name = "training")
    X_drop = tf.layers.dropout(X_noise, drop_rate, training=training)

    hiddens = [X_drop]
    for i in range(len(hidden_layers)):
        n_layer = hidden_layers[i]
        hidden = tf.layers.dense(hiddens[i], n_layer, )
        hiddens.append(hidden)

    outputs = tf.layers.dense(hiddens[-1], n_outputs)
    hiddens.append(outputs)

    reconstruction_loss = tf.reduce_mean(tf.square(outputs - X))

    if optimizer_type == 'adam':
        optimizer = tf.train.AdamOptimizer(learning_rate)
    else:
        optimizer = tf.train.GradientDescentOptimizer(learning_rate)

    training_op = optimizer.minimize(reconstruction_loss)

    init = tf.global_variables_initializer()

    # coding layer
    codings = hiddens[len(hiddens)//2]

    with tf.Session() as sess:
        init.run()
        for epoch in range(n_epochs):
            sess.run(training_op, feed_dict={X: data, training: True})
            loss_train = reconstruction_loss.eval(feed_dict={X: data})
            if epoch % 100 == 0 and verbose:
                print("\r{}".format(epoch), "Train MSE:", loss_train)
        data_ndim = codings.eval(feed_dict={X: data})

    return data_ndim
