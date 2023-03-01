import TRACLUS as tr_util
import queue
import matplotlib.pyplot as plt



def PLain_Text_TRACLUS(filename_1,filename_2,count_list_1,count_list_2,minpts,e):

    class Line_Segment:
        def __init__(self,start,end):
            self. start=start
            self.end=end
            self.cluster_id=-1
            self.is_clustered=False
            self.direct_reach=set()

        def __str__(self):
            return 'start:[%1f,%1f];end:[%1f,%1f]'%(self.start[0],self.start[1],self.end[0],self.end[1])
    def Euclidean_Distance(point_1,point_2):
        return (point_2[0]-point_1[0])**2+(point_2[1]-point_1[1])**2

    def Line_Distance_1(line_1:Line_Segment,line_2:Line_Segment):
        temp1=Euclidean_Distance(line_1.start,line_2.start)
        temp2=Euclidean_Distance(line_1.start,line_2.end)
        temp3=Euclidean_Distance(line_1.end,line_2.start)
        temp4=Euclidean_Distance(line_1.end,line_2.end)
        return temp1+temp2+temp3+temp4

    f = open(filename_1)
    data_alice = []
    while True:
        temp_segment = []
        line = f.readline()
        if not line:
            break
        temp_str = line.split(' ')[:-1]
        for j in range(0, len(temp_str),2):
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
        for j in range(0, len(temp_str),2):
            data_bob.append([float(temp_str[j]), float(temp_str[j + 1])])

    data_all = data_alice + data_bob
    count_all_list = count_list_1 + count_list_2
    count_k = 0
    print(data_all)
    line_list=[]

    for i in range(len(data_all) - 1):
        if i + 1 == count_all_list[count_k]:
            count_k += 1

            continue
        line_list.append(Line_Segment([data_all[i][0], data_all[i][1]],[data_all[i + 1][0], data_all[i + 1][1]]))
    # for q in line_list:
    #     print(q)
    for i in range(len(line_list)):
        for j in range(i + 1, len(line_list)):
            # print(Line_Distance_1(line_list[i],
            #                        line_list[j]))
            if (Line_Distance_1(line_list[i],
                                   line_list[j]) <= e):
                line_list[i].direct_reach.add(j)
                line_list[j].direct_reach.add(i)

                continue

    cluster_count = 0
    cluster_group = {}
    cluster_center = set()
    for i in range(len(line_list)):
        if len(line_list[i].direct_reach) >= minpts:
            cluster_center.add(i)
    while len(cluster_center) != 0:
        rand_core = cluster_center.pop()
        temp_queue = queue.Queue()
        temp_queue.put(rand_core)
        line_list[rand_core].is_clustered = True
        temp_cluster_group = set()
        while not temp_queue.empty():
            p = temp_queue.get()
            line_list[p].is_clustered = True
            temp_cluster_group.add(p)
            if len(line_list[p].direct_reach) >= minpts:
                for direct_index in line_list[p].direct_reach:
                    if not line_list[direct_index].is_clustered:
                        temp_queue.put(direct_index)
                        line_list[direct_index].is_clustered = True
                        temp_cluster_group.add(direct_index)
        cluster_group[cluster_count] = temp_cluster_group
        cluster_count += 1
        cluster_center = cluster_center - temp_cluster_group
    print(len(cluster_group))
    print(cluster_group[1])
    return cluster_group

def Plain_Text_Traclus_Based_Trajectory(filename_1,filename_2,minpts,e):


    def Euclidean_Distance(point_1,point_2):
        return (point_2[0]-point_1[0])**2+(point_2[1]-point_1[1])**2

    def tr_distance(tr1:tr_util.TRAJECTORY,tr2:tr_util.TRAJECTORY):

        temp=0
        for i in range(len(tr1.pointlist)-1):
            for j in range(len(tr2.pointlist)-1):
                temp1=Euclidean_Distance(tr1.pointlist[i],tr2.pointlist[j])
                temp2=Euclidean_Distance(tr1.pointlist[i],tr2.pointlist[j+1])
                temp3=Euclidean_Distance(tr1.pointlist[i+1],tr2.pointlist[j])
                temp4=Euclidean_Distance(tr1.pointlist[i+1],tr2.pointlist[j+1])
                temp+=temp1+temp2+temp3+temp4

        return temp/(len(tr1.pointlist)+len(tr2.pointlist))




    f = open(filename_1)
    data_alice = []
    while True:
        temp_segment = []
        point_list=[]
        line = f.readline()
        if not line:
            break
        temp_str = line.split(' ')[:-1]
        for j in range(0, len(temp_str), 2):
            point_list.append([float(temp_str[j]), float(temp_str[j + 1])])
        tr=tr_util.TRAJECTORY(point_list)
        data_alice.append(tr)

    f.close()
    f = open(filename_2)
    data_bob = []
    while True:
        temp_segment = []
        point_list=[]
        line = f.readline()
        if not line:
            break
        temp_str = line.split(' ')[:-1]
        for j in range(0, len(temp_str), 2):
            point_list.append([float(temp_str[j]), float(temp_str[j + 1])])
        tr=tr_util.TRAJECTORY(point_list)
        data_bob.append(tr)
    data=data_alice+data_bob
    print(data)
    for i in range(len(data)):
        for j in range(i+1,len(data)):
            if tr_distance(data[i],data[j])<e:

                data[i].direct_reach.add(j)
                data[j].direct_reach.add(i)
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


    return cluster_group





