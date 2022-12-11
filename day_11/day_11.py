from __future__ import annotations

from dataclasses import dataclass, field
import re
import math

MONKEY_REGEX_STR = r"""Monkey (?P<monkey_id>\d):
[\s]{2}Starting items: (?P<items>[\d,\s]*)
[\s]{2}Operation: new = old (?P<operator>[+*-]) (?P<other>old|[\d]*)
[\s]{2}Test: divisible by (?P<test>\d*)
[\s]{4}If true: throw to monkey (?P<true_target>\d*)
[\s]{4}If false: throw to monkey (?P<false_target>\d*)"""

WORRY_DIVIDER = 3
ROUNDS = 10000

@dataclass
class Monkey:
    id: int
    items: list[int]
    operation: str
    operation_num: str
    test: int
    true_target: int
    false_target: int
    inspect_count: int = field(default=0)
    
    def play(self, monkeys: list[Monkey]) -> None:
        for _ in range(len(self.items)):
            self.inspect_count += 1
            worry = self.inspect(self.items.pop())
            worry //= WORRY_DIVIDER
            
            if worry % self.test == 0:
                monkeys[self.true_target].catch(worry)
            else:
                monkeys[self.false_target].catch(worry)
    
    def inspect(self, item: int) -> int:
        num = item if self.operation_num == "old" else int(self.operation_num)
        
        match self.operation:
            case '+':
                return item + num
            case '*':
                return item * num
            case _:
                raise RuntimeError("Operation unclear, elf stuck in machinery")

    def catch(self, item:int) -> None:
        self.items.append(item)

    def __str__(self) -> str:
        return f"Monkey {self.id}: {self.items}"


class Game:

    def __init__(self, monkeys: list[Monkey], max_rounds: int) -> None:
        self.monkeys = monkeys
        self.round = 0
        self.max_rounds = max_rounds
    
    def play_round(self):
        self.round += 1
        for monkey in self.monkeys:
            monkey.play(self.monkeys)
    
    def ended(self) -> bool:
        return self.round >= self.max_rounds
    
    def report_round(self) -> None:
        print(f"Round {self.round}")
        for monkey in self.monkeys:
            print(monkey)
    
    def report_game(self) -> None:
        for monkey in self.monkeys:
            print(f"Monkey {monkey.id}: {monkey.inspect_count}")
        
        shenanigans = [monkey.inspect_count for monkey in self.monkeys]
        shenanigans.sort(reverse=True)
        print(math.prod(shenanigans[:2]))

def main():
    monkeys = get_monkeys()
    game = Game(monkeys, ROUNDS)
    
    while not game.ended():
        game.play_round()
        game.report_round()
    
    game.report_game()

def get_monkeys() -> list[Monkey]:
    monkey_regex = re.compile(MONKEY_REGEX_STR)
    
    with open("input/day_11", mode="r", encoding="UTF-8") as file:
        monkeys_str = file.read()
    
    matches = monkey_regex.findall(monkeys_str)
    
    monkeys: list[Monkey] = []
    for match in matches:
        match_dict = {k:v for k, v in zip(monkey_regex.groupindex.keys(), match)}
        
        items = [int(item) for item in match_dict["items"].split(", ")]
        
        monkeys.append(Monkey(id=match_dict["monkey_id"],
                              items=items, 
                              operation=match_dict["operator"],
                              operation_num=match_dict["other"],
                              test=int(match_dict["test"]),
                              true_target=int(match_dict["true_target"]),
                              false_target=int(match_dict["false_target"])
                              ))
        
    return monkeys


if __name__ == "__main__":
    main()