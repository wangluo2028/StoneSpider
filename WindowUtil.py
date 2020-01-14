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
import pyautogui
import numpy as np
import cv2

class WindowInfo:
    def __init__(self, windowRect):
        self._left = windowRect.left
        self._top = windowRect.top
        self._right = windowRect.right
        self._bottom = windowRect.bottom
        self._screenShot = None

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
        #win32gui.ShowWindow(self.hwnd, win32Constant.SW_MINIMIZE)
        win32gui.ShowWindow(self.hwnd, win32Constant.SW_SHOWNORMAL)

    def refreshWindowRect(self):
        self._windowInfo = WindowUtil.getWindowInfo(self.hwnd)

    def takeScreenshot(self):
        self.bringToFront()
        self.refreshWindowRect()

        self._screenShot = None
        with mss.mss() as sct:
            self._screenShot = sct.grab({
                'left': self.windowInfo.left, 'top': self.windowInfo.top,
                'width': self.windowInfo.width, 'height': self.windowInfo.height
            })

        return self._screenShot

    def clickButtonImage(self, buttonImage):
        screenShotData = np.array(self._screenShot)
        # cv2.imshow('test', screenShotData)
        # if (cv2.waitKey(1) & 0xFF) == ord('q'):
        #     cv2.destroyAllWindows()
        screenShotPath = 'shot.png'
        mss.tools.to_png(self._screenShot.rgb, self._screenShot.size, output=screenShotPath)
        try:
            buttonImageLocation = pyautogui.locate(buttonImage, screenShotPath)
            buttonImagePosition = pyautogui.center(buttonImageLocation)
            self.clickButtonPosition(buttonImagePosition)
            print('click')
        except Exception as e:
            print('locate error' + str(e))

    def clickButtonPosition(self, buttonPosition):
        pyautogui.click(buttonPosition.x + self.windowInfo.left, buttonPosition.y + self.windowInfo.top)




