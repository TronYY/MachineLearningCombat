#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import numpy as np
import matplotlib.pyplot as plt
import random
path = os.getcwd()

# ------使用 Logistic 回归在简单数据集上的分类-----------


def load_data_set():
    """
    加载数据集
    :return:返回两个数组，普通数组 
        data_arr -- 原始数据的特征
        label_arr -- 原始数据的标签，也就是每条样本对应的类别
    """
    data_arr, label_arr = [], []
    with open(path + '/Data/TestSet.txt', 'r') as f:
        for line in f.readlines():
            line_arr = line.strip().split()
            # 为了方便计算，我们将 X0 的值设为 1.0 ，也就是在每一行的开头添加一个 1.0 作为 X0
            data_arr.append(
                [1.0, np.float(line_arr[0]),
                 np.float(line_arr[1])])
            label_arr.append(int(line_arr[2]))
    return data_arr, label_arr


def sigmoid(x):
    # 错误: RuntimeWarning: overflow encountered in exp
    # 解释: 计算出的结果太大，或者太小(要求精度高小数点后N位数之类的)。统称叫溢出，上溢或下溢
    # 解决办法: 使用bigfloat这个库
    return 1.0 / (1 + np.exp(-x))


def grad_ascent(data_mat, class_labels):
    """
    梯度上升法，其实就是因为使用了极大似然估计
    :param data_mat: 数据矩阵
    :param class_labels: class_labels 是类别标签，它是一个 1*100 的行向量。
                    为了便于矩阵计算，需要将该行向量转换为列向量，做法是将原向量转置，再将它赋值给label_mat
    :return: 
    """
    # 变成矩阵之后进行转置
    label_mat = class_labels.transpose()
    # _->数据量，样本数 n->特征数
    _, n = np.shape(data_mat)
    # 学习率
    alpha = 0.001
    # 最大迭代次数
    max_cycles = 500
    # weights 代表回归系数
    weights = np.ones((n, 1))
    for _ in range(max_cycles):
        # 这里是点乘  _ x n dot n x 1
        h = sigmoid(data_mat * weights)
        error = label_mat - h
        # 运用到了最大似然估计。。。
        weights = weights + alpha * data_mat.transpose() * error
    return weights


def stoc_grad_ascent0(data_mat, class_labels):
    """
    随机梯度上升，只使用一个样本点来更新回归系数
    :param data_mat: 输入数据的数据特征（除去最后一列）,ndarray
    :param class_labels: 输入数据的类别标签（最后一列数据）
    :return: 得到的最佳回归系数
    """
    m, n = np.shape(data_mat)
    alpha = 0.001
    weights = np.ones(n)
    for i in range(m):
        # sum(data_mat[i]*weights)为了求 f(x)的值， f(x)=a1*x1+b2*x2+..+nn*xn,
        # 此处求出的 h 是一个具体的数值，而不是一个矩阵)
        h = sigmoid(sum(data_mat[i] * weights))
        error = class_labels[i] - h
        weights = weights + alpha * data_mat[i] * error
    return weights


def stoc_grad_ascent1(data_mat, class_labels, num_iter=150):
    """
    改进版的随机梯度上升，使用随机的一个样本来更新回归系数
    :param data_mat: 输入数据的数据特征（除去最后一列）,ndarray
    :param class_labels: 输入数据的类别标签（最后一列数据
    :param num_iter: 迭代次数
    :return: 得到的最佳回归系数
    """
    m, n = np.shape(data_mat)
    weights = np.ones(n)
    for j in range(num_iter):
        # 随机样本的索引列表
        data_index = list(range(m))
        for i in range(m):
            # i和j的不断增大，导致alpha的值不断减少，但是不为0
            alpha = 4 / (1.0 + j + i) + 0.001
            # 从data_index中随机取一个元素
            rand_index = random.sample(data_index, 1)[0]
            h = sigmoid(np.sum(data_mat[rand_index] * weights))
            error = class_labels[rand_index] - h
            weights = weights + alpha * data_mat[rand_index] * error
            # 移除刚刚取出的元素，因为data_index里面每个元素都是唯一的，所以直接使用remove
            data_index.remove(rand_index)

    return weights


