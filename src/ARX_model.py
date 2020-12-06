import matplotlib.pyplot as plt
import matplotlib as mpl
import math
import pandas as pd
import numpy as np
import copy
# 우선 n_a > n_b 라고 가정하자


def make_y_t(output_data, n_a):
    y_t = []
    for i in range(n_a, len(output_data)):
        y_t.append([output_data[i]])
    return np.array(y_t)


def make_pi_matrix(input_data, output_data, n_a, n_b):
    y_start = n_a - 1
    u_start = n_a - 1
    pi = []
    for i in range(len(output_data) - n_a):
        im = []
        for j in range(n_a):
            im.append(-1 * output_data[y_start - j])
        for j in range(n_b):
            im.append(input_data[u_start - j])
        pi.append(copy.deepcopy(im))
        y_start = y_start + 1
        u_start = u_start + 1

    return np.array(pi)


# def make_result(input_data, output_data, ans_a, ans_b, n_a, n_b):
#     t = 0
#     result = []
#     for k in range(len(input_data)):
#         im = 0
#         cnt_b = n_b-1
#         cnt_a = n_a-1
#         for i in range(t-n_b, t-1):
#             if i < 0:
#                 pass
#             else:
#                 im = im + ans_b[cnt_b] * input_data[i]
#             cnt_b = cnt_b-1
#         for i in range(t-n_a, t-1):
#             if i < 0:
#                 pass
#             else:
#                 im = im - ans_a[cnt_a] * result[i]
#             cnt_a = cnt_a-1
#         result.append(im)
#         t = t+1
#     return result


def ARX(input_data, output_data, n_a, n_b):
    y_t = make_y_t(output_data, n_a)
    pi = make_pi_matrix(input_data, output_data, n_a, n_b)
    pi_persudo = np.linalg.pinv(pi)
    ans = np.dot(pi_persudo, y_t)
    front = [0]
    for i in range(1, n_b+1):
        im = 0
        cnt = 0
        for j in range(i, 0, -1):
            im = im + input_data[cnt] * ans[n_a + j - 1][0]
            cnt = cnt+1
        front.append(0)  # 원래 im인데 뭔가 이상한거같아가지고
    front = np.array(front)
    result = np.dot(pi, ans)
    result = np.append(front, result)
    return result
