# coding:utf-8
# # 本文档用于编写机器学习
import random
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from bingoRate import bingoRate
plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 解决负号“-”显示为方块的问题
# 1.0版本 使用 逻辑回归
# 输入参数 [(id, mid_dist, nearest_dist, anceMatchRate, contMatchRate, true/false),...]
# 输出结果： 一个最有可能匹配的标签

train_rate = 0.8  # 训练集train占总数据集比例


def ord_split(data_arr, rate):
    return data_arr[:int(len(data_arr)*rate)], data_arr[int(len(data_arr)*rate):]


def rand_split(data_arr, rate):
    train_set = []
    test_set = []
    for i in data_arr:
        if random.random() < rate:
            train_set.append(i)
        else:
            test_set.append(i)
    return train_set, test_set


def sigmoid(num):
    return 1/(1+tf.exp(-num))


def drawGraph(bingo_rate, loss_set, sig_lists, nA1B_bingo_rate, valve):
    # 画图
    plt.figure(figsize=(10, 6))
    plt.rcParams['figure.figsize'] = (8.0, 4.0)
    plt.subplot(331)
    plt.plot(bingo_rate)
    plt.xlabel("迭代次数")
    plt.ylabel("命中率")
    plt.subplot(332)
    plt.plot(loss_set)
    plt.xlabel("迭代次数")
    plt.ylabel("loss值")
    plt.subplot(333)
    plt.plot(nA1B_bingo_rate)
    plt.xlabel("迭代次数")
    plt.ylabel("nA命中率")
    # 第一阶段的展示
    plt.subplot(334)
    plt.hist(x=sig_lists[0], bins=100)
    plt.xlabel("sig值")
    plt.ylabel("样本数量")
    plt.axvline(valve, c="r", ls="--", lw=1)
    # 第二阶段的展示
    plt.subplot(335)
    plt.hist(x=sig_lists[1], bins=100)
    # plt.xlabel("sig值")
    # plt.ylabel("样本数量")
    plt.axvline(valve, c="r", ls="--", lw=1)
    # 第三阶段的展示
    plt.subplot(336)
    plt.hist(x=sig_lists[2], bins=100)
    # plt.xlabel("sig值")
    # plt.ylabel("样本数量")
    plt.axvline(valve, c="r", ls="--", lw=1)
    # 第四阶段的展示
    plt.subplot(337)
    plt.hist(x=sig_lists[3], bins=100)
    plt.xlabel("sig值")
    plt.ylabel("样本数量")
    plt.axvline(valve, c="r", ls="--", lw=1)
    # 第五阶段的展示
    plt.subplot(338)
    plt.hist(x=sig_lists[4], bins=100)
    plt.xlabel("sig值")
    # plt.ylabel("样本数量")
    plt.axvline(valve, c="r", ls="--", lw=1)
    # 第六阶段的展示
    plt.subplot(339)
    plt.hist(x=sig_lists[5], bins=100)
    plt.xlabel("sig值")
    # plt.ylabel("样本数量")
    plt.axvline(valve, c="r", ls="--", lw=1)

    plt.show()


