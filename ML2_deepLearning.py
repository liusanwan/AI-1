# tensorflow框架 深度学习神经网络

from loadDataJson import extractTrainData
import tflearn
from tflearn.data_utils import load_csv


def loadDataJson(url):

    # 加载文件夹
    data, labels = load_csv(url, target_column=10, columns_to_ignore=[
        0], has_header=True, categorical_labels=True, n_classes=2)
    # data, labels = load_csv(url, target_column=1, columns_to_ignore=[
    #                         0], has_header=True, categorical_labels=True, n_classes=2)
    return data, labels


# def DNN_tf(train_x, train_y, test_x, test_y, n_layer_1=4, n_layer_2=2, n_layer_3=1):
#     # train_set=[[x11,x12,x13,x14,x15],
#     #            [x21,x22,x23,x24,x25],
#     #            ...,
#     #            [xn1,xn2,xn3,xn4,xn5]]

#     # 深度神经网络
#     # 设置深度神经网络的一些参数
#     learning_rate = 0.001               # 学习率
#     times = 500                         # 迭代次数
#     batch_size = 25                     # 一次迭代的训练集大小
#     feature_size = len(train_x[0])    # 传入参数
#     print("完成！")

######################################################
# 尝试使用 tfLearn


def DNN_tfLearn(train_x, train_y,  n_layer_1=4, n_layer_2=4, n_layer_3=4, output=2):
    # 使用tfLearn编写全连接神经网络
    # Define network
    inputData = tflearn.input_data(shape=[None, 9])
    layer_1 = tflearn.fully_connected(
        inputData, 32, activation='sigmoid', name='layer_1')
    layer_2 = tflearn.fully_connected(
        layer_1, 108, activation='sigmoid', name='layer_2')
    layer_3 = tflearn.fully_connected(
        layer_2, 64, activation='sigmoid', name='layer_3')
    outputData = tflearn.fully_connected(
        layer_3, 2, activation='softmax', name='output')
    net = tflearn.regression(outputData)

    # Define model
    model = tflearn.DNN(net, best_checkpoint_path='model_breast_cancer',
                        max_checkpoints=1, tensorboard_verbose=0)

    # Start training (apply gradient descent algorithm)
    model.fit(data, labels, n_epoch=10, validation_set=0.2, shuffle=True,
              batch_size=len(data), show_metric=True, run_id='breast_cancer')

    # Record best parameters    layer_1_vars[0]--第一层的weights; layer_2_vars[1]--第二层的biases
    layer_1_vars = tflearn.variables.get_layer_variables_by_name('layer_1')
    layer_2_vars = tflearn.variables.get_layer_variables_by_name('layer_2')
    layer_3_vars = tflearn.variables.get_layer_variables_by_name('layer_3')
    output_vars = tflearn.variables.get_layer_variables_by_name('output')
    print("1--output:", outputData)
    print("2--")
    #print("2--output:", tflearn.variables.get_value(outputData[0]))

    with model.session.as_default():
        print(tflearn.variables.get_value(layer_1_vars[0]))
        print(tflearn.variables.get_value(layer_2_vars[0]))
        print(tflearn.variables.get_value(layer_3_vars[0]))
        print("output[1]", tflearn.variables.get_value(output_vars[1]))
    return 0
#######################################################


def tf_tran(data):
    x = []
    y = []
    for i in data:
        temp_res = []
        temp_res.append(i["mid_dist"])
        temp_res.append(i["nearest_dist"])
        temp_res.append(i["anceMatchRate"])
        temp_res.append(i["contMatchRate"])
        temp_res.append(i["row"])
        x.append(temp_res)
        temp_label = []
        temp_label.append(int(i["ifMatch"]))
        y.append(temp_label)
    return x, y


def tf_tran2(data):
    x = []
    y = []
    for i in data:
        temp_res = []
        temp_res.append(i["mid_dist"])
        temp_res.append(i["nearest_dist"])
        temp_res.append(i["anceMatchRate"])
        temp_res.append(i["contMatchRate"])
        temp_res.append(i["row"])
        x.append(temp_res)
        y.append(int(i["ifMatch"]))
    return x, y


if __name__ == '__main__':
    data, labels = loadDataJson('dataset/tfLearn_data/data3.csv')
    # 第一步：获取信息
    # train_data = extractTrainData(
    #     'dataset/demo_data/test7/trainData_part2.txt')
    # test_data = extractTrainData(
    #     'dataset/demo_data/test6_testdata/testData.txt')

    # # 将输入数据调整为tf格式
    # train_x, train_y = tf_tran(train_data)
    # test_x, test_y = tf_tran(test_data)
    # train_x = pd.DataFrame(data=train_x)
    # train_y = pd.DataFrame(data=train_y)
    # train_x.to_csv('dataset/tfLearn_data/data1.csv', encoding='utf-8')
    # train_y.to_csv('dataset/tfLearn_data/data2.csv', encoding='utf-8')

    DNN_tfLearn(data, labels,
                n_layer_1=4, n_layer_2=4, n_layer_3=4, output=2)
    #DNN_tf(train_x, train_y, test_x, test_y, 4, 4, 2)
