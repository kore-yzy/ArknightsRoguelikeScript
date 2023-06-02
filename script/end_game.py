#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import time

import win32api
import win32con


class EndGame:
    def __init__(self, conf, pos_x, pos_y):
        self._conf = conf
        self._pos_x = pos_x
        self._pos_y = pos_y

    def quit(self):
        self.click(self._conf.getint('end', 'quit_x') + self._pos_x,
                   self._conf.getint('end', 'quit_y') + self._pos_y)

        self.click(self._conf.getint('end', 'give_up_x') + self._pos_x,
                   self._conf.getint('end', 'give_up_y') + self._pos_y)

        self.click(self._conf.getint('end', 'confirm_x') + self._pos_x,
                   self._conf.getint('end', 'confirm_y') + self._pos_y)

        submit_pos = (self._conf.getint('end', 'confirm_quit_x') + self._pos_x,
                      self._conf.getint('end', 'confirm_quit_y') + self._pos_y)
        time.sleep(3)
        self.click(submit_pos[0], submit_pos[1])
        time.sleep(10)
        self.click(submit_pos[0], submit_pos[1])
        time.sleep(1)
        self.click(submit_pos[0] - 100, submit_pos[1])

        self.click(self._conf.getint('end', 'blank_x') + self._pos_x,
                   self._conf.getint('end', 'blank_y') + self._pos_y)

    @staticmethod
    def click(pos_x, pos_y):
        win32api.SetCursorPos([pos_x, pos_y])
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN | win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        time.sleep(1)