def logistic_hand(train_set, test_set, nA1B_url):
    # 手写逻辑回归模型
    # 输入参数：
    # train_set/test_set:[[x1,x2,x3,x4,y],...]
    # 1.返回数据:一个元素为int的列表, 每个 int 代表测试集中每一对逻辑回归的概率值
    # 2.画出不同训练时期的 test_set 的命中率
    res = []
    # 第一步：将data与label分离
    test_data, test_label = test_set[..., :-1], test_set[..., -1]
    print("test_data in logistic_hand:", test_data)
    print("test_label in logistic_hand:", test_label)
    # 第二步：建立逻辑回归模型
    valve = 0.68        # 判断rel为 1的阈值
    alpha = 0.01    # 学习率
    batch_size = 5   # 每次学习的样本个数
    times = 1000      # 学习次数
    # function y = w^T*x+b
    w = np.array([-1, -1, 1, 1, 1])
    b = np.random.rand()
    # 每次迭代测试集的命中率
    bingo_rate = []
    # 训练集每次迭代的损失值
    loss_set = []
    # 需要记录并用来展示的数据

    true_bingo = 0
    false_bingo = 0
    true_num = 0
    false_num = 0
    sig_lists = []
    nA1B_bingo_rate = []

    # 新建数据导出文档
    f = open('best_para_w_b.txt', mode='w')
    # 待导出的最优参数
    best_obj = {"w": [],
                "b": [],
                "bingoNum": -1,
                "allNum": -1}
    # 第三步：使用train_set进行训练(随机批量)
    for i in range(times):
        # 随机选取 batch_size 个训练样本
        batch_data = random.sample(list(train_set), batch_size)
        # 拆分参数与标签
        batch_data = np.array(batch_data)
        batch_para = batch_data[..., :-1]
        batch_label = batch_data[..., -1]
        sig = np.zeros(batch_size)
        val = []
        for j in range(batch_size):
            val = w*(batch_para[j].T)+b
            sig[j] = sigmoid(sum(val))
        # 计算训练集的 Loss
        Loss = 0
        for j in range(batch_size):
            Loss += batch_label[j]*np.log(sig[j]) + \
                (1-batch_label[j])*np.log(1-sig[j])
        Loss = -1/batch_size*Loss
        loss_set.append(Loss)
        # 计算Grad=[g1,g2,g3,g4]
        g_temp = 0
        for j in range(batch_size):
            g_temp += sig[j]-batch_label[j]
        Grad = g_temp*val
        # 更新参数
        w = w-alpha/batch_size*Grad
        b = b-alpha/batch_size*Grad
        bingo = 0

        temp_sig = []
        exp_List = []
        # 第四步：使用test_set进行测试
        for j in range(len(test_data)):
            val = w*(test_data[j].T)+b
            sig = sigmoid(sum(val))
            if sig >= valve and test_label[j] == 1:
                bingo += 1
            elif sig < valve and test_label[j] == 0:
                bingo += 1
            if i == times-1:
                # print("bingo_num:", bingo, "   all:", len(test_data))
                if test_label[j] == 1:
                    true_num += 1
                    if sig >= valve:
                        true_bingo += 1
                if test_label[j] == 0:
                    false_num += 1
                    if sig < valve:
                        false_bingo += 1
            # 存储阶段性sig值
            if i in [0, int(1*times/5), int(2*times/5), int(3*times/5), int(4*times/5), times-1]:
                temp_sig.append(float(sig))
        # 使用 nAs_1B进行测试
        bingoNum, allNum = bingoRate(nA1B_url, w, b, 0.75)
        # 如果 bingoNum == allNum，将此数据存入待导出队列
        if bingoNum == allNum:
            object = {"w": list(w),
                      "b": list(b),
                      "bingoNum": bingoNum,
                      "allNum": allNum}
            exp_List.append(str(object)+"\n")
        # 存最优参数信息
        if bingoNum > best_obj["bingoNum"]:
            best_obj["w"] = list(w)
            best_obj["b"] = list(b)
            best_obj["bingoNum"] = bingoNum
            best_obj["allNum"] = allNum

        nA1B_bingo_rate.append(float(bingoNum/allNum))
        if len(temp_sig) != 0:
            sig_lists.append(temp_sig)
        bingo_rate.append(bingo/len(test_data))
    # 如果 sig_lists为空，导出最优效果的参数信息
    print("best_obj:", best_obj)
    print("exp_List:", exp_List)
    if len(exp_List) == 0:
        f.write(str(best_obj))
    else:
        f.writelines(exp_List)
    f.close()
    # 查看 true_bingo_rate
    # 查看 false_bingo_rate
    # 查看 true result 的正确率
    print("true_num:", true_num, "  true_bingo:", true_bingo,
          "  true_bingo_rate:", true_bingo/true_num)
    print("false_num:", false_num, "  false_bingo:", false_bingo,
          "  false_bingo_rate:", false_bingo/false_num)
    print("w:", w)
    print("b:", b)

    # 第五步：画图
    drawGraph(bingo_rate, loss_set, sig_lists, nA1B_bingo_rate, valve)

    return res

###########################################################
# 以下是使用tensorflow编写的逻辑回归
###########################################################


def logistic_regression(x, w, b):
    x = tf.cast(x, dtype='float32')
    lr = tf.add(tf.matmul(w, x, transpose_b=True), b)
    return tf.nn.sigmoid(lr)


def cross_entropy(train_label, y):
    print("train_label:", train_label, "  y:", y)
    # loss = tf.nn.softmax_cross_entropy_with_logits(
    #     labels=train_label, logits=y)
    train_label = tf.cast(train_label, dtype='float32')
    loss = -tf.reduce_sum(train_label*tf.math.log(y))

    Loss = train_label*np.log(y) + (1-train_label)*np.log(1-y)
    print("loss in cross_entropy:", Loss)
    return tf.reduce_mean(Loss)


def accuracy(test_label, y):
    test_label = tf.cast(test_label, dtype=tf.int32)
    preds = tf.cast(tf.argmax(y, axis=1), dtype=tf.int32)
    preds = tf.equal(test_label, preds)
    return tf.reduce_mean(tf.cast(preds, dtype=tf.float32))


