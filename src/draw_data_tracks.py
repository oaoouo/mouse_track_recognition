#coding: utf-8

"""
    draw_data_tracks.py
    ```````````````````

    根据数据库中的测试数据绘制轨迹

    + 使用matplotlib绘图
        - 官方: https://matplotlib.org/
        - 快速上手: https://zhuanlan.zhihu.com/p/28993962
"""

import sys
import numpy as np
import matplotlib
from mpl_toolkits import mplot3d
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import redis
import math


def scatter3D_x_y_t(N):
    """
    各个id轨迹点(x,y,t)的三维分布
    相同id轨迹点的颜色相同
    """
    for id in xrange(N):
        x = y = t = []
        tracks = eval(db.hget(id+1, 'tracks'))
        label = db.hget(id+1, 'label')
        for track in tracks:
            x.append(float(track.split(',')[0]))
            y.append(float(track.split(',')[1]))
            t.append(float(track.split(',')[2]))
        ax.scatter3D(t, x, y)
    fig1.savefig('track.png')


def plot_v_t(N):
    """
    各个id数据的速度与时间的二维关系
    机器轨迹: 灰色
    人类轨迹: 红色
    """
    for id in xrange(N):
        v = t = []
        tracks = eval(db.hget(id+1, 'tracks'))
        label = db.hget(id+1, 'label')
        for pos in range(len(tracks)-1):
            track = tracks[pos]
            next_track = tracks[pos+1]
            track_list = track.split(',')
            next_track_list = next_track.split(',')

            x1 = float(track_list[0])
            y1 = float(track_list[1])
            t1 = float(track_list[2])

            x2 = float(next_track_list[0])
            y2 = float(next_track_list[1])
            t2 = float(next_track_list[2])

            di = 1  # 方向
            if x2 < x1: di = -1
            elif x2 == x1 and y2 < y1: di = -1
            distance = math.sqrt(math.pow((x2-x1), 2) + math.pow((y2-y1), 2))
            _dt = t2 - t1
            if _dt == 0:  # 奇怪...有时间点相等的数据(比如2596)
                continue
            _v = float((distance / _dt) * di)
            
            v.append(_v); t.append(t1+(t2-t1)/2)
        if label == '0':
            ax.plot(t, v, 'C7')
            ax_c.plot(t, v, 'C7')
        if label == '1':
            ax.plot(t, v, 'C3')
            ax_m.plot(t, v, 'C3')
    fig2.savefig('v_t.png')


if __name__ == '__main__':
    db = redis.StrictRedis(host='localhost', port=6379)

    if sys.argv[1] == 'track':
        fig1 = plt.figure()
        ax = plt.axes(projection='3d')
        ax.set_title('the track point distribution')
        ax.set_xlabel('time')
        ax.set_ylabel('x-coordinate')
        ax.set_zlabel('y-coordinate')
        scatter3D_x_y_t(3000)

    if sys.argv[1] == 'speed':
        fig2, axes = plt.subplots(nrows=2, ncols=2)
        ax = axes.ravel()[0]
        ax_m = axes.ravel()[2]  # 子图(人类)
        ax_c = axes.ravel()[3]  # 子图(电脑)
        axes.ravel()[1].axis('off') # 隐藏子图1
        plot_v_t(3000)
