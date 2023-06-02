#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os.path
import time

import pyautogui
import win32api
import win32con

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 1
path = os.path.abspath('.') + r'\data\event'


class Gaming:
    def __init__(self, conf, pos_x, pos_y, logger):
        self._conf = conf
        self._pos_x = pos_x
        self._pos_y = pos_y
        self._event_images_lis = os.listdir(path)
        self._logger = logger
        self._cnt = 0

    def recognize_next_event(self):
        temp = self.get_first_branch()
        if 0 == temp:
            return -1
        pos_x, pos_y = temp.left, temp.top + 40
        self.click(pos_x, pos_y)
        for index, image in enumerate(self._event_images_lis):
            image_path = os.path.join(path, image)
            rect = pyautogui.locateOnScreen(image_path, confidence=0.8, region=(self._pos_x, self._pos_y, 1280, 720))
            if rect:
                return index
        return -1

    def action(self):
        self._cnt = 0
        event_num = self.recognize_next_event()
        if -1 == event_num:
            return 0, self._cnt
        elif 0 == event_num or 3 == event_num:
            self.buqieryu()
        elif 1 == event_num:
            self.guiyixingshang()
            return 0, self._cnt
        elif event_num in (2, 4, 5, 6, 7):
            event_name = self._event_images_lis[event_num].split('.')[0]
            deploy_x = self._conf.getint('gaming', f'{event_name}_x') + self._pos_x
            deploy_y = self._conf.getint('gaming', f'{event_name}_y') + self._pos_y
            skill_x = self._conf.getint('gaming', f'{event_name}_skill_x') + self._pos_x
            skill_y = self._conf.getint('gaming', f'{event_name}_skill_y') + self._pos_y
            offset = self._conf.getint('gaming', f'{event_name}_x_offset')
            direc = self._conf.get('gaming', f'{event_name}_direc')

            status = self.fight(deploy_x, deploy_y, skill_x, skill_y, offset, direc)
            if 0 == status:
                return 0, self._cnt
        else:
            return 0, self._cnt
        return 1, self._cnt

    def buqieryu(self):
        self.click(self._conf.getint('gaming', 'enter_x') + self._pos_x,
                   self._conf.getint('gaming', 'enter_y') + self._pos_y)
        # time.sleep(5)
        self.click(self._conf.getint('gaming', 'enter_x') + self._pos_x,
                   self._conf.getint('gaming', 'enter_y') + self._pos_y)
        for i in range(1, 4):
            self.click(self._conf.getint('gaming', 'buqieryu_x') + self._pos_x,
                       self._conf.getint('gaming', f'buqieryu_y_{i}') + self._pos_y)
            rect = pyautogui.locateOnScreen('data/buqieryu/is_ok.png',
                                            confidence=0.8, region=(self._pos_x, self._pos_y, 1280, 720))
            if rect:
                self.click(self._conf.getint('gaming', 'buqieryu_x') + self._pos_x,
                           self._conf.getint('gaming', f'buqieryu_y_{i}') + self._pos_y)
                time.sleep(3)
                self.click(self._conf.getint('gaming', 'buqieryu_x') + self._pos_x,
                           self._conf.getint('gaming', f'buqieryu_y_{i}') + self._pos_y)
                break

    def guiyixingshang(self):
        self.click(self._conf.getint('gaming', 'enter_x') + self._pos_x,
                   self._conf.getint('gaming', 'enter_y') + self._pos_y)
        rect = pyautogui.locateOnScreen('data/bank/touzhi.png',
                                        confidence=0.8, region=(self._pos_x, self._pos_y, 1280, 720))
        if rect:
            self.click(rect.left, rect.top)

            self.click(self._conf.getint('gaming', 'touzhirukou_x') + self._pos_x,
                       self._conf.getint('gaming', 'touzhirukou_y') + self._pos_y)

            while True:
                self.click(self._conf.getint('gaming', 'touzhi_enter_x') + self._pos_x,
                           self._conf.getint('gaming', 'touzhi_enter_y') + self._pos_y)
                self._cnt += 1

                rec = pyautogui.locateOnScreen('data/bank/shouxian.png',
                                               confidence=0.8, region=(self._pos_x, self._pos_y, 1280, 720))
                if rec:
                    self._logger.info(f'此次投资了{self._cnt}。。。')
                    break

    def fight(self, deploy_x, deploy_y, skill_x, skill_y, offset, direc):
        current_x = self._conf.getint('gaming', 'shan_x') + self._pos_x
        current_y = self._conf.getint('gaming', 'shan_y') + self._pos_y
        self.click(self._conf.getint('gaming', 'enter_x') + self._pos_x,
                   self._conf.getint('gaming', 'enter_y') + self._pos_y)
        self.click(self._conf.getint('gaming', 'start_action_x') + self._pos_x,
                   self._conf.getint('gaming', 'start_action_y') + self._pos_y)
        time.sleep(7)
        self.click(self._conf.getint('gaming', 'mul_x') + self._pos_x,
                   self._conf.getint('gaming', 'mul_y') + self._pos_y)
        time.sleep(1)
        self.move(current_x, current_y, deploy_x + offset, deploy_y)
        if 'left' == direc:
            self.move(deploy_x, deploy_y, deploy_x - 500, deploy_y)
        elif 'right' == direc:
            self.move(deploy_x, deploy_y, deploy_x + 500, deploy_y)
        time.sleep(3)
        self.click(deploy_x, deploy_y)
        self.click(skill_x, skill_y)
        status = self.is_over()
        if 0 == status:
            return 0
        self.click(skill_x, skill_y)
        while True:
            rect = pyautogui.locateOnScreen('data/over/over.png',
                                            confidence=0.8, region=(self._pos_x, self._pos_y, 1280, 720))
            if rect:
                break
            self.click(self._conf.getint('gaming', 'money_x') + self._pos_x,
                       self._conf.getint('gaming', 'money_y') + self._pos_y)
        self.click(rect.left, rect.top)
        self.click(rect.left + self._conf.getint('gaming', 'over_x_off'),
                   rect.top + self._conf.getint('gaming', 'over_y_off'))

    def get_first_branch(self):
        rect = pyautogui.locateAllOnScreen('data/other/xiayibu.png',
                                           confidence=0.8, region=(self._pos_x, self._pos_y, 1280, 720))
        lis = list(rect)
        if 0 == len(lis):
            return 0
        return lis[0]

    def is_over(self):
        while True:
            time.sleep(10)
            fight_over_rect = pyautogui.locateOnScreen('data/over/fight_over.png',
                                                       confidence=0.8, region=(self._pos_x, self._pos_y, 1280, 720))
            game_over_rect = pyautogui.locateOnScreen('data/over/game_over.png',
                                                      confidence=0.8, region=(self._pos_x, self._pos_y, 1280, 720))
            if fight_over_rect:
                return 1

            if game_over_rect:
                return 0

    @staticmethod
    def move(current_x, current_y, target_x, target_y):
        pyautogui.moveTo(current_x, current_y, duration=0.5)
        pyautogui.dragTo(target_x, target_y, duration=1)
        pyautogui.mouseUp()

    @staticmethod
    def click(pos_x, pos_y):
        win32api.SetCursorPos([pos_x, pos_y])
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN | win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        time.sleep(1)
