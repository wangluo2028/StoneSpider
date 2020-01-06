#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum
import treelib

class GameStatus(Enum):
    NotStart = 1
    BattleNet = 2
    Welcome = 3
    BattleMode = 4
    AdventureMode = 5


class GameState(treelib.Node):
    def __init__(self, tag=None, identifier=None, expanded=True, data=None):
        super.__init__(tag, identifier, expanded, data)




