from tqdm import tqdm
import numpy as np
cimport numpy as np
cimport cython

ctypedef np.int64_t DTYPE_t

def calculate(str row, str column, int alpha):
    """ Smith Waterman algorithm

    Parameters
    ------------
    row : str
        Row comparison string
    column : str
        Column comparison string

    Returns
    ------------
    row_similar_parts : list
        List of similar parts of row
    column_similar_parts : list
        List of similar parts of column

    """
    cdef:
        np.ndarray[DTYPE_t, ndim=2] v = np.zeros([len(row)+1, len(column)+1], dtype=np.int)
        row_index_array = np.zeros(len(row))
        column_index_array = np.zeros(len(column))
        int match = 1
        int mis = -1
        int gap = -1
        int s = 0
        int traceback_score = 0
        int tb_i = 0, tb_j = 0
        int i = 0, j = 0

    for m in tqdm(range(1, len(row)+1)):
        for n in range(1, len(column)+1):
            if row[m-1] == column[n-1]:
                s = match
            else:
                s = mis
            cell_score = []
            cell_score.append(v[m-1,n-1] + s)
            cell_score.append(v[m-1,n] + gap)
            cell_score.append(v[m,n-1] + gap)
            cell_score.append(0)
            v[m,n] = max(cell_score)

    while v[len(row), len(column)] != -1:
        traceback_score = 0
        tb_i, tb_j = 0, 0

        # find the maximum score and its coordinate
        for m in range(1, len(row)+1):
            for n in range(1, len(column)+1):
                if v[m,n] > 0 and row[m-1] == column[n-1] and v[m,n] >= traceback_score:
                    traceback_score = v[m,n]
                    tb_i, tb_j = m, n

        # can't find the maximum score
        if traceback_score < alpha or tb_i == 0 and tb_j == 0:
            if column_index_array.any() == False:
                print("InputError: This document is not copied.")
            break

        # traceback
        i, j = tb_i, tb_j
        while True:
            v[i,j] = -1
            if v[i-1,j] >= v[i-1,j-1] and v[i-1,j] >= v[i,j-1] and v[i-1,j] > 0:
                i = i-1
            elif v[i,j-1] >= v[i-1,j-1] and v[i,j-1] >= v[i-1,j] and v[i,j-1] > 0:
                j = j-1
            elif v[i-1,j-1] >= v[i,j-1] and v[i-1,j-1] >= v[i-1,j] and v[i-1,j-1] > 0:
                i = i-1
                j = j-1
            elif v[i-1,j] == 0 and v[i,j-1] == 0 and v[i-1,j-1] == 0:
                break
            elif v[i-1,j] == -1 or v[i,j-1] == -1 or v[i-1,j-1] == -1:
                break

        # set outside the search range
        for k in range(0, len(row)+1):
            for l in range(j, tb_j+1):
                v[k,l] = -1

        # save similar sentences
        for di in range(i-1, tb_i):
            row_index_array[di] = 1
        for dj in range(j-1, tb_j):
            column_index_array[dj] = 1

    return row_index_array, column_index_array
