import torch
import crypten
import crypten.communicator as comm
import crypten.mpc as mpc
from torch import tensor
import queue
import matplotlib.pyplot as plt

crypten.init()


@mpc.run_multiprocess(world_size=2)
def Privacy_Preserving_DBSCAN_2(filename_1,filename_2,count_1,count_2,minpts, e):
    class Share_object:

        def __init__(self, rank, share):
            self.rank = rank
            self.share = share
            self.is_clustered= False
            self.cluster = -1
            self.direct_reach=set()
    rank=comm.get().get_rank()
    data_alice=[]
    data_bob=[]
    data=[]
    if rank==0:
        f=open(filename_1)
        while True:
            line = f.readline()
            if not line:
                break
            str = line.split(',')
            data_alice.append([float(str[0]), float(str[1])])

        share=crypten.cryptensor(data_alice, ptype=crypten.mpc.arithmetic, src=0)
    else:
        data_alice.append([0,0])
        b=[[0, 0]]*count_1
        share=crypten.cryptensor(b, ptype=crypten.mpc.arithmetic, src=0)
    data.append(share)

    if rank==1:

        f = open(filename_2)
        while True:
            line = f.readline()
            if not line:
                break
            str = line.split(',')
            data_bob.append([float(str[0]), float(str[1])])

        share = crypten.cryptensor(data_bob, ptype=crypten.mpc.arithmetic, src=1)
    else:
        data_bob.append([0,0])
        b=[[0,0]]*count_2
        share = crypten.cryptensor(b, ptype=crypten.mpc.arithmetic, src=1)
    data.append(share)


    p=crypten.cat(data,dim=0)
    #at this point,p is visible for two parties
    #and it's the same order of 2 files
    print(len(p))
    data_point=[]
    for temp_share in p:
        data_point.append(Share_object(0,temp_share))
    #we do not contain 2 parties count
    #todo... 2 parties count, but not influence final result

    min_distance=crypten.cryptensor([e],ptype=crypten.mpc.arithmetic)

    data_count = 0
    test_count = 0
    for i in range(len(data_point)):
        for j in range(i + 1, len(data_point)):
            if (Euclidean_Distance(data_point[i].share, data_point[j].share) <= min_distance).get_plain_text() == tensor([1]):
                data_point[i].direct_reach.add(j)
                data_point[j].direct_reach.add(i)
                print(test_count)
                test_count += 1
                continue
            else:
                print(test_count)
                test_count += 1
    cluster_count = 0
    cluster_group = {}
    cluster_center = set()
    for i in range(len(data_point)):
        if len(data_point[i].direct_reach) >= minpts:
            cluster_center.add(i)
    while len(cluster_center) != 0:
        rand_core = cluster_center.pop()
        temp_queue = queue.Queue()
        temp_queue.put(rand_core)
        data_point[rand_core].is_clustered = True
        temp_cluster_group = set()
        while not temp_queue.empty():
            p = temp_queue.get()
            data_point[p].is_clustered = True
            temp_cluster_group.add(p)
            if len(data_point[p].direct_reach) >= minpts:
                for direct_index in data_point[p].direct_reach:
                    if not data_point[direct_index].is_clustered:
                        temp_queue.put(direct_index)
                        data_point[direct_index].is_clustered = True
                        temp_cluster_group.add(direct_index)
        cluster_group[cluster_count] = temp_cluster_group
        cluster_count += 1
        cluster_center = cluster_center - temp_cluster_group
    print(cluster_group)
    return cluster_group




def Euclidean_Distance(a_tensor_1, a_tensor_2):
    a_tensor_temp = a_tensor_2 - a_tensor_1
    x_tensor = a_tensor_temp[0]

    y_tensor = a_tensor_temp[1]
    #print((x_tensor.pos_pow(2)+y_tensor.pos_pow(2)).get_plain_text())


    return x_tensor.pos_pow(2) + y_tensor.pos_pow(2)


def draw_table_2(filename_1,filename_2,count_1,count_2):
    data_x = []
    data_y = []
    file = open(filename_1)
    while True:
        line = file.readline()
        if not line:
            break
        str = line.split(',')
        data_x.append(float(str[0]))
        data_y.append(float(str[1]))

    file.close()
    file=open(filename_2)
    while True:
        line=file.readline()
        if not line:
            break
        str = line.split(',')
        data_x.append(float(str[0]))
        data_y.append(float(str[1]))
    file.close()
    cluster_group=Privacy_Preserving_DBSCAN_2(filename_1,filename_2,count_1,count_2,minpts=5,e=2)[0]
    """
    cluster_group presents like : {1:[x,x],2:[x,x]},so we need to extract it like cluster_group[0]
    """
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

if __name__ == '__main__':
    draw_table_2('point_0','point_1',50,50)

