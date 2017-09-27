#coding: utf-8

"""
    set_traning_data.py
    ```````````````````

    将训练数据按照格式存储到redis数据库中

    训练数据格式
     __________________________________________
    | a1      bigint      id                   |
    | a2      string  (x, y, t) 鼠标移动轨迹   |
    | a3      string  (x, y)    目标坐标       |
    | Label   string  1(正常轨迹), 0(机器轨迹) |
    |__________________________________________|

    + redis: https://redis.io/
        - 数据库是NoSql数据库, 适合简单的非关系型键值对存储以及用作缓存
"""

# Python redis-py 包, 提供redis数据库的Python接口
## 文档: https://redis-py.readthedocs.io/en/latest/index.html#module-redis
## 源代码: https://github.com/andymccurdy/redis-py
import redis


def read_traning_file(path):
    """
    从训练数据文件中读取数据
    """
    with open(path, 'rb') as f:
        data = f.read()
    # 使用with语句, 语句块结束后会自动做清除工作
    # 这里就是自动关闭文件: f.close() 

    # split 作用字符串, 根据split的参数将字符串截断
    # 并将截断后的字符串放置到列表中供索引
    # dsjtzs_txfz_traning.txt文件中, 每行是一个特定id的数据
    # 所以以换行符'\n'分割从文件中读出的字符串
    data_list = data.split('\n')
    return data_list


def store_data_in_redis(data_list):
    """
    将数据格式化存入redis

    思路:
        data_list列表的每个元素就是特定id的数据字符串,例如第0个元素(id=1的数据)

        1 353,2607,349;367,2607,376;388,2620,418;416,2620,442;500,2620,493;584,2620,547;675,2620,592;724,2620,643;780,2620,694;822,2620,742;850,2633,793;885,2633,844;934,2633,895;983,2633,946;1060,2633,1006;1144,2633,1063;1235,2633,1093;1284,2633,1144;1312,2633,1210;1326,2633,1243;1333,2633,1354;1354,2633,1408;1375,2646,1450;1452,2659,1492;1473,2672,1543;1480,2672,1954;1487,2672,2050;1494,2672,2233;1501,2672,2245;1515,2672,2293;1515,2659,2347;1522,2659,2554;1529,2659,2722;1543,2659,2773;1550,2659,2794;1564,2659,2842;1578,2659,2893;1592,2659,2944;1599,2659,2992;1606,2659,3043;1613,2659,3100;1620,2659,3178;1634,2659,3220;1648,2659,3244;1669,2659,3301;1676,2646,3445;1690,2646,3490;1718,2633,3547;1732,2633,3592;1739,2633,3646;1732,2633,4930;1725,2633,4981;1718,2620,6466;1704,2620,6562;1704,2607,6598;1697,2607,7237; 1420.5,202 1

        这行数据以分号分隔的是鼠标经过的轨迹点坐标(x, y, t).
        但是第一个和最后一个是特例, 分别包含了空格分隔的id和label

        所以第一个和最后一个单独处理, 提取出id和label.
        剩下的轨迹点放入一个tracks列表中(不要漏了第一个起始点)
        最后target(x, y)单独拿出
    """ 
    db.flushall() # 每次更新redis存储前清除旧数据
    for data in data_list[:3000]:
        subdatas = data.split(';')
        id = subdatas[0].split()[0]  # 提取id
        tracks = [subdatas[0].split()[1]]  # 先放入起始点
        for subdata in subdatas[1:-1]:
            tracks.append(subdata)  # 加入其余轨迹点
        target = subdatas[-1].split()[0]  # 提取target
        label = subdatas[-1].split()[1]  # 提取label
        # 数据存储到redis数据库中的结构
        ## {'id':
        ##     {'target': 'x, y',
        ##      'tracks': "['x1,y1,t1', 'x2,y2,t2']",
        ##      'label': '1'
        ##     }
        ## }
        # 数据存储到redis数据库中
        db.hset(id, 'tracks', tracks) 
        db.hset(id, 'target', target) 
        db.hset(id, 'label', label) 
    db.save()  # 保存数据


if __name__ == '__main__':
    db = redis.StrictRedis(host='127.0.0.1', port=6379)  # redis数据库连接句柄
    data_list = read_traning_file('./ml/dsjtzs_txfz_traning.txt')
    store_data_in_redis(data_list)
