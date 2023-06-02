#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import time

import pyautogui
import win32api
import win32con


class StartGame:
    def __init__(self, conf, pos_x, pos_y):
        self._handle = 0
        self._sub_handle = 0
        self._conf = conf
        self._pos_x = pos_x
        self._pos_y = pos_y

    def start_explore(self):
        self.click(self._conf.getint('start', 'explore_x') + self._pos_x,
                   self._conf.getint('start', 'explore_y') + self._pos_y)

    def select_team_and_comb(self, is_team=True):
        if is_team:
            x = self._conf.getint('start', f'team_x') + self._pos_x
            y = self._conf.getint('start', f'team_y') + self._pos_y
            is_team = False
        else:
            x = self._conf.getint('start', f'comb_x') + self._pos_x
            y = self._conf.getint('start', f'comb_y') + self._pos_y
            is_team = True
        self.click(x, y)
        self.click(x, y)
        if not is_team:
            self.select_team_and_comb(is_team)

    def select_person(self):
        recruit_pos = (self._conf.getint('start', 'recruit_x') + self._pos_x,
                       self._conf.getint('start', 'recruit_y') + self._pos_y)
        for i in range(1, 4):
            self.click(self._conf.getint('start', f'person_{i}_x') + self._pos_x,
                       self._conf.getint('start', f'person_{i}_y') + self._pos_y)
            if 1 == i:
                # 山
                rect = pyautogui.locateOnScreen('data/other/shan.png',
                                                confidence=0.8, region=(self._pos_x, self._pos_y, 1280, 720))
                # 煌
                # rect = pyautogui.locateOnScreen('data/other/huang.png',
                #                                 confidence=0.8, region=(self._pos_x, self._pos_y, 1280, 720))
                self.click(rect.left, rect.top)
                # self.click(self._conf.getint('start', 'shan_x') + self._pos_x,
                #            self._conf.getint('start', 'shan_y') + self._pos_y)
                self.click(recruit_pos[0], recruit_pos[1])
                time.sleep(5)
                self.click(recruit_pos[0], recruit_pos[1])
            else:
                self.click(recruit_pos[0], recruit_pos[1])
                self.click(self._conf.getint('start', 'confirm_x') + self._pos_x,
                           self._conf.getint('start', 'confirm_y') + self._pos_y)
                time.sleep(1)

        self.click(self._conf.getint('start', 'start_x') + self._pos_x,
                   self._conf.getint('start', 'start_y') + self._pos_y)

    def formation(self):
        self.click(self._conf.getint('start', 'formation_x') + self._pos_x,
                   self._conf.getint('start', 'formation_y') + self._pos_y)

        self.click(self._conf.getint('start', 'add_person_x') + self._pos_x,
                   self._conf.getint('start', 'add_person_y') + self._pos_y)

        self.click(self._conf.getint('start', 'add_shan_x') + self._pos_x,
                   self._conf.getint('start', 'add_shan_y') + self._pos_y)

        self.click(self._conf.getint('start', 'skill_x') + self._pos_x,
                   self._conf.getint('start', 'skill_y') + self._pos_y)

        self.click(self._conf.getint('start', 'formation_x') + self._pos_x,
                   self._conf.getint('start', 'formation_y') + self._pos_y)

        self.click(self._conf.getint('start', 'return_x') + self._pos_x,
                   self._conf.getint('start', 'return_y') + self._pos_y)

    @staticmethod
    def click(pos_x, pos_y):
        win32api.SetCursorPos([pos_x, pos_y])
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN | win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        time.sleep(1)

    def init(self):
        self.start_explore()
        self.select_team_and_comb()
        self.select_person()
        time.sleep(5)
        self.formation()
