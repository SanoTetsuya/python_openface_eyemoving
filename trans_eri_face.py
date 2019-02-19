import matplotlib.pyplot as plt
import numpy as np
import sys # モジュール属性 argv を取得するため
import csv
#Actroidで使えるようにデータのFPSを調整する。
result = []
ros_fps = 23
target_fps = 10 #10
#フレーム合わせ
count = int(ros_fps/target_fps)
#端数
number_small = (ros_fps/target_fps) - int(ros_fps/target_fps)

print(count)
f = open('./mouth_face_move_range.csv')
data = csv.reader(f)
frame = 0
for row in data:
    result.append(float(row[0]))
    frame += 1

total_mouth=0

outgaze = []
count_for = 0
plas_num = 0
for num in range(int((frame)/(count+number_small))):
    total_mouth=0
    count_for += number_small
    if count_for < 1:
        for math in range(count):
            total_mouth+=result[num*count+math+plas_num]/count
    else:
        for math in range(count+1):
            total_mouth+=result[num*count+math]/(count+1)
        count_for = 0
        plas_num += 1
    outgaze.append(total_mouth)


out = open('eri_mouth_face.csv', 'w')

for num in range(len(outgaze)):
    listData = []
    writer = csv.writer(out, lineterminator='\n')
    listData.append(float(outgaze[num]))
    writer.writerow(listData)

out.close()


plt.plot(outgaze, '.', markersize=1)
plt.xlabel("time [s]")
plt.ylabel("gaze")
title_int = int(len(outgaze)/target_fps)
#plt.title("total time:{:}[s] gaze time {:.3}[s]".format(title_int,gazetime))

plt.xticks([0,len(outgaze)/2,len(outgaze)],[0,title_int/2,title_int])  #時間表示させる。これで60[s]
#plt.yticks([0,0.2,0.8,1],[str("not face"),str("not blink"),str("blink"),str("face")])
plt.savefig("result_eri_face.png")
plt.show()
