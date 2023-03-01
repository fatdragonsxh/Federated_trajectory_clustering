import torch
import crypten
import crypten.communicator as comm
import crypten.mpc as mpc
from torch import tensor
import queue
import matplotlib.pyplot as plt
import TRACLUS

crypten.init()

class Line_Arithmetic_Share:
    def __init__(self,start_share:crypten.cryptensor,end_share:crypten.cryptensor):
        self.start_share=start_share
        self.end_share=end_share
        self.is_clustered = False
        self.cluster = -1
        self.direct_reach = set()

def Trajectory_Distance_1(t1:Line_Arithmetic_Share,t2:Line_Arithmetic_Share):
    temp1=t1.start_share-t2.start_share
    temp2=t1.start_share-t2.end_share
    temp3=t1.end_share-t2.start_share
    temp4=t1.end_share-t2.end_share
    return temp1*temp1+temp2*temp2+temp3*temp3+temp4*temp4

def Privacy_Preserving_TRACLUS(minpts,eps):
    density=crypten.cryptensor([eps],ptype=crypten.mpc.arithmetic)
    filename = 'hurricane.tra'
    f = open(filename)

    trajectory_queue=queue.Queue()
    while True:
        pointlist = []
        line = f.readline()
        if not line:
            break
        str = line.split(' ')
        for i in range(0, len(str), 2):
            pointlist.append([float(str[i]), float(str[i + 1])])
        TR = TRACLUS.TRAJECTORY(pointlist)
        trajectory_queue.put(TR)

    Line_share_list=[]

    # TRAJECTORY PARTITION TO LINE SEGMENT

    while not trajectory_queue.empty():
        temp_trajectory=trajectory_queue.get()
        line_seg_set=list(TRACLUS.partition(temp_trajectory))
        for i in range(len(line_seg_set)-1):
            temp_start=line_seg_set[i]
            temp_end=line_seg_set[i+1]
            temp_start_share=crypten.cryptensor(temp_start,ptype=crypten.mpc.arithmetic)
            temp_end_share = crypten.cryptensor(temp_start, ptype=crypten.mpc.arithmetic)
            temp_trajectory_share=Line_Arithmetic_Share(temp_start_share,temp_end_share)
            Line_share_list.append(temp_trajectory_share)
    test_count = 0
    for i in range(len(Line_share_list)):
        for j in range(i + 1, len(Line_share_list)):
            if (Trajectory_Distance_1(Line_share_list[i], Line_share_list[j]) <= density).get_plain_text() == tensor([1]):
                Line_share_list[i].direct_reach.add(j)
                Line_share_list[j].direct_reach.add(i)
                print(test_count)
                test_count += 1
                continue
            else:
                print(test_count)
                test_count += 1
    cluster_count = 0
    cluster_group = {}
    cluster_center = set()
    for i in range(len(Line_share_list)):
        if len(Line_share_list[i].direct_reach) >= minpts:
            cluster_center.add(i)
    while len(cluster_center) != 0:
        rand_core = cluster_center.pop()
        temp_queue = queue.Queue()
        temp_queue.put(rand_core)
        Line_share_list[rand_core].is_clustered = True
        temp_cluster_group = set()
        while not temp_queue.empty():
            p = temp_queue.get()
            Line_share_list[p].is_clustered = True
            temp_cluster_group.add(p)
            if len(Line_share_list[p].direct_reach) >= minpts:
                for direct_index in Line_share_list[p].direct_reach:
                    if not Line_share_list[direct_index].is_clustered:
                        temp_queue.put(direct_index)
                        Line_share_list[direct_index].is_clustered = True
                        temp_cluster_group.add(direct_index)
        cluster_group[cluster_count] = temp_cluster_group
        cluster_count += 1
        cluster_center = cluster_center - temp_cluster_group









