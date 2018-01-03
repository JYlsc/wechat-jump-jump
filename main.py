#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/2 10:17
# @Author  : Leishichi
# @File    : main.py
# @Software: PyCharm
# @Tag:

import cv2
import os
import time
import math
import numpy as np

# 指令集
cut_command = "adb shell screencap -p /sdcard/n.png "
get_command = "adb pull /sdcard/n.png ."
click_command = "adb shell input swipe "

# 读取小人图片
people_img = cv2.imread('./img/people_720.png')

# 720 分辨率下小人中心偏移像素
# 1440 分辨率下需重新计算
# 中心点应该
x_720 = 26
y_720 = 138

# 720 分辨率下 distance 与 time的关系为
# time = (distance + b) * w
# w = 1440 / 分辨率
# b需要手动进行调试优化
b_720 = 27
w_720 = 2

cut_size = 300


def jump(distance):
    """
    模拟跳跃
    :param distance: 距离
    :return:
    """
    # 防止被反外挂监测出，更改每次点击的位置
    x = distance / 3
    y = distance
    t = get_time(distance)
    command = click_command + " {} {} {} {} {}".format(x, y, x, y, t)
    run(command)

    if t > 1000:
        t = 1.2 + (t % 100) / 1000
        time.sleep(t)
    else:
        t = 1 + (t % 100) / 1000
        time.sleep(t)


def get_people_center(x, y):
    """
    获取小人的中心点
    :param x:
    :param y:
    :return:
    """
    return x + x_720, y + y_720


def get_people_left(img):
    """
    使用图片匹配获取小人的左上角坐标
    :param img:
    :return:
    """
    res1 = cv2.matchTemplate(img, people_img, cv2.TM_CCOEFF_NORMED)
    min_val1, max_val1, min_loc1, max_loc1 = cv2.minMaxLoc(res1)
    return max_loc1[0], max_loc1[1]


def get_distance(img):
    # 获取小人左上角坐标
    lx, ly = get_people_left(img)

    # 获取小人中心点坐标
    px, py = get_people_center(lx, ly)

    img = cv2.GaussianBlur(img, (5, 5), 0)
    canny = cv2.Canny(img, 1, 10)

    # 消除小人影响
    for i in range(ly - 250, ly + 200, 1):
        for b in range(lx - 10, lx + 70, 1):
            canny[i][b] = 0

    # 计算物块上沿的坐标
    y = np.nonzero([max(row) for row in canny[:]])[0][0]

    # 获取物体最终的x值
    x = int(np.mean(np.nonzero(canny[y])))

    # 角度固定为30度，
    # 根据勾股定理算出偏移量
    y = int(py - abs(px - x) / 1.733)

    return int(math.sqrt((px - x) ** 2 + (py - y) ** 2))



def run(command):
    os.system(command)


def get_time(distance):
    return int((distance + 27) * 2)


if __name__ == "__main__":
    while True:
        run(cut_command)
        run(get_command)
        img = cv2.imread('./n.png')[cut_size:, :]
        distance = get_distance(img)
        jump(distance)


