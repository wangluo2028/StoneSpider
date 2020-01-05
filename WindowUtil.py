#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygetwindow
import ctypes
import win32gui
import importlib
import win32.constants
#win32Constant = importlib.import_module('.constants', 'xpra-3.0.4.xpra.platform.win32')
import mss, mss.tools

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
        windowInfo = WindowInfo(rect)

        return windowInfo

class WindowController:
    def __init__(self, programWinTitle):
        winTitles = pygetwindow.getWindowsWithTitle(programWinTitle)
        targetWinTitle = None
        for winTitle in winTitles:
            if programWinTitle == winTitle.title:
                targetWinTitle = winTitle
                break

        if targetWinTitle == None:
            raise Exception(programWinTitle+" could not be found...")
        else:
            self._targetWinTitle = targetWinTitle
            self._hwnd = targetWinTitle._hWnd
            self._windowInfo = None

    @property
    def hwnd(self):
        return self._hwnd

    @property
    def windowInfo(self):
        return self._windowInfo

    def bringToFront(self):
        self._targetWinTitle.restore()
        win32gui.BringWindowToTop(self.hwnd)
        #win32gui.SetForegroundWindow(self.hwnd)
        SW_SHOWNORMAL = 1
        win32gui.ShowWindow(self.hwnd, win32.constants.SW_SHOWNORMAL)

    def refreshWindowRect(self):
        self._windowInfo = WindowUtil.getWindowInfo(self.hwnd)

    def takeScreenshot(self):
        self.refreshWindowRect()
        self.bringToFront()

        screenShot = None
        with mss.mss() as sct:
            screenShot = sct.grab({
                'left': self.windowInfo.left, 'top': self.windowInfo.top,
                'width': self.windowInfo.width, 'height': self.windowInfo.height
            })

        return screenShot




