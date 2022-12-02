#!/bin/env python

from enum import Enum, auto

class MatchScore(Enum):
    win:int = 6
    draw:int = 3
    loss:int = 0

class Shape(Enum):
    rock = auto()
    paper = auto()
    scissors = auto()

class AnswerMapping(Enum):
    X:Shape = Shape.rock
    Y:Shape = Shape.paper
    Z:Shape = Shape.scissors

class QuestionMapping(Enum):
    A:Shape = Shape.rock
    B:Shape = Shape.paper
    C:Shape = Shape.scissors
    

win_list = ["A Y", "B Z", "C X"]
draw_list = ["A X", "B Y", "C Z"]
score_map = { Shape.rock: 1, Shape.paper: 2, Shape.scissors: 3 }
score = 0

with open("input/day_2", mode="r", encoding="UTF-8") as file:
    for line in file.readlines():
        trimmed = line.rstrip()
        if trimmed in win_list:
            score += MatchScore.win.value
        if trimmed in draw_list:
            score += MatchScore.draw.value
            
        shapes = trimmed.split(" ")
        score += score_map[AnswerMapping[shapes[1]].value]

print(score)