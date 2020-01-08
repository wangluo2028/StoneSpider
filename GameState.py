#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import IntEnum
import treelib

class GameStatus(IntEnum):
    NoStatus = 1
    NotStart = auto()
    Started = auto()
    Login = auto()
    BattleNet = auto()
    BattleNetSystemTray = auto()
    BattleNetHeartStone = auto()



class GameState(treelib.Node):
    def __init__(self, tag=None, identifier=None, expanded=True, data=None):
        super.__init__(tag, identifier, expanded, data)




