#!/usr/bin/env python
# -*- coding: utf-8 -*-

import networkx
import treelib
import GameState

graph = networkx.Graph()
graph.add_edge()

class GameMachine:
    def __init__(self):
        self._nodes = {}
        self._gameTree = treelib.Tree()
        self._gameTree.node_class = GameState
        gameRoot = self._gameTree.create_node('Root', 'Root')
        notStart = self._gameTree.create_node('NotStart', 'NotStart', parent=gameRoot)
        loginIn = self._gameTree.create_node('LoginIn', 'LoginIn', parent=notStart)
        battleNet = self._gameTree.create_node('BattleNet', 'BattleNet', parent=loginIn)
        hearthstone = self._gameTree.create_node('Hearthstone', 'Hearthstone', parent=battleNet)
        self._gameTree.create_node('Welcome', 'Welcome', parent=hearthstone)
        battleMode = self._gameTree.create_node('BattleMode', 'BattleMode', parent=hearthstone)
        adventureMode = self._gameTree.create_node('AdventureMode', 'AdventureMode', parent=hearthstone)
        self._currentState = None
        self._gameGraph = networkx.DiGraph()