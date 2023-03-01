
import math
import matplotlib.pyplot as plt

class TRAJECTORY:
    def __init__(self,pointlist:[]):
        self.pointlist=pointlist
        self.is_clustered=False
        self.cluster_id=-1
        self.direct_reach=set()

def vertical_distance(s1,e1,s2,e2):
    #2 dao 1
    if math.fabs(e1[0]-s1[0])<1e-8:
        l1=math.fabs(s2[0]-s1[0])
        l2=math.fabs(e2[0]-s1[0])
        if (l1 + l2) == 0:
            return 0
        return (l1**2+l2**2)/(l1+l2)
    k=(e1[1]-s1[1])/(e1[0]-s1[0])
    b=e1[1]-k*e1[0]
    l1=math.fabs(k*s2[0]-s2[1]+b)/math.sqrt(1+k**2)
    l2=math.fabs(k*e2[0]-e2[1]+b)/math.sqrt(1+k**2)
    if (l1+l2)==0:
        return 0
    return (l1**2+l2**2)/(l1+l2)

def angle_distance(s1,e1,s2,e2):
    vector_1=[e1[0]-s1[0],e1[1]-s1[1]]
    vector_2 = [e2[0] - s2[0], e2[1] - s2[1]]
    vector_mix=vector_1[0]*vector_2[0]+vector_1[1]*vector_2[1]
    if math.fabs(vector_1[0]**2+vector_1[1]**2)<1e-8:
        return 0
    temp_1=vector_mix/math.sqrt(vector_1[0]**2+vector_1[1]**2)

    return math.sqrt(math.fabs((vector_2[0]**2+vector_2[1]**2)-(temp_1**2)))

def parallel_distance(s1,e1,s2,e2):
    pass


def MDL_par(TR:TRAJECTORY,i,j):
    direct_distance=math.sqrt((TR.pointlist[j][0]-TR.pointlist[i][0])**2+(TR.pointlist[j][1]-TR.pointlist[i][1])**2)
    if math.fabs(direct_distance)<1e-8:
        return float('-inf')
    LH=math.log2(direct_distance)
    LDH=0
    angle_all=0
    distance_all=0
    for i in range(i,j):
        angle_all+=angle_distance(TR.pointlist[i],TR.pointlist[j],TR.pointlist[i],TR.pointlist[i+1])
        distance_all += vertical_distance(TR.pointlist[i], TR.pointlist[j], TR.pointlist[i], TR.pointlist[i + 1])
    if angle_all==0 or distance_all==0:
        return float('-inf')

    LDH+=math.log2(angle_all)
    LDH+=math.log2(distance_all)
    return LH+LDH

def MDL_nopar(TR:TRAJECTORY,i,j):
    direct_distance = math.sqrt(
        (TR.pointlist[j][0] - TR.pointlist[i][0]) ** 2 + (TR.pointlist[j][1] - TR.pointlist[i][1]) ** 2)
    if math.fabs(direct_distance)<1e-8:
        return float('-inf')
    LH = math.log2(direct_distance)
    LDH = 0
    return LH+LDH


def partition(TR:TRAJECTORY):
    cp=set()
    cp.add(0)
    startIndex=0
    length=1
    TR_len=len(TR.pointlist)-1
    while startIndex+length<=TR_len:
        currIndex=startIndex+length
        cost_par=MDL_par(TR,startIndex,currIndex)
        cost_nopar=MDL_nopar(TR,startIndex,currIndex)
        if cost_par>cost_nopar:
            cp.add(currIndex)
            startIndex=currIndex-1
            length=1
        else:
            length+=1

    cp.add(TR_len)
    return cp

def partition_to_file(origin_file_name):
    origin_file=open(origin_file_name)
    trajectory_list=[]

    while True:
        point_list = []
        line = origin_file.readline()
        if not line:
            break

        temp_str = line.split(' ')
        for i in range(2,len(temp_str),2):
            point_list.append([float(temp_str[i]),float(temp_str[i+1])])
        temp_tr=TRAJECTORY(point_list)
        trajectory_list.append(temp_tr)
    partition_file_name = origin_file_name + '.par'
    partition_file = open(partition_file_name, 'w')
    segment_count=0
    every_line_count=[]
    for temp_trajectory in trajectory_list:
        segment_index = partition(temp_trajectory)
        temp_every_line_count=0

        for temp_index in segment_index:
            partition_file.write(str(temp_trajectory.pointlist[temp_index][0]))
            partition_file.write(' ')
            partition_file.write(str(temp_trajectory.pointlist[temp_index][1]))
            partition_file.write(' ')
            segment_count+=1
            temp_every_line_count+=1
        every_line_count.append(temp_every_line_count)
        partition_file.write('\r\n')



    return partition_file_name,segment_count,every_line_count

def argument_test():
    class Line:
        def __init__(self,start,end):
            self.start=start
            self.end=end
    def Line_Distance(line_1,line_2):
        temp1=(line_2.start[0]-line_1.start[0])**2+(line_2.start[1]-line_1.start[1])**2
        temp2 = (line_2.start[0] - line_1.end[0]) ** 2 + (line_2.start[1] - line_1.end[1]) ** 2
        temp3 = (line_2.end[0] - line_1.start[0]) ** 2 + (line_2.end[1] - line_1.start[1]) ** 2
        temp4 = (line_2.end[0] - line_1.end[0]) ** 2 + (line_2.end[1] - line_1.end[1]) ** 2


def test():
    filename='hurricane.tra'
    f=open(filename)
    pointlist=[]
    point_list_all=[]

    while True:
        line = f.readline()
        if not line:
            break
        str = line.split(' ')
        for i in range(0,len(str),2):
            pointlist.append([float(str[i]),float(str[i+1])])
        point_list_all.append(pointlist)
    f.close()
    p_filename="hurricane1950_2006.tra.par"
    pointlist_p=[]
    f = open(p_filename)
    pointlist = []

    while True:
        line = f.readline()
        if not line:
            break
        str = line.split(' ')
        for i in range(0, len(str), 2):
            pointlist.append([float(str[i]), float(str[i + 1])])



    ax1=plt.subplot(1,2,1)
    x1=[]
    y1=[]
    for t in pointlist:
        x1.append(t[0])
        y1.append(t[1])
    ax1.plot(x1,y1)
    ax2 = plt.subplot(1, 2, 2)
    x1=[]
    y1=[]
    for t in pointlist_1:
        x1.append(t[0])
        y1.append(t[1])
    ax2.plot(x1,y1)


    plt.show()



partition_to_file('hurricane1950_2006.tra')

