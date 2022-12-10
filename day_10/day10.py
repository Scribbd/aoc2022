from dataclasses import dataclass

class CPU:
    
    def __init__(self) -> None:
        self.X = 1
        self.cycle = 0
        self._history_x = []
    
    def noop(self):
        self._history_x.append(self.X)
        self.cycle += 1
    
    def addx(self, V: int):
        self.noop()
        self.cycle += 1
        self._history_x.append(self.X)
        self.X += V
    
    @property
    def history_x(self):
        return self._history_x #+ [self.X]
    
    def get_x_at_cycle(self, i:int) -> int:
        return self.history_x[i-1]

class GPU:
    
    def __init__(self, height:int, width:int) -> None:
        self.height = height
        self.width = width
        self.pixels: list[list[int]] = []
        for _ in range(height):
            self.pixels.append(["." for _ in range(width)])
            
    def simulate_crt(self, x_history):
        for x, line in enumerate(self.pixels):
            for y, _ in enumerate(line):
                cycle = self.width * x + y
                sprite_center = x_history[cycle]
                
                if sprite_center < -2 or sprite_center > self.width + 2:
                    continue
                
                sprite = [sprite_center-1, sprite_center, sprite_center+1]
                
                if y in sprite:
                    self.pixels[x][y] = "#"

    def draw(self):
        for line in self.pixels:
            print("".join(line))
        
def main():
    cpu = CPU()
    gpu = GPU(6, 40)
    
    noop_count = 0
    addx_count = 0
    
    for instruction in get_instructions():
        if instruction.startswith("noop"):
            cpu.noop()
            noop_count += 1
        elif instruction.startswith("addx"):
            args = instruction.split(" ")
            cpu.addx(int(args[1]))
            addx_count += 1
        else:
            print(f"instuctions unclear, dick stuck in cpu: {instruction}")
    
    values = []
    
    for i in range(20, len(cpu.history_x),40):
        values.append(cpu.get_x_at_cycle(i) * i)
    
    print("Summary")
    print(f"Ops: {len(cpu.history_x)} {cpu.cycle}")
    print(f" noops: {noop_count} {noop_count*1}")
    print(f" addx {addx_count} {addx_count*2}")
    print(f"Values: {values}")
    print(sum(values))
    
    gpu.simulate_crt(cpu.history_x)
    gpu.draw()
    

def get_instructions() -> list[str]:
    with open("input/day_10", mode="r", encoding="UTF-8") as file:
        lines = file.readlines()
    
    return [line.rstrip() for line in lines]

if __name__ == "__main__":
    main()