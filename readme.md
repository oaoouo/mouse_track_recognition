# Mouse Track Recognition

> 鼠标轨迹识别

https://bdc.saikr.com/vse/bdc/2017

## 先画些简单的图

### 每个id数据经过的轨迹点分布

#### 所有数据
![](https://raw.githubusercontent.com/oaoouo/mouse_track_recognition/master/imgs/track.png)

#### 正常轨迹数据
![](https://raw.githubusercontent.com/oaoouo/mouse_track_recognition/master/imgs/track_h.png)

#### 机器轨迹数据
![](https://raw.githubusercontent.com/oaoouo/mouse_track_recognition/master/imgs/track_c.png)

**结论**:

    呃... 人类和机器数据轨迹没有很大区别, 毕竟移动鼠标进行验证的路径是固定的.
    所以看看能不能从速度的变化进行区分.

### 每个id数据在相邻时间间隔内的平均速度与时间的关系

![](https://raw.githubusercontent.com/oaoouo/mouse_track_recognition/master/imgs/v_t.png)

+ 第一幅图是所有数据
+ 红色是正常数据, 灰色是机器数据

**结论**
<img src="https://user-images.githubusercontent.com/31455293/30903351-0f16940e-a3a1-11e7-9876-d558949a1eac.jpg" width = "300" height = "300" alt="" align=center />

或许是我图画错了.... <br>
比较奇怪的是, 训练数据中存在时间相同但是轨迹(x, y)不同的点, 比如: id=2596

    290,2737,247;304,2737,247

### 每个id速度和加速度的二维分布: 有效果了!

![](https://raw.githubusercontent.com/oaoouo/mouse_track_recognition/master/imgs/v_a.png)

+ 红色是人类轨迹; 绿色是机器轨迹;

**结论**

    速度人类和机器基本在一个区间(个别机器轨迹更快一点);
    但是加速度区别就很大了, 人类对速度的把控没有机器强, 机器基本是匀速的,
    而人类加速度区间的范围就很大了.
