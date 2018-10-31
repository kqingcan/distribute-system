import session


if __name__ == '__main__':
    # 连接client
    c_m_task, c_m_result = session.connect('127.0.0.1', 8001, b'client_master')

    # 创建与worker之间的连接
    m_w_task, m_w_result = session.register('127.0.0.1', 8002, b'master_worker')

    # 创建与parameter之间的连接
    m_p_task, m_p_result = session.register('127.0.0.1', 8003, b'master_parameter')

    graph = c_m_task.get(timeout=100)
    inputs = c_m_task.get(timeout=100)
    learning_rate = c_m_task.get(timeout=100)
    node_list1 = []
    node = graph
    while not node.get_is_leaf():
        node_list1.append(node)
        node = node.get_left_child()
    node_list = list(reversed(node_list1))
    m_w_task.put(node_list)
    m_w_task.put(inputs)
    m_w_task.put(learning_rate)
    m_p_task.put(graph)
    accuracy = m_w_result.get(timeout=1000)
    c_m_result.put(accuracy)