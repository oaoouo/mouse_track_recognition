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
"""

import redis


def read_traning_file(path):
    """
    读取训练数据文件中读取数据
    """
    with open(path, 'rb') as f:
        data = f.read()
    data_list = data.split('\n')
    return data_list


def store_data_in_redis(data_list):
    """
    将数据格式化存入redis
    """ 
    db.flushall()
    for data in data_list[:3000]:
        subdatas = data.split(';')
        id = subdatas[0].split()[0]
        tracks = [subdatas[0].split()[1]]
        for subdata in subdatas[1:-1]:
            tracks.append(subdata)
        target = subdatas[-1].split()[0]
        label = subdatas[-1].split()[1]
        # 数据存储到redis数据库中
        ## {'id':
        ##     {'target': 'x, y',
        ##      'tracks': "['x1,y1,t1', 'x2,y2,t2']",
        ##      'label': '1'
        ##     }
        ## }
        db.hset(id, 'tracks', tracks) 
        db.hset(id, 'target', target) 
        db.hset(id, 'label', label) 
    db.save()


if __name__ == '__main__':
    db = redis.StrictRedis(host='127.0.0.1', port=6379)
    data_list = read_traning_file('./ml/dsjtzs_txfz_traning.txt')
    store_data_in_redis(data_list)
