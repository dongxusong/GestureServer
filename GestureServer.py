# -*-coding:utf-8-*-
import random

from flask import Flask
from flask import request
import thread

from matplotlib import pyplot as plt
from matplotlib import animation
import numpy as np
import seaborn as sns


def Normalize(data):
    m = np.mean(data)
    mx = max(data)
    mn = min(data)
    return [(float(i) - m) / (mx - mn) for i in data]


app = Flask(__name__)


@app.route('/')
def test():
    return '服务器正常运行'


gesture_i = [0] * 2200
gesture_q = [0] * 2200
cur_data_count = 0


@app.route('/senddata_i', methods=['POST'])
def getdata_i():
    global gesture_i

    value_i = request.form['gesture']
    value_i = value_i.split(",")

    global cur_data_count
    temp_i = []

    for i in range(0, 110):
        temp_i.append(float(value_i[i]))

    temp_i = Normalize(temp_i)

    if cur_data_count == 20:
        for i in range(0, 110):  # 先这么写吧，优化的时候最好吧这两步放在一个for里面处理
            del gesture_i[0]
            gesture_i.append(float(temp_i[i]))
    else:
        cur_data_count = cur_data_count + 1
        for i in range(0, 110):
            gesture_i[cur_data_count * 110 + i] = float(temp_i[i])
    print(temp_i)
    return "ok"





@app.route('/senddata_q', methods=['POST'])
def getdata_q():
    global gesture_q

    value_i = request.form['gesture']
    value_i = value_i.split(",")

    global cur_data_count
    temp_i = []

    for i in range(0, 110):
        temp_i.append(float(value_i[i]))

    temp_i = Normalize(temp_i)

    if cur_data_count == 20:
        for i in range(0, 110):  # 先这么写吧，优化的时候最好吧这两步放在一个for里面处理
            del gesture_q[0]
            gesture_q.append(float(temp_i[i]))
    else:
        cur_data_count = cur_data_count + 1
        for i in range(0, 110):
            gesture_q[cur_data_count * 110 + i] = float(temp_i[i])
    print(temp_i)
    return "ok"


'''
x轴为时间，y轴为幅度值，范围为【-1,1】，要求入的数据为归一化之后的
每0.5s更新一次数据，每次更新数据增加（去掉）550个点
'''
#
# sns.set_style("whitegrid")
#
# # 创建画布，包含2个子图,分别是I和Q，后期可以再增加
fig = plt.figure(figsize=(15, 10))
ax1 = fig.add_subplot(2, 1, 1)
ax2 = fig.add_subplot(2, 1, 2)

# 先绘制初始图形，每个子图包含1个正弦波和三个点的散点图
x = np.arange(0, 2200, 1)  # x轴

ax1.set_ylim(-1, 1)
line1, = ax1.plot(x, gesture_i)

ax2.set_ylim(-1, 1)
line2, = ax2.plot(x, gesture_q)


def init():
    # 构造开始帧函数init
    # 改变y轴数据，x轴不需要改
    line1.set_ydata(gesture_i)
    line2.set_ydata(gesture_q)
    label = 'timestep {0}'.format(0)
    ax1.set_xlabel(label)
    return line1, line2, ax1  # 注意返回值，我们要更新的就是这些数据


def animate(i):
    global gesture_i
    global gesture_q
    # 接着，构造自定义动画函数animate，用来更新每一帧上各个x对应的y坐标值，参数表示第i帧
    # plt.cla() 这个函数很有用，先记着它
    line1.set_ydata(gesture_i)
    line2.set_ydata(gesture_q)
    label = 'timestep {0}'.format(i)
    ax1.set_xlabel(label)
    return line1, line2, ax1


# 接下来，我们调用FuncAnimation函数生成动画。参数说明：
# fig 进行动画绘制的figure
# func 自定义动画函数，即传入刚定义的函数animate
# frames 动画长度，一次循环包含的帧数
# init_func 自定义开始帧，即传入刚定义的函数init
# interval 更新频率，以ms计
# blit 选择更新所有点，还是仅更新产生变化的点。应选择True，但mac用户请选择False，否则无法显示动画


def draw_view():
    ani = animation.FuncAnimation(fig=fig,
                                  func=animate,
                                  frames=100,
                                  init_func=init,
                                  interval=100,
                                  blit=False)
    plt.show()


def run_server():
    app.run(host='0.0.0.0')


if __name__ == '__main__':
    thread.start_new_thread(run_server, ())
    draw_view()
