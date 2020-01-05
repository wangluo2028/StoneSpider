#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum
import networkx
import treelib

graph = networkx.Graph()
graph.add_edge()

class GameStatus(Enum):
    NotStart = 1
    BattleNet = 2
    Welcome = 3
    BattleMode = 4
    AdventureMode = 5


class GameState:
    def __init__(self):
        pass

class GameMachine:
    def __init__(self):
        self._nodes = {}
        self._gameTree = treelib.Tree()
        gameRoot = self._gameTree.create_node('Root', 'Root')
        self._gameTree.create_node('NotStart', 'NotStart', parent=gameRoot)
        self._gameTree.create_node('BattleNet', 'BattleNet', parent=gameRoot)
        hearthstone = self._gameTree.create_node('Hearthstone', 'Hearthstone', parent=gameRoot)
        self._gameTree.create_node('Welcome', 'Welcome', parent=hearthstone)
        self._gameTree.create_node('BattleMode', 'BattleMode', parent=hearthstone)
        self._gameTree.create_node('AdventureMode', 'AdventureMode', parent=hearthstone)

