import queue

import torch
from torch import tensor
import matplotlib.pyplot as plt


def Plain_Text_DBSCAN(minpts, e):
    class point:

        def __init__(self, data):
            self.data = data
            self.is_clustered = False
            self.cluster = -1
            self.direct_reach=set()

    def Euclidean_Distance(point_1: point, point_2: point):
        temp_result = (point_2.data - point_1.data).pow(2)
        return temp_result[0] + temp_result[1]

    min_distance = tensor(e)
    data = []
    file = open("point_2")
    while True:
        line = file.readline()
        if not line:
            break
        str = line.split(',')
        temp_point = tensor([float(str[0]), float(str[1])])
        temp_data = point(temp_point)

        data.append(temp_data)
    file.close()

    cluster_count = 0
    cluster_group = {}
    cluster_center=set()
    test_count=0
    for i in range(len(data)):
        for j in range(i+1,len(data)):

            if Euclidean_Distance(data[i],data[j])<min_distance:

                data[i].direct_reach.add(j)
                data[j].direct_reach.add(i)
    for i in range(len(data)):
        if len(data[i].direct_reach)>=minpts:
            cluster_center.add(i)
    while len(cluster_center)!=0:
        rand_core=cluster_center.pop()
        temp_queue=queue.Queue()
        temp_queue.put(rand_core)
        data[rand_core].is_clustered=True
        temp_cluster_group=set()
        while not temp_queue.empty():
            p=temp_queue.get()
            data[p].is_clustered=True
            temp_cluster_group.add(p)
            if len(data[p].direct_reach)>=minpts:
                for direct_index in data[p].direct_reach:
                    if not data[direct_index].is_clustered:
                        temp_queue.put(direct_index)
                        data[direct_index].is_clustered=True
                        temp_cluster_group.add(direct_index)
        cluster_group[cluster_count]=temp_cluster_group
        cluster_count+=1
        cluster_center=cluster_center-temp_cluster_group
    print(cluster_group)


    return cluster_group


def draw_table():
    data_x = []
    data_y = []
    file = open("point_2")
    while True:
        line = file.readline()
        if not line:
            break
        str = line.split(',')
        data_x.append(float(str[0]))
        data_y.append(float(str[1]))

    file.close()
    cluster_group=Plain_Text_DBSCAN(2,5)
    cluster_x=[]
    cluster_y=[]
    cluster_count=0
    for i in cluster_group:
        cluster_count+=1
        temp_x=[]
        temp_y=[]
        for p in cluster_group[i]:
            temp_x.append(data_x[p])
            temp_y.append(data_y[p])
        cluster_x.append(temp_x)
        cluster_y.append(temp_y)

    for i in range(cluster_count):
        plt.scatter(cluster_x[i],cluster_y[i])
    plt.legend(['grouup_1','group_2','group_3'])
    plt.show()




def test():
    p1 = tensor([3277701, 814082])
    p2 = tensor([387577, 176780])
    t = (p2 - p1).pow(2)
    print(t[0] + t[1])
    t1 = tensor(1)
    t2 = tensor(2)
    print(t2 > t1)

#test()
draw_table()
