#!/usr/bin/env python
# -*- coding: utf-8 -*-

class IGameStateController:
    def __init__(self, thisState, nextState):
        self._thisState = thisState
        self._nextState = nextState

    def execute(self):
        pass


class GameExecutableProgram(IGameStateController):
    def __init__(self, thisState, nextState):
        super.__init__(thisState, nextState)

class GameButtonOnScreenShot(IGameStateController):
    def __init__(self, thisState, nextState):
        super.__init__(thisState, nextState)


