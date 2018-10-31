import session


if __name__ == '__main__':
    # 连接master
    m_p_task, m_p_result = session.connect('127.0.0.1', 8003, b'master_parameter')

    # 创建与parameter之间的连接
    w_p_task, w_p_result = session.connect('127.0.0.1', 8004, b'worker_parameter')

    graph = m_p_task.get(timeout=100)
    s = graph
    node_dict = {}
    node_temp = s
    while not node_temp.get_is_leaf():
        node_dict[node_temp.get_name()] = node_temp
        if node_temp.get_right_child() is not None:
            node_dict[node_temp.get_right_child().get_name()] = node_temp.get_right_child()
        node_temp = node_temp.get_left_child()
    node_dict[node_temp.get_name()] = node_temp
    w1 = node_dict["w1"]
    b1 = node_dict["b1"]
    w2 = node_dict["w2"]
    b2 = node_dict["b2"]
    w1_value = w1.get_value()
    w2_value = w2.get_value()
    b1_value = b1.get_value()
    b2_value = b2.get_value()

    while w_p_task.get(timeout=1000) == "get_parameters":
        w_p_result.put(w1_value)
        w_p_result.put(w2_value)
        w_p_result.put(b1_value)
        w_p_result.put(b2_value)
        delta_w1 = w_p_task.get(timeout=100)
        delta_w2 = w_p_task.get(timeout=100)
        delta_b1 = w_p_task.get(timeout=100)
        delta_b2 = w_p_task.get(timeout=100)
        w1_value = w1_value + delta_w1
        w2_value = w2_value + delta_w2
        b1_value = b1_value + delta_b1
        b2_value = b2_value + delta_b2
