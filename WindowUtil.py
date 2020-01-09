#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygetwindow
import ctypes
import win32gui
import win32.constants as win32Constant
# import sys
# sys.path.append("/path/to/my/modules/")
# import my_module
#import importlib
#win32Constant = importlib.import_module('.constants', 'xpra-3.0.4.xpra.platform.win32')
# import importlib.util
# spec = importlib.util.spec_from_file_location("constants", "xpra-3.0.4/xpra/platform/win32/constants.py")
# win32Constant = importlib.util.module_from_spec(spec)
# spec.loader.exec_module(win32Constant)
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

    @staticmethod
    def isWindow(windowHandle):
        return ctypes.windll.user32.isWindow(windowHandle)

class WindowController:
    def __init__(self, **kwargs):
        self._windowInfo = None
        self._hwnd = None
        if 'handle' in kwargs:
            self._hwnd = kwargs['handle']
        elif 'title' in kwargs:
            programWinTitle = kwargs['title']
            winTitles = pygetwindow.getWindowsWithTitle(programWinTitle)
            targetWinTitle = None
            for winTitle in winTitles:
                if programWinTitle == winTitle.title:
                    targetWinTitle = winTitle
                    break

            if targetWinTitle == None:
                raise Exception(programWinTitle + " could not be found...")
            else:
                self._hwnd = targetWinTitle._hWnd

    @property
    def hwnd(self):
        return self._hwnd

    @property
    def windowInfo(self):
        return self._windowInfo

    def bringToFront(self):
        win32gui.ShowWindow(self.hwnd, win32Constant.SW_RESTORE)
        win32gui.BringWindowToTop(self.hwnd)
        #win32gui.SetForegroundWindow(self.hwnd)
        win32gui.ShowWindow(self.hwnd, win32Constant.SW_SHOWNORMAL)

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




