import torch
import crypten
import crypten.communicator as comm
import crypten.mpc as mpc
from torch import tensor
import queue
import matplotlib.pyplot as plt
import TRACLUS as tr_util

crypten.init()

#actually the same as ppDBSCAN_2.py
@mpc.run_multiprocess(world_size=2)
def Privacy_Preserving_TRACLUS_2(filename_1,filename_2,count_1,count_1_list,count_2,count_2_list,minpts, e):
    class Line_Arithmetic_Share:
        def __init__(self, start_share: crypten.cryptensor, end_share: crypten.cryptensor):
            self.start_share = start_share
            self.end_share = end_share
            self.is_clustered = False
            self.cluster = -1
            self.direct_reach = set()

    def Euclidean_Distance(a_tensor_1, a_tensor_2):

        a_tensor_temp = a_tensor_2 - a_tensor_1
        x_tensor = a_tensor_temp[0]

        y_tensor = a_tensor_temp[1]
        # print((x_tensor.pos_pow(2)+y_tensor.pos_pow(2)).get_plain_text())

        return x_tensor.pos_pow(2) + y_tensor.pos_pow(2)

    def Line_Distance_1(t1: Line_Arithmetic_Share, t2: Line_Arithmetic_Share):
        temp1 = Euclidean_Distance(t1.start_share , t2.start_share)
        temp2 = Euclidean_Distance(t1.start_share , t2.end_share)
        temp3 = Euclidean_Distance(t1.end_share , t2.start_share)
        temp4 = Euclidean_Distance(t1.end_share , t2.end_share)
        return temp1+temp2+temp3+temp4

    rank = comm.get().get_rank()
    data_alice = []
    data_bob = []
    data = []
    if rank == 0:

        f = open(filename_1)
        while True:
            line = f.readline()
            if not line:
                break
            temp_str = line.split(' ')[:-1]
            for j in range(0,len(temp_str),2):
                data_alice.append([float(temp_str[j]), float(temp_str[j+1])])

        share = crypten.cryptensor(data_alice, ptype=crypten.mpc.arithmetic, src=0)
        print(share.shape)
    else:
        dummy_data = [[0.0,0.0]]*count_1
        share = crypten.cryptensor(dummy_data, ptype=crypten.mpc.arithmetic, src=0)
    data.append(share)

    if rank == 1:


        f = open(filename_2)
        while True:
            line = f.readline()
            if not line:
                break
            temp_str = line.split(' ')[:-1]
            for j in range(0, len(temp_str),2):
                data_bob.append([float(temp_str[j]), float(temp_str[j + 1])])


        share = crypten.cryptensor(data_bob, ptype=crypten.mpc.arithmetic, src=1)
    else:
        dummy_data = [[0.0, 0.0]] * count_2
        share = crypten.cryptensor(dummy_data, ptype=crypten.mpc.arithmetic, src=1)
    data.append(share)

    p = crypten.cat(data, dim=0)
    # at this point,p is visible for two parties
    # and it's the same order of 2 files
    print(len(p))
    count_list_all=count_1_list+count_2_list
    count_k=0

    Line_Share_List = []
    print(p[0])
    for i in range(len(p)-1):
        if i+1==count_list_all[count_k]:
            count_k+=1
            continue
        Line_Share_List.append(Line_Arithmetic_Share(p[i],p[i+1]))
    # for temp_trajectory in p:
    #     # every temp_trajectory represents a trajectory
    #     for i in range(0,len(temp_trajectory)-1):
    #         if i+1==count_list_all[count_k]:
    #             count_k+=1
    #             continue
    #
    #         Line_Share_List.append(Line_Arithmetic_Share(temp_trajectory[i],temp_trajectory[i+1]))




    min_distance = crypten.cryptensor([e], ptype=crypten.mpc.arithmetic)

    data_count = 0
    test_count = 0
    for i in range(len(Line_Share_List)):
        for j in range(i + 1, len(Line_Share_List)):
            if (Line_Distance_1(Line_Share_List[i],
                                   Line_Share_List[j]) <= min_distance).get_plain_text() == tensor([1]):
                Line_Share_List[i].direct_reach.add(j)
                Line_Share_List[j].direct_reach.add(i)
                print(test_count)
                test_count += 1
                continue
            else:
                print(test_count)
                test_count += 1
    cluster_count = 0
    cluster_group = {}
    cluster_center = set()
    for i in range(len(Line_Share_List)):
        if len(Line_Share_List[i].direct_reach) >= minpts:
            cluster_center.add(i)
    while len(cluster_center) != 0:
        rand_core = cluster_center.pop()
        temp_queue = queue.Queue()
        temp_queue.put(rand_core)
        Line_Share_List[rand_core].is_clustered = True
        temp_cluster_group = set()
        while not temp_queue.empty():
            p = temp_queue.get()
            Line_Share_List[p].is_clustered = True
            temp_cluster_group.add(p)
            if len(Line_Share_List[p].direct_reach) >= minpts:
                for direct_index in Line_Share_List[p].direct_reach:
                    if not Line_Share_List[direct_index].is_clustered:
                        temp_queue.put(direct_index)
                        Line_Share_List[direct_index].is_clustered = True
                        temp_cluster_group.add(direct_index)
        cluster_group[cluster_count] = temp_cluster_group
        cluster_count += 1
        cluster_center = cluster_center - temp_cluster_group
    print(cluster_group)
    return cluster_group


def num_test():
    filename_1, count_1, count_1_list = tr_util.partition_to_file('hurricane.tra')
    filename_2, count_2, count_2_list = tr_util.partition_to_file('hurricane_1.tra')

    f = open(filename_1)
    data_alice = []
    while True:
        temp_segment = []
        line = f.readline()
        if not line:
            break
        temp_str = line.split(' ')[:-1]
        for j in range(0, len(temp_str), 2):
            data_alice.append([float(temp_str[j]), float(temp_str[j + 1])])

    f.close()
    f = open(filename_2)
    data_bob = []
    while True:
        temp_segment = []
        line = f.readline()
        if not line:
            break
        temp_str = line.split(' ')[:-1]
        for j in range(0, len(temp_str), 2):
            data_bob.append([float(temp_str[j]), float(temp_str[j + 1])])

    data_all = data_alice + data_bob
    count_all_list = count_1_list + count_2_list
    count_k = 0
    print(data_all)

    for i in range(len(data_all) - 1):
        if i + 1 == count_all_list[count_k]:
            count_k += 1
            print('\n')
            continue
        print('[%f,%f]' % (data_all[i][0], data_all[i][1]))
        print('[%f,%f]' % (data_all[i + 1][0], data_all[i + 1][1]))

if __name__ == '__main__':
    filename_1,count_1,count_1_list=tr_util.partition_to_file('hurricane.tra')
    filename_2,count_2,count_2_list=tr_util.partition_to_file('hurricane_1.tra')


    c_group=Privacy_Preserving_TRACLUS_2(filename_1,filename_2,count_1,count_1_list,count_2,count_2_list,5,100)
    print(c_group)



