# Mouse Track Recognition

> 鼠标轨迹识别

https://bdc.saikr.com/vse/bdc/2017

## 先画些简单的图

### 每个id数据经过的轨迹点分布

+ 所有数据
![](https://raw.githubusercontent.com/oaoouo/mouse_track_recognition/master/imgs/track.png)

+ 正常轨迹数据
![](https://raw.githubusercontent.com/oaoouo/mouse_track_recognition/master/imgs/track_h.png)

+ 机器轨迹数据
![](https://raw.githubusercontent.com/oaoouo/mouse_track_recognition/master/imgs/track_c.png)

**结论**:

    呃... 人类和机器数据轨迹没有很大区别, 毕竟移动鼠标进行验证的路径是固定的.
    所以看看能不能从速度的变化进行区分.

### 每个id数据在相邻时间间隔内的平均速度与时间的关系
