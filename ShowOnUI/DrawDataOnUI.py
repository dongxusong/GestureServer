# -*-coding:utf-8-*-
from matplotlib import pyplot as plt
from matplotlib import animation
import numpy as np
import seaborn as sns


'''
需求：
x轴为时间，y轴为幅度值，范围为【-1,1】，要求入的数据为归一化之后的
每0.5s更新一次数据，每次更新数据增加（去掉）550个点
'''




# 模拟数据
def randn_point():
    # 产生-1到1之间的550个随机数据
    y = np.random.randint(-1, 1, 2200)
    return y

sns.set_style("whitegrid")

# 创建画布，包含2个子图,分别是I和Q，后期可以再增加
fig = plt.figure(figsize=(15, 10))
ax1 = fig.add_subplot(2, 1, 1)
ax2 = fig.add_subplot(2, 1, 2)

# 先绘制初始图形，每个子图包含1个正弦波和三个点的散点图
x = np.arange(0, 2200, 1)  # x轴

y = randn_point()

line1, = ax1.plot(x, randn_point())

line2, = ax2.plot(x, randn_point())


def init():

    # 构造开始帧函数init
    # 改变y轴数据，x轴不需要改
    line1.set_ydata(y)
    line2.set_ydata(y)
    label = 'timestep {0}'.format(0)
    ax1.set_xlabel(label)
    return line1, line2, ax1  # 注意返回值，我们要更新的就是这些数据


def animate(i):
    # 接着，构造自定义动画函数animate，用来更新每一帧上各个x对应的y坐标值，参数表示第i帧
    # plt.cla() 这个函数很有用，先记着它
    line1.set_ydata(y)
    line2.set_ydata(y)
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
                                  interval=20,
                                  blit=False)
    plt.show()