def EDR_Plain_Text_Traclus(filename,e,minpts,theta):
    def Euclidean_Distance(point_1,point_2):
        return (point_2[0]-point_1[0])**2+(point_2[1]-point_1[1])**2


    def EDR(tr1:tr_util.TRAJECTORY,tr2:tr_util.TRAJECTORY,count_1,count_2):
        #create subcost matrix first
        tr1_length=len(tr1.pointlist)
        tr2_length=len(tr2.pointlist)
        subcost=[]
        for j in range(tr2_length+1):
            subcost.append([0]*(tr1_length+1))

        for i in range(1,tr1_length+1):
            subcost[0][i]=1
        for i in range(1,tr2_length+1):
            subcost[i][0]=1
        print(subcost)
        for i in range(1,tr1_length+1):
            for j in range(1,tr2_length+1):
                if Euclidean_Distance(tr1.pointlist[i-1],tr2.pointlist[j-1])>theta:

                    subcost[j][i]=1

        print(subcost)

        dp=[[0]*(tr1_length+1)]*(tr2_length+1)
        for i in range(tr1_length+1):
            dp[0][i]=i
        for i in range(tr2_length+1):
            dp[i][0]=i
        for i in range(1,tr2_length+1):
            for j in range(1,tr1_length+1):
                dp[i][j]=min(dp[i-1][j-1]+subcost[i][j],dp[i][j-1]+1,dp[i-1][j]+1)

        return dp[tr2_length][tr1_length]


    origin_file = open(filename)
    trajectory_list = []

    while True:
        point_list = []
        line = origin_file.readline()
        if not line:
            break

        temp_str = line.split(' ')[:-1]
        for i in range(0, len(temp_str), 2):
            point_list.append([float(temp_str[i]), float(temp_str[i + 1])])

        temp_tr = tr_util.TRAJECTORY(point_list)
        trajectory_list.append(temp_tr)
    print('fj')
    #so now we get trajectory list
    cluster_count = 0
    cluster_group = {}
    cluster_center = set()
    test_count = 0
    for i in range(len(trajectory_list)):
        for j in range(i + 1, len(trajectory_list)):
            temp=EDR(trajectory_list[i],trajectory_list[j],0,0)
            print(temp)

            if temp < e:
                trajectory_list[i].direct_reach.add(j)
                trajectory_list[j].direct_reach.add(i)
    for i in range(len(trajectory_list)):
        if len(trajectory_list[i].direct_reach) >= minpts:
            cluster_center.add(i)
    while len(cluster_center)!=0:
        rand_core=cluster_center.pop()
        temp_queue=queue.Queue()
        temp_queue.put(rand_core)
        trajectory_list[rand_core].is_clustered=True
        temp_cluster_group=set()
        while not temp_queue.empty():
            p=temp_queue.get()
            trajectory_list[p].is_clustered=True
            temp_cluster_group.add(p)
            if len(trajectory_list[p].direct_reach)>=minpts:
                for direct_index in trajectory_list[p].direct_reach:
                    if not trajectory_list[direct_index].is_clustered:
                        temp_queue.put(direct_index)
                        trajectory_list[direct_index].is_clustered=True
                        temp_cluster_group.add(direct_index)
        cluster_group[cluster_count]=temp_cluster_group
        cluster_count+=1
        cluster_center=cluster_center-temp_cluster_group
    print(cluster_group)


    return cluster_group

def draw_trajectory(filename_1,filename_2,count_1_list,count_2_list,cluster_group):
    class Line_Segment:
        def __init__(self, start, end):
            self.start = start
            self.end = end
            self.cluster_id = -1
            self.is_clustered = False
            self.direct_reach = set()

        def __str__(self):
            return 'start:[%1f,%1f];end:[%1f,%1f]' % (self.start[0], self.start[1], self.end[0], self.end[1])

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

    line_list = []

    for i in range(len(data_all) - 1):
        if i + 1 == count_all_list[count_k]:
            count_k += 1

            continue
        line_list.append(Line_Segment([data_all[i][0], data_all[i][1]], [data_all[i + 1][0], data_all[i + 1][1]]))
    for t in cluster_group:
        start_x=[]
        start_y=[]
        end_x=[]
        end_y=[]

        for index in cluster_group[t]:

            start_x.append(line_list[index].start[0])
            start_y.append(line_list[index].start[1])
            end_x.append(line_list[index].end[0])
            end_y.append(line_list[index].end[1])

        plt.plot(start_x,start_y,label='group%d'%(t))
    plt.legend()


    plt.show()



if __name__ == '__main__':
    filename_1,count_1,count_1_list=tr_util.partition_to_file('hurricane.tra')
    filename_2,count_2,count_2_list=tr_util.partition_to_file('hurricane_1.tra')
    # c_group=PLain_Text_TRACLUS(filename_1,filename_2,count_1_list,count_2_list,2,10000)
    # draw_trajectory(filename_1,filename_2,count_1_list,count_2_list,c_group)
    # Plain_Text_Traclus_Based_Trajectory(filename_1,filename_2,2,300000)
    EDR_Plain_Text_Traclus('hurricane.tra.par',50,2,10000)
