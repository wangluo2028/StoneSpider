#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum

class Language(Enum):
    Chinese = 1
    English = 2


class HearthstoneLang:
    def __init__(self, battleNetLang = Language.Chinese):
        self._hsLang = None
        self._hsWindowTitles = {Language.Chinese: '炉石传说', Language.English: 'Hearthstone'}
        self._thisHsWindowTitle = None

        self._battleNetLang = battleNetLang
        self._battleNetWindowTitles = {Language.Chinese:'暴雪战网', Language.English:'Blizzard Battle'}
        self._thisBattleNetWindowTitle = self._battleNetWindowTitles.get(self._battleNetLang, 'no supported language')

    @property
    def hsLang(self):
        return self._hsLang

    @hsLang.setter
    def hsLang(self, value):
        self._hsLang = value
        self._thisHsWindowTitle = self.hsWindowTitles.get(self.hsLang, 'language not supported')

    @property
    def hsWindowTitles(self):
        return self._hsWindowTitles

    @property
    def hsWindowTitle(self):
        return self._thisHsWindowTitle

    @property
    def battleNetLang(self):
        return self._battleNetLang

    @battleNetLang.setter
    def battleNetLang(self, value):
        self._battleNetLang = value
        self._thisBattleNetWindowTitle = self._battleNetWindowTitles.get(self.battleNetLang, 'language not supported')

    @property
    def battleNetWindowTitles(self):
        return self._battleNetWindowTitles

    @property
    def battleNetWindowTitle(self):
        return self._thisBattleNetWindowTitle


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