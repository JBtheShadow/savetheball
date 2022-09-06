from enum import Enum

class Player:
    def __init__(self):
        self.radius = 20
        self.x = -100
        self.y = -100
        self.paused_x = None
        self.paused_y = None
        self.died_x = None
        self.died_y = None

class Game:
    class State(Enum):
        MENU = 1
        PAUSED = 2
        RUNNING = 3
        ENDED = 4

    def __init__(self):
        self.difficulty = 1
        self.state = self.State.MENU
        self.curr_level = 0
        self.score = 0