#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum

class Language(Enum):
    Chinese = 1
    English = 2


class HearthstoneLang:
    def __init__(self, language):
        self._language = language
        self._windowTitles = {Language.Chinese:'炉石传说', Language.English:'Hearthstone'}
        self._thisWindowTitle = self._windowTitles.get(self._language, 'not supported language')

    @property
    def windowTitle(self):
        return self._thisWindowTitle


    # @property
    # def x(self):
    #     """I'm the 'x' property."""
    #     return self._x
    #
    # @x.setter
    # def x(self, value):
    #     self._x = value
    #
    # @x.deleter
    # def x(self):
    #     del self._x