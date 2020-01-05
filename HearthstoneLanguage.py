#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum

class Language(Enum):
    Chinese = 1
    English = 2


class HearthstoneLang:
    def __init__(self, hsLang, battleNetLang = Language.Chinese):
        self._hsLang = hsLang
        self._hsWindowTitles = {Language.Chinese: '炉石传说', Language.English: 'Hearthstone'}
        self._thisHsWindowTitle = self._hsWindowTitles.get(self._hsLang, 'not supported language')

        self._battleNetLang = battleNetLang
        self._battleNetWindowTitles = {Language.Chinese:'暴雪战网', Language.English:'Blizzard Battle.net'}
        self._thisBattleNetWindowTitle = self._battleNetWindowTitles.get(self._battleNetLang, 'not supported language')

    @property
    def hsWindowTitle(self):
        return self._thisHsWindowTitle


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