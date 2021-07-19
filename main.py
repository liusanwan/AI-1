# coding:utf-8
from loadDataJson import extractTrainData
from ML2_logistic import getBestId

# 项目的main文件
# 传入参数：{A1,A2,A3,A4,B}
# 传入参数_1：A--文本组件
# A = {
#     position: {
#         left_up : (x_l, y_l),
#         right_down : (x_r, y_r)
#     },
#     xpath:"XXXXX"
#     },
#     context:{
#         data:"XXXXX"
#     }
# }
# 传入参数_2：B--交互组件
# B = {
#     position: {
#         left_up : (x_l, y_l),
#         right_down : (x_r, y_r)
#     },
#     xpath:"XXXXX"
#     },
#     context:{
#         data:"XXXXX"
#     }
# }
# 传入参数_3：rel--是否相关
# rel=True or False


# Demo版本--针对一个A组件，判断传入的B组件是否与其想对应：
# 如果B与A对应，则返回true，反之返回false；

# def main():
#     print("this message is from the main function")


if __name__ == '__main__':
    # 第一步：获取信息
    train_data = extractTrainData(
        'dataset/demo_data/test7/trainData_part2.txt')
    test_data = extractTrainData(
        'dataset/demo_data/test6_testdata/testData.txt')
    # 第二步：调用逻辑回归 Logistic Function
    getBestId(train_data, test_data,
              'dataset/demo_data/nA1B_testData/2021-7-7-NA1B-ALL.txt')
    # 第三步：使用真实业务数据对模型进行测试
