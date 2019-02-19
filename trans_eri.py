import matplotlib.pyplot as plt
import numpy as np
import sys # モジュール属性 argv を取得するため
import csv

result = []
pupilframe = 30
ros_fps = 10 #10
#フレーム合わせ
if ((pupilframe/ros_fps)-int(pupilframe/ros_fps)) > 0.5:
    count = int(pupilframe/ros_fps) + 1
else:
    count = int(pupilframe/ros_fps)

print(count)
f = open('./mouth_move_range.csv')
data = csv.reader(f)
frame = 0
for row in data:
    result.append(float(row[0]))
    frame += 1

total_mouth=0

outgaze = []

for num in range(int((frame)/count)):
    total_mouth=0
    for math in range(count):
        total_mouth+=result[num*count+math]/count
    outgaze.append(total_mouth)


out = open('eri_mouth.csv', 'w')

for num in range(len(outgaze)):
    listData = []
    writer = csv.writer(out, lineterminator='\n')
    listData.append(float(outgaze[num]))
    writer.writerow(listData)

out.close()


plt.plot(outgaze, '.', markersize=1)
plt.xlabel("time [s]")
plt.ylabel("gaze")
title_int = int(len(outgaze)/ros_fps)
#plt.title("total time:{:}[s] gaze time {:.3}[s]".format(title_int,gazetime))

plt.xticks([0,len(outgaze)/2,len(outgaze)],[0,title_int/2,title_int])  #時間表示させる。これで60[s]
#plt.yticks([0,0.2,0.8,1],[str("not face"),str("not blink"),str("blink"),str("face")])
plt.savefig("result_eri.png")
plt.show()
