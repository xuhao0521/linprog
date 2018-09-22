# encode: utf8

import sys
import numpy as np
from scipy import linalg

from utils import *

def conv_piv(vec):
    num = len(vec)
    raw = range(num)
    for i in range(num-1):
        trn = raw[vec[i]]
        raw[vec[i]] = raw[i]
        raw[i] = trn
    return raw


def inv_piv(piv):
    num = len(piv)
    inv = [0] * num
    for i in range(num):
        inv[piv[i]] = i
    return inv


def swap_row(mat, k, j):
    tmp = mat.take(k, axis=0)
    mat[k] = mat[j]
    mat[j] = tmp


def calc_lu_lower(lu, out, piv_ind, trn_val):
    size = lu.shape[0]
    Lt = np.tril(lu, -1).T + np.eye(size)
    i = 0
    for k in range(out, size - 1):
        piv = piv_ind[i]
        trn = trn_val[i]
        Lt[k][k+1:] -= Lt[k+1][k+1:] * trn
        i += 1
    return Lt.T


def lu_update_col(lu, out, col_in):
    is_big_num = lambda x: x >= 1e3
    size = lu.shape[0]
    h_L = linalg.solve_triangular(lu, col_in, lower=True, unit_diagonal=True)
    Ut = np.triu(lu).T
    H = np.row_stack((Ut[0:out], Ut[out+1:], h_L)).T
    piv_ind = []
    trn_val = []
    for k in range(out, size-1):
        if is_zero(H[k, k]) and is_zero(H[k+1, k]):
            piv_ind.append(k)
            trn_val.append(0)
            continue
        if is_zero(H[k, k]) or is_big_num(H[k, k+1] / H[k, k]):
            swap_row(H, k, k+1)
            piv_ind.append(k+1)
        else:
            piv_ind.append(k)
        trn = -H[k+1, k] / H[k, k]
        #H[k+1][k] = 0
        #H[k+1][k+1:] += H[k][k+1:] * trn
        H[k+1][k:] += H[k][k:] * trn
        trn_val.append(trn)
    return H, piv_ind, trn_val