def plot_best_fit(weights):
    """
    可视化
    :param weights: 
    :return: 
    """

    data_mat, label_mat = load_data_set()
    data_arr = np.array(data_mat)
    n = np.shape(data_mat)[0]
    x_cord1, y_cord1 = [], []
    x_cord2, y_cord2 = [], []
    for i in range(n):
        if int(label_mat[i]) == 1:
            x_cord1.append(data_arr[i, 1])
            y_cord1.append(data_arr[i, 2])
        else:
            x_cord2.append(data_arr[i, 1])
            y_cord2.append(data_arr[i, 2])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(x_cord1, y_cord1, s=30, color='k', marker='^')
    ax.scatter(x_cord2, y_cord2, s=30, color='red', marker='s')
    x = np.arange(-3.0, 3.0, 0.1)
    y = (-weights[0] - weights[1] * x) / weights[2]
    """
    y的由来，卧槽，是不是没看懂？
    首先理论上是这个样子的。
    dataMat.append([1.0, float(lineArr[0]), float(lineArr[1])])
    w0*x0+w1*x1+w2*x2=f(x)
    x0最开始就设置为1叻， x2就是我们画图的y值，而f(x)被我们磨合误差给算到w0,w1,w2身上去了
    所以： w0+w1*x+w2*y=0 => y = (-w0-w1*x)/w2   
    """
    ax.plot(x, y)
    plt.xlabel('x1')
    plt.ylabel('y1')
    plt.show()


def test():
    """
    对上面的几个算法的测试
    """
    data_arr, class_labels = load_data_set()
    # 注意，这里的grad_ascent返回的是一个 matrix, 所以要使用getA方法变成ndarray类型
    #    weights = grad_ascent(np.mat(data_arr), np.mat(class_labels)).getA()
    #    weights = stoc_grad_ascent0(np.array(data_arr), class_labels)
    weights = stoc_grad_ascent1(np.array(data_arr), class_labels)
    plot_best_fit(weights)


# -------从疝气病症预测病马的死亡率------


def classify_vector(in_x, weights):
    """
    最终的分类函数，根据回归系数和特征向量来计算 Sigmoid 的值，大于0.5函数返回1，否则返回0
    :param in_x: 特征向量，features
    :param weights: 根据梯度下降/随机梯度下降 计算得到的回归系数
    :return: 
    """
    # print(np.sum(in_x * weights))
    prob = sigmoid(np.sum(in_x * weights))
    if prob > 0.5:
        return 1.0
    return 0.0


def colic_test():
    """
    打开测试集和训练集，并对数据进行格式化处理,其实最主要的的部分，比如缺失值的补充（真的需要学会的），人家已经做了
    :return: 
    """
    # 解析训练数据集中的数据特征和Labels
    # trainingSet 中存储训练数据集的特征，trainingLabels 存储训练数据集的样本对应的分类标签
    training_set, training_labels = [], []
    with open(path + '/Data/HorseColicTraining.txt', 'r') as f_train:
        for line in f_train.readlines():
            curr_line = line.strip().split('\t')
            line_arr = [float(curr_line[i]) for i in range(21)]
            training_set.append(line_arr)
            training_labels.append(float(curr_line[21]))
    # 使用 改进后的 随机梯度下降算法 求得在此数据集上的最佳回归系数 trainWeights
    train_weights = stoc_grad_ascent1(
        np.array(training_set), training_labels, 500)
    error_count, num_test_vec = 0, 0
    # 读取 测试数据集 进行测试，计算分类错误的样本条数和最终的错误率
    with open(path + '/Data/HorseColicTest.txt', 'r') as f_test:
        for line in f_test.readlines():
            num_test_vec += 1
            curr_line = line.strip().split('\t')
            line_arr = [float(curr_line[i]) for i in range(21)]
            if int(classify_vector(np.array(line_arr), train_weights)) != int(
                    curr_line[21]):
                error_count += 1
    error_rate = error_count / num_test_vec
    print('the error rate is {}'.format(error_rate))
    return error_rate


def multi_test():
    """
    调用 colicTest() 10次并求结果的平均值
    :return: nothing 
    """
    num_tests = 10
    error_sum = 0
    for _ in range(num_tests):
        error_sum += colic_test()
    print('after {} iteration the average error rate is {}'.format(
        num_tests, error_sum / num_tests))


if __name__ == '__main__':
    # test()
    # colic_test()
    # multi_test()
    pass
