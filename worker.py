import numpy as np
import session


def sigmoid(total_input):
    for i in range(len(total_input)):
        total_input[i] = 1 / (1 + np.exp(-total_input[i]))
    return total_input


def matmul(a, b):
    return np.matmul(a, b)


def plus(a, b):
    return a + b


def loss_function_der(output, goal):
    result = []
    for i in range(len(goal)):
        result.append(output[i]-goal[i])
    return result


def sigmoid_der(output):
    for i in range(len(output)):
        output[i] = output[i]*(1-output[i])
    return output


def calculate_out(node_list):
    dict = {"matmul": matmul, "plus": plus, "sigmoid": sigmoid}
    for node in node_list:
        node.calculate(dict[node.get_calculate_function()])
    return node_list[-1].get_value()


if __name__ == '__main__':
    # 连接master
    m_w_task, m_w_result = session.connect('127.0.0.1', 8002, b'master_worker')

    # 创建与parameter之间的连接
    w_p_task, w_p_result = session.register('127.0.0.1', 8004, b'worker_parameter')

    node_list = m_w_task.get(timeout=100)
    inputs = m_w_task.get(timeout=100)
    learning_rate = m_w_task.get(timeout=100)
    s = node_list[-1]
    node_dict = {}
    node_temp = s
    while not node_temp.get_is_leaf():
        node_dict[node_temp.get_name()] = node_temp
        if node_temp.get_right_child() is not None:
            node_dict[node_temp.get_right_child().get_name()] = node_temp.get_right_child()
        node_temp = node_temp.get_left_child()
    node_dict[node_temp.get_name()] = node_temp

    for i in range(100):
        print(i)
        for input_temp in inputs:

            x = node_dict["x"]
            w_p_task.put("get_parameters")
            w1_value = w_p_result.get(timeout=10)
            w2_value = w_p_result.get(timeout=10)
            b1_value = w_p_result.get(timeout=10)
            b2_value = w_p_result.get(timeout=10)
            w2 = node_dict["w2"]
            w1 = node_dict["w1"]
            b1 = node_dict["b1"]
            b2 = node_dict["b2"]
            w1.set_value(w1_value)
            w2.set_value(w2_value)
            b1.set_value(b1_value)
            b2.set_value(b2_value)
            h_out = node_dict["h_out"]
            x.set_value(np.mat(input_temp[0]))
            # print(x.get_value())
            # print(node_list[0].get_left_child().get_name())
            # print(node_list[0].get_left_child().get_value())
            calculate_out(node_list)
            res1 = np.array(loss_function_der(s.get_value().tolist()[0], input_temp[1])) * np.array(
                sigmoid_der(s.get_value().tolist()[0]))
            res2 = np.array(np.mat(res1).dot(
                np.transpose(w2.get_value())))[0] * np.array(sigmoid_der(h_out.get_value().tolist()[0]))
            delta_weight1 = -1 * learning_rate * np.transpose(np.mat(x.get_value())).dot(np.mat(res2))
            delta_bias1 = -1 * learning_rate * np.mat(res2)
            delta_weight2 = -1 * learning_rate * np.transpose(np.mat(h_out.get_value())).dot(np.mat(res1))
            delta_bias2 = -1 * learning_rate * np.mat(res1)
            w_p_task.put(delta_weight1)
            w_p_task.put(delta_weight2)
            w_p_task.put(delta_bias1)
            w_p_task.put(delta_bias2)

    w_p_task.put("get_parameters")
    w1_value = w_p_result.get(timeout=10)
    w2_value = w_p_result.get(timeout=10)
    b1_value = w_p_result.get(timeout=10)
    b2_value = w_p_result.get(timeout=10)
    w2 = node_dict["w2"]
    w1 = node_dict["w1"]
    b1 = node_dict["b1"]
    b2 = node_dict["b2"]
    w1.set_value(w1_value)
    w2.set_value(w2_value)
    b1.set_value(b1_value)
    b2.set_value(b2_value)

    count = 0
    correct = 0
    for input_temp in inputs:
        x = node_dict["x"]
        x.set_value(np.mat(input_temp[0]))
        output = calculate_out(node_list).tolist()[0]
        result = 0
        if output[0] > 0.5:
            result = 1
        if result == input_temp[1][0]:
            correct = correct + 1
        count = count + 1
    accuracy = float(correct)/count
    print("accuracy: ", accuracy)
    m_w_result.put(accuracy)

    w_p_result.get(timeout=100)