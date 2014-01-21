# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

class player:
    def __init__(self, starting_pos):
        self.current_pos = starting_pos
    
    def get_current(self):
        return self.current_pos
    
    def change_pos(self, next_pos):
        self.current_pos = next_pos
        

