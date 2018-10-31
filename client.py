import csv
import session
import Node
import numpy as np


def read_file(file_name):
    csv_file = csv.reader(open(file_name, 'r'))

    file_inputs_temp = []
    for data in csv_file:
        file_inputs_temp.append(data)
    return file_inputs_temp


def deal_inputs(file_inputs):
    inputs_temp = []
    for i in range(len(file_inputs)-1):
        file_input_temp = file_inputs[i+1]
        one_input = [float(file_input_temp[1])/800, float(file_input_temp[2])/4, float(file_input_temp[3])/4]
        one_goal = int(file_input_temp[0])
        inputs_temp.append([one_input, [one_goal]])
    return inputs_temp


class Client:

    def __init__(self, input_nums, hidden_nums, output_nums):
        self.input_nums = input_nums
        self.hidden_nums = hidden_nums
        self.output_nums = output_nums
        self.x = Node.Node(False, None, "x", True)
        self.w1 = Node.Node(False, None, "w1", True)
        self.b1 = Node.Node(False, None, "b1", True)
        self.mul1 = Node.Node(False, None, "mul1", False, self.x, self.w1)
        self.plus1 = Node.Node(False, None, "plus1", False, self.mul1, self.b1)
        self.h_out = Node.Node(False, None, "h_out", False, self.plus1)
        self.w2 = Node.Node(False, None, "w2", True)
        self.b2 = Node.Node(False, None, "b2", True)
        self.mul2 = Node.Node(False, None, "mul2", False, self.h_out, self.w2)
        self.plus2 = Node.Node(False, None, "plus2", False, self.mul2, self.b2)
        self.s = Node.Node(True, None, "s", False, self.plus2)
        self.mul1.set_calculate_function("matmul")
        self.plus1.set_calculate_function("plus")
        self.h_out.set_calculate_function("sigmoid")
        self.mul2.set_calculate_function("matmul")
        self.plus2.set_calculate_function("plus")
        self.s.set_calculate_function("sigmoid")
        self.init_variables()

    def init_variables(self):
        w1_value = 1*np.random.random((self.input_nums, self.hidden_nums))
        w2_value = 1*np.random.random((self.hidden_nums, self.output_nums))
        b1_value = 1*np.random.random(self.hidden_nums)
        b2_value = 1* np.random.random(self.output_nums)
        self.w1.set_value(w1_value)
        self.w2.set_value(w2_value)
        self.b1.set_value(b1_value)
        self.b2.set_value(b2_value)

    def generate_graph(self):
        return self.s


if __name__ == '__main__':
    file_inputs = read_file("student_data.csv")
    inputs = deal_inputs(file_inputs)
    client = Client(3, 15, 1)
    # client.train(inputs)
    # client.test(inputs)
    # 创建与master之间的连接
    learning_rate = 0.05
    c_m_task, c_m_result = session.register('127.0.0.1', 8001, b'client_master')
    c_m_task.put(client.generate_graph())
    c_m_task.put(inputs)
    c_m_task.put(learning_rate)
    print("accuracy:  ", c_m_result.get(timeout=1000))