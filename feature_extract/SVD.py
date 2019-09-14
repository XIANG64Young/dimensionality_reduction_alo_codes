# coding:utf-8
import numpy as np
import sys
sys.path.append('..')

from decoraters import *
'''
author: heucoder
email: 812860165@qq.com
date: 2019.6.13
'''
@check
def SVD(data):
    '''
    :param data:
    :return: U, Sigma, VT
    '''

    # mean
    N, D = data.shape
    data = data - np.mean(data, axis=0)

    # V
    Veig_val, Veig_vector = np.linalg.eigh(np.dot(data.T, data))
    VT = Veig_vector[:, np.argsort(-abs(Veig_val))].T

    # U
    Ueig_val, Ueig_vector = np.linalg.eigh(np.dot(data, data.T))
    U = Ueig_vector[:, np.argsort(-abs(Ueig_val))]

    # Sigma
    Sigma = np.zeros((N, D))
    for i in range(D):
        Sigma[i, i] = np.dot(data, VT[i])[i]/U[i,i]

    return U, Sigma, VT


