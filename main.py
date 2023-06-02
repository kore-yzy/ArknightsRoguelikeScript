import configparser
import logging
import os.path
import random
import time
from datetime import datetime

import pyautogui
import win32gui

from script.end_game import EndGame
from script.gaming import Gaming
from script.start_game import StartGame
# https://pypi.tuna.tsinghua.edu.cn/simple

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 1
pyautogui.size()


def log():
    logger = logging.getLogger("log")
    logger.setLevel(logging.INFO)

    ch = logging.FileHandler(filename=rf'data\logs\log-{datetime.timestamp(datetime.now())}.log', encoding='utf8')
    ch.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')

    ch.setFormatter(formatter)

    logger.addHandler(ch)

    return logger


def parse_ini():
    path = os.path.abspath('.') + r'\docs\setting.ini'
    conf = configparser.ConfigParser()
    conf.read(path)
    return conf


def find_window(conf):
    handle = win32gui.FindWindow(0, conf.get('basic', 'window_title'))
    if handle != 0:
        sub_handle = win32gui.FindWindowEx(handle, 0, 0, None)
        if sub_handle != 0:
            rect = win32gui.GetWindowRect(sub_handle)
            pos_x = rect[0]
            pos_y = rect[1]
            return pos_x, pos_y
    return 0, 0


def main():
    conf = parse_ini()
    logger = log()
    times, cnt = 0, 0
    pos_x, pos_y = 0, 0
    while not pos_x and not pos_y:
        pos_x, pos_y = find_window(conf)
    start = StartGame(conf, pos_x, pos_y)
    gaming = Gaming(conf, pos_x, pos_y, logger)
    end = EndGame(conf, pos_x, pos_y)
    while True:
        times += 1
        logger.info(f'即将开始第{times}次探索。。。')

        start.init()
        while True:
            time.sleep(2)
            status, num = gaming.action()
            cnt += num
            if 0 == status:
                break
        end.quit()
        logger.info(f'第{times}次探索结束，截至当前一共投资了{cnt}。。。')


if __name__ == '__main__':
    main()
