#!/usr/bin/python
# coding:utf8

'''
Created on 2017-03-08
Update  on 2017-05-18
Tree-Based Regression Methods Source Code for Machine Learning in Action Ch. 9
@author: Peter/片刻
《机器学习实战》更新地址：https://github.com/apachecn/MachineLearning
'''
import regTrees
import numpy as np
# from Tkinter import *
import tkinter as tk
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
matplotlib.use('TkAgg')


def test_widget_text(root):
    mylabel = tk.Label(root, text="helloworld")
    # 相当于告诉 布局管理器(Geometry Manager),如果不设定位置，默认在 0行0列的位置
    mylabel.grid()


# 最大为误差， 最大子叶节点的数量
def reDraw(tolS, tolN):
    # clear the figure
    reDraw.f.clf()
    reDraw.a = reDraw.f.add_subplot(111)

    # 检查复选框是否选中
    if chkBtnVar.get():
        if tolN < 2:
            tolN = 2
        myTree = regTrees.createTree(reDraw.rawDat, regTrees.modelLeaf, regTrees.modelErr, (tolS, tolN))
        yHat = regTrees.createForeCast(myTree, reDraw.testDat, regTrees.modelTreeEval)
    else:
        myTree = regTrees.createTree(reDraw.rawDat, ops=(tolS, tolN))
        yHat = regTrees.createForeCast(myTree, reDraw.testDat)

    # use scatter for data set
    reDraw.a.scatter(reDraw.rawDat[:, 0], reDraw.rawDat[:, 1], s=5)
    # use plot for yHat
    reDraw.a.plot(reDraw.testDat, yHat, linewidth=2.0, c='red')
    reDraw.canvas.show()


def getInputs():
    try:
        tolN = int(tolNentry.get())
    except:
        tolN = 10
        print("enter Integer for tolN")
        tolNentry.delete(0, tk.END)
        tolNentry.insert(0, '10')
    try:
        tolS = float(tolSentry.get())
    except:
        tolS = 1.0
        print("enter Float for tolS")
        tolSentry.delete(0, tk.END)
        tolSentry.insert(0, '1.0')
    return tolN, tolS


# 画新的tree
def drawNewTree():
    # #get values from Entry boxes
    tolN, tolS = getInputs()
    reDraw(tolS, tolN)


def main(root):
    # 标题
    tk.Label(root, text="Plot Place Holder").grid(row=0, columnspan=3)
    # 输入栏1, 叶子的数量
    tk.Label(root, text="tolN").grid(row=1, column=0)
    global tolNentry
    tolNentry = tk.Entry(root)
    tolNentry.grid(row=1, column=1)
    tolNentry.insert(0, '10')
    # 输入栏2, 误差量
    tk.Label(root, text="tolS").grid(row=2, column=0)
    global tolSentry
    tolSentry = tk.Entry(root)
    tolSentry.grid(row=2, column=1)
    # 设置输出值
    tolSentry.insert(0,'1.0')

    # 设置提交的按钮
    tk.Button(root, text="确定", command=drawNewTree).grid(row=1, column=2, rowspan=3)

    # 设置复选按钮
    global chkBtnVar
    chkBtnVar = tk.IntVar()
    chkBtn = tk.Checkbutton(root, text="Model Tree", variable = chkBtnVar)
    chkBtn.grid(row=3, column=0, columnspan=2)

    # 退出按钮
    tk.Button(root, text="退出", fg="black", command=quit).grid(row=1, column=2)

    # 创建一个画板 canvas
    reDraw.f = Figure(figsize=(5, 4), dpi=100)
    reDraw.canvas = FigureCanvasTkAgg(reDraw.f, master=root)
    reDraw.canvas.show()
    reDraw.canvas.get_tk_widget().grid(row=0, columnspan=3)

    reDraw.rawDat = np.mat(regTrees.loadDataSet('testData/RT_sine.txt'))
    reDraw.testDat = np.arange(min(reDraw.rawDat[:, 0]), max(reDraw.rawDat[:, 0]), 0.01)
    reDraw(1.0, 10)


if __name__ == "__main__":

    # 创建一个事件
    root = tk.Tk()
    # test_widget_text(root)
    main(root)

    # 启动事件循环
    root.mainloop()
