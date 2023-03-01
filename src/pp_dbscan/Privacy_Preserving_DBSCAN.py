import torch
import crypten
import crypten.communicator as comm
import crypten.mpc as mpc
from torch import tensor
import queue
import matplotlib.pyplot as plt

crypten.init()


@mpc.run_multiprocess(world_size=1)
def examine_arithmetic_shares(minpts, e):
    class Share_object:

        def __init__(self, rank, point):
            self.rank = rank
            self.share = crypten.cryptensor(point, ptype=crypten.mpc.arithmetic)
            self.is_clustered= False
            self.cluster = -1
            self.direct_reach=set()
    x_enc = crypten.cryptensor([1, 2, 3], ptype=crypten.mpc.arithmetic)

    min_distance = crypten.cryptensor([e], ptype=crypten.mpc.arithmetic)
    print(min_distance)

    cluster_group = []
    cluster_count = 0

    data = []
    file = open("test0.txt")
    while True:
        line = file.readline()
        if not line:
            break
        str = line.split(';')
        temp_share = Share_object(rank=0, point=[float(str[0])/1000, float(str[1])/1000])

        data.append(temp_share)
    file.close()
    data_count = 0
    test_count=0
    for i in range(len(data)):
        for j  in range(i+1,len(data)):
            if (Euclidean_Distance(data[i].share,data[j].share)<=min_distance).get_plain_text()==tensor([1]):
                data[i].direct_reach.add(j)
                data[j].direct_reach.add(i)
                print(test_count)
                test_count+=1
                continue
            else:
                print(test_count)
                test_count+=1
    cluster_count = 0
    cluster_group = {}
    cluster_center = set()
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
    data_x = []
    data_y = []
    file = open("test0.txt")
    while True:
        line = file.readline()
        if not line:
            break
        str = line.split(';')
        data_x.append(float(str[0]) / 1000)
        data_y.append(float(str[1]) / 1000)

    file.close()
    cluster_x = []
    cluster_y = []
    cluster_count = 0
    for i in cluster_group:
        cluster_count += 1
        temp_x = []
        temp_y = []
        print(i)
        for p in cluster_group[i]:
            temp_x.append(data_x[p])
            temp_y.append(data_y[p])
        cluster_x.append(temp_x)
        cluster_y.append(temp_y)

    for i in range(cluster_count):
        plt.scatter(cluster_x[i], cluster_y[i])
    plt.legend(['grouup_1', 'group_2', 'group_3'])
    plt.show()

    return cluster_group

    # compute all distance?


def Euclidean_Distance(a_tensor_1, a_tensor_2):
    a_tensor_temp = a_tensor_2 - a_tensor_1
    x_tensor = a_tensor_temp[0]

    y_tensor = a_tensor_temp[1]
    #print((x_tensor.pos_pow(2)+y_tensor.pos_pow(2)).get_plain_text())


    return x_tensor.pos_pow(2) + y_tensor.pos_pow(2)


class Point_Object:

    def __init__(self, a_share):
        self.a_share = a_share
        self.density_reach_group = []
        self.is_processed = False

def draw_table():
    data_x = []
    data_y = []
    file = open("test0.txt")
    while True:
        line = file.readline()
        if not line:
            break
        str = line.split(';')
        data_x.append(float(str[0])/1000)
        data_y.append(float(str[1])/1000)

    file.close()
    cluster_group=examine_arithmetic_shares(10,50000)
    cluster_x=[]
    cluster_y=[]
    cluster_count=0
    for i in cluster_group:
        cluster_count+=1
        temp_x=[]
        temp_y=[]
        print(i)
        for p in cluster_group[i]:
            temp_x.append(data_x[p])
            temp_y.append(data_y[p])
        cluster_x.append(temp_x)
        cluster_y.append(temp_y)

    for i in range(cluster_count):
        plt.scatter(cluster_x[i],cluster_y[i])
    plt.legend(['grouup_1','group_2','group_3'])
    plt.show()

def read_data():
    return

def test():
    p1=crypten.cryptensor([1],ptype=crypten.mpc.arithmetic)
    p2=crypten.cryptensor([4],ptype=crypten.mpc.arithmetic)
    if ((p1 > p2).get_plain_text()==tensor([0])):
        print('ssd')

    print((p1 > p2)._tensor.get_plain_text()==tensor([0]))

print(examine_arithmetic_shares(10,50000))



