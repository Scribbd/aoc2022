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

class ConditionMapping(Enum):
    X: MatchScore = MatchScore.loss
    Y: MatchScore = MatchScore.draw
    Z: MatchScore = MatchScore.win

class QuestionMapping(Enum):
    A:Shape = Shape.rock
    B:Shape = Shape.paper
    C:Shape = Shape.scissors
    

loss_map = { Shape.rock: Shape.scissors, Shape.scissors: Shape.paper, Shape.paper: Shape.rock}
win_map = {v:k for k,v in loss_map.items()}
score_map = { Shape.rock: 1, Shape.paper: 2, Shape.scissors: 3 }
score = 0

with open("input/day_2", mode="r", encoding="UTF-8") as file:
    for line in file.readlines():
        environment = line.rstrip().split(" ")
        question:Shape = QuestionMapping[environment[0]].value
        condition:MatchScore = ConditionMapping[environment[1]].value
        # Add known round score
        score += condition.value
        answer:Shape = question
        match condition:
            case MatchScore.win:
                answer = win_map[question]
            case MatchScore.loss:
                answer = loss_map[question] 
        
        score += score_map[answer]

print(score)