def grad(x, y, w, b, optimizer):
    loss_val = 0
    with tf.GradientTape() as tape:
        y_pred = logistic_regression(x, w, b)

        loss_val = cross_entropy(y, y_pred)
    print("loss_val:", loss_val)
    # 计算梯度
    gradients = tape.gradient(loss_val, [w, b])
    print("gradients：", gradients)
    # 根据gradients更新 w 和 b
    optimizer.apply_gradients(zip(gradients, [w, b]))
    return loss_val, w, b


def logistic_tf(train_set, test_set):
    # 输入参数：
    # train_set/test_set:[[x1,x2,x3,x4,y],...]
    # 1.返回数据:一个元素为int的列表, 每个 int 代表测试集中每一对逻辑回归的概率值
    # 2.画出不同训练时期的 test_set 的命中率
    res = []

    # 第一步：设置参数
    alpha = 1.0     # 学习率
    batch_size = 5  # 每次学习的样本个数
    times = 500     # 学习次数

    # 初始化w，b
    w = tf.Variable(tf.random.normal(
        shape=(1, len(train_set[0])-1), dtype=tf.float32))
    b = tf.Variable(tf.random.normal(shape=(1, 1), dtype=tf.float32))

    # 随机梯度下降优化器
    optimizer = tf.optimizers.SGD(alpha)

    # 将 train_set的数据格式变为tf.matrix, 并打乱
    train_set = tf.random.shuffle(tf.Variable(train_set), seed=None)
    # 将 参数 与 标签 分开
    loss = []

    # train_set开始训练
    for i in range(times):
        # 选取训练集：每次的训练规模是batch_size
        train_temp = random.sample(list(train_set), batch_size)
        train_temp = np.array(train_temp)
        test_data, test_label = train_temp[..., :-1], train_temp[..., -1]
        # 训练
        for j in range(batch_size):
            loss_temp, w, b = grad(test_data, test_label, w, b, optimizer)
            print("w:", w)
            print("loss_temp:", loss_temp)
            loss.append(loss_temp)
            # 使用测试集进行测试 命中率

    # 画图
    drawGraph([], loss)
    return res

###########################################################
# 以下是使用tensorflow编写的逻辑回归深度神经网络
###########################################################


def logistic_dn(train_set, test_set):
    res = []

    return res


def splitSets(data, rate=0.8):
    # 分割训练集和测试集
    # data={
    #   mid_dist: XXX,
    #   nearest_dist: XXX,
    #   anceMatchRate: XXX,
    #   contMatchRate: XXX,
    #   row: -1 or 1,           # -1 -- A在B的左边，1 -- A在B的右边
    #   ifMatch: True or False
    #  }
    data_arr = np.zeros((len(data), 6))
    # 打乱数据集
    np.random.shuffle(data)
    # 赋值
    for i in range(len(data)):
        data_arr[i][0] = data[i]["mid_dist"]
        data_arr[i][1] = data[i]["nearest_dist"]
        data_arr[i][2] = data[i]["anceMatchRate"]
        data_arr[i][3] = data[i]["contMatchRate"]
        data_arr[i][4] = data[i]["row"]
        # data_arr[i][5] = data[i]["col"]
        data_arr[i][5] = data[i]["ifMatch"]
    # train_set 和 test_set 分割
    # 顺序切割
    train_set, test_set = ord_split(data_arr, rate)
    # 随机切割
    # train_set, test_set = rand_split(data_arr, train_rate)

    return train_set, test_set


def translate(data):
    # data={
    #   mid_dist: XXX,
    #   nearest_dist: XXX,
    #   anceMatchRate: XXX,
    #   contMatchRate: XXX,
    #   row: -1 or 1,           # -1 -- A在B的左边，1 -- A在B的右边
    #   ifMatch: True or False
    #  }
    data_arr = np.zeros((len(data), 6))
    # 打乱数据集
    np.random.shuffle(data)
    # 赋值
    for i in range(len(data)):
        data_arr[i][0] = data[i]["mid_dist"]
        data_arr[i][1] = data[i]["nearest_dist"]
        data_arr[i][2] = data[i]["anceMatchRate"]
        data_arr[i][3] = data[i]["contMatchRate"]
        data_arr[i][4] = data[i]["row"]
        data_arr[i][5] = data[i]["ifMatch"]
    return data_arr


def getBestId(trainData, testData, nA1B_url):

    # 第一步：划分数据集（train_rate--划分比例）
    # trainData, testData = splitSets(trainData, train_rate)
    # 如果不需要从训练集里面划分数据集，使用translate()
    trainData = translate(trainData)
    testData = translate(testData)

    # 第二步：调用想要的逻辑回归函数
    # logistic_hand()--手写逻辑回归公式
    # logistic_dn()--神经网络逻辑回归框架
    pro_set = logistic_hand(trainData, testData, nA1B_url)
    # pro_set = logistic_dn(train_set, test_set)

    return pro_set
