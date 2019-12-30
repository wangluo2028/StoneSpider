#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ctypes

class WindowInfo:
    def __init__(self, windowRect):
        self._left = windowRect.left
        self._top = windowRect.top
        self._right = windowRect.right
        self._bottom = windowRect.bottom

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right

    @property
    def top(self):
        return self._top

    @property
    def bottom(self):
        return self._bottom

    @property
    def width(self):
        return self._right - self._left

    @property
    def height(self):
        return self._bottom - self._top


class WindowUtil:
    @staticmethod
    def getWindowInfo(windowHandle):
        try:
            windowAttrFunc = ctypes.windll.dwmapi.DwmGetWindowAttribute
        except WindowsError:
            windowAttrFunc = None

        rect = ctypes.wintypes.RECT()
        if windowAttrFunc:  # Vista & 7 stuff
            DWMWA_EXTENDED_FRAME_BOUNDS = 9
            windowAttrFunc(ctypes.wintypes.HWND(windowHandle),
              ctypes.wintypes.DWORD(DWMWA_EXTENDED_FRAME_BOUNDS),
              ctypes.byref(rect),
              ctypes.sizeof(rect)
              )
        else:
            rect.
        windowInfo = WindowInfo(rect)
