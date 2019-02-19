from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import math
import sys # モジュール属性 argv を取得するため
import csv
#
argvs = sys.argv  # コマンドライン引数を格納したリストの取得

R_fps = 23  #ROSのFPSを入力する。
limit_sec = 60
#Pupil labsとOpenfaceRosの結果を読み込み一つのファイルを生成する
#両者FPSが合っていないので、FPSを合わせたデータを生成する。
#f = open('./pupillabs.csv')
f = open(sys.argv[1])
data = csv.reader(f)

#顔認識をした結果を読み込む
#f_ros = open('./openface.csv')
#コマンドラインで指定してあげてください。 
min_x = []     #X軸の最小値
max_x = []     #X軸の最大値
min_y = []     #y軸の最小値
max_y = []     #y軸の最大値
min_face_x = []     #顔のX軸の最小値
max_face_x = []     #顔のX軸の最大値
min_face_y = []     #顔のy軸の最小値
max_face_y = []     #顔のy軸の最大値

count = 0
max_area = 0
cal_area = 0
in_area =[]
in_face_area =[]
for row in data:
    min_x.append(float(row[1]))
    max_x.append(float(row[2]))
    min_face_x.append(float(row[3]))
    max_face_x.append(float(row[4]))
    #min_y.append(float(row[3]))
    #max_y.append(float(row[4]))
    min_y.append(float(row[5]))
    max_y.append(float(row[6]))
    min_face_y.append(float(row[7]))
    max_face_y.append(float(row[8]))
    #cal_area = (float(row[2])-float(row[1]))*(float(row[4])-float(row[3]))
    cal_area = (float(row[2])-float(row[1]))*(float(row[6])-float(row[5]))
    in_area.append(cal_area)
    if max_area < cal_area:
        max_area = cal_area
    cal_area = (float(row[4])-float(row[3]))*(float(row[8])-float(row[7]))
    in_face_area.append(cal_area)
    count += 1

print(max_area)
out = open('mouth_face_move_range.csv', 'w')
range_area = []
in_range = 0
limit = 0.2
plas = 0
for i in range(count):
    in_range = (in_area[i]/in_face_area[i]) * 100
    #in_range = in_area[i]/max_area
    #if in_range < 4:
    #    in_range = 4
    #else:
    #    while((in_range - (0.54 + plas)) > limit):
    #        plas += limit
    #    in_range = 0.5 + plas
    #    plas = 0

    range_area.append(in_range)

    listData = []
    writer = csv.writer(out, lineterminator='\n')
    listData.append(range_area[i])
    listData.append(in_area[i])
    listData.append(in_face_area[i])
    writer.writerow(listData)

out.close()

plt.figure(figsize=(12,4))
plt.subplot(1,2,1)
plt.plot(range_area, '.', markersize=0.4)
plt.xlabel("time [s]")
plt.ylabel("mouth [%]")
plt.xticks([0,count/2,count],[0,int(count/(2*R_fps)),int(count/R_fps)])  #時間表示させる。これで60[s]
#plt.title("total time:{:.4}[s] gaze time {:.3}[s]".format(total_time,gaze_time))
plt.title("Mouth movement")
plt.subplot(1,2,2)
plt.xlabel("Mouth size [%]")
plt.ylabel("Numbers")
plt.hist(range_area,bins=50,rwidth=0.8)
plt.title("Mouth movement histgram")
plt.savefig("result_face.png")
plt.show()
