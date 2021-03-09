"""
A model of the Master Lock Speed Dial (1500iD) lock (also known as Master Lock One).
It will tell you the internal state of the lock, given a list of moves.

The utility of this is admittedly limited. I have used it to generate possible
sequences to find alternative sequences that will all unlock the lock. The
results are unsurprising and not particularly interesting.

Based on research and documentation by Michael Huebler:

https://toool.nl/images/e/e5/The_New_Master_Lock_Combination_Padlock_V2.0.pdf
"""

class Wheel:

    def __init__(self, init_state = (0,0)):
        self.init_state = init_state
        self.N = init_state[0] 
        self.M = init_state[1]

    def pin0(self):
        if self.M in [0, 1]:
            self._incN()
        self.M = 0

    def pin1(self):
        if self.M in [1]:
            self._incN()
        self.M = 1

    def pinminus1(self):
        self._incN()
        self.M = -1

    def _incN(self):
        self.N += 1
        if self.N == 5:
            self.N = 0

    @property
    def position(self):
        pos = (self.N * 72) + (self.M * 24)
        if pos > 360:
            pos -= 360
        if pos < 0:
            pos += 360
        return pos

    def reset(self):
        self.N = self.init_state[0] 
        self.M = self.init_state[1]

    def __repr__(self):
        return "{0.N}; {0.M} - Angle: {0.position}".format(self)


class Lock:
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3
    SYMBOLS = "URDL"

    def __init__(self, initial_state = ((0,0),(0,0),(0,0),(0,0)), gate_pos = ((2, -1), (1, 0), (2, 1), (2, 0))):
        self.wheels = [Wheel(initial_state[n]) for n in range(4)]
        self.moves = []
        self.gate_pos = gate_pos

    def reset(self):
        self.moves = []
        [wheel.reset() for wheel in self.wheels]

    def state(self):
        return tuple([(wheel.N, wheel.M) for wheel in self.wheels])

    def pull(self):
        state = self.state()
        gates_aligned = [ t[0] == t[1] for t in zip( self.gate_pos, state) ]
        gates_aligned_count = gates_aligned.count(True)
        
        if gates_aligned_count == 1:
          return 'binding on ' + self.SYMBOLS[gates_aligned.index(True)]
        elif state == self.gate_pos: 
          return 'open'
        if gates_aligned_count > 1:
          return 'binding on more than one wheel'
        else:
          return 'closed'
          

    def moves_str(self):
        return " ".join([self.SYMBOLS[move] for move in self.moves])

    def __repr__(self):
        return "Moves: " + self.moves_str() + "\n" + "\n".join([
            "Wheel {0}: {1}".format(idx, wheel) for idx, wheel in enumerate(self.wheels)
        ])

    def _act(self, a, b, c):
        self.wheels[a].pin0()
        self.wheels[b].pin1()
        self.wheels[c].pinminus1()

    def up(self):
        self.moves.append(self.UP)
        self._act(0, 1, 3)

    def down(self):
        self.moves.append(self.DOWN)
        self._act(2, 3, 1)

    def left(self):
        self.moves.append(self.LEFT)
        self._act(3, 0, 2)

    def right(self):
        self.moves.append(self.RIGHT)
        self._act(1, 2, 0)
