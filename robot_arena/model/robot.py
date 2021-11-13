"""
Robot class
"""


import numpy as np


class Robot:
    """
    Robot class
    """
    position = (int(0), int(0))
    ident = 0
    grid = np.empty(0)
    goal_position = None
    win = False
    logger = None
    # other neighbors (diag),(1,1),(1,-1),(-1,1),(-1,-1)]
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # cross neighbors
    nb_move = 0

    def __init__(self):
        self.positionlist = []

    def __repr__(self):
        """
        __repr__
        """
        return str(f"<Robot ident:{self.ident}, position: {self.position}")

    def move(self):
        """
        move
        """
        target_position = tuple(
            map(lambda i, j: i - j, self.position, self.goal_position))

        run_x, run_y = self.compute_tmp_move(target_position=target_position)

        return self.validate_move(move_x=run_x, move_y=run_y)

    def compute_tmp_move(self, target_position):
        """
        compute_tmp_move
        """
        tmp_move_x = self.get_new_position(
            self.position[0], target_position[0])
        tmp_move_y = self.get_new_position(
            self.position[1], target_position[1])

        return tmp_move_x, tmp_move_y

    def validate_move(self, move_x, move_y):
        """
        validate_move
        """
        # if self.grid[move_x, move_y] == 0 or self.grid[move_x, move_y] >= 99:
        #     if self.grid[move_x, move_y] >= 99:
        if self.grid[move_x, move_y] == 0 or (move_x, move_y) == self.goal_position:
            if (move_x, move_y) == self.goal_position:
                self.win = True
            # on remove l'ancienne position
            self.grid[self.position] = 0
            self.grid[move_x, move_y] += self.ident
            self.position = (int(move_x), int(move_y))
            
            self.nb_move += 1

            return True

        return False

    def show_neighbors(self):
        """
        show_neighbors
        """
        for i, j in self.neighbors:
            neighbor = self.position[0] + i, self.position[1] + j
            self.logger.log("neighbors", self.ident, neighbor[0], neighbor[1])

    @staticmethod
    def get_new_position(actual, target):
        """
        get_new_position
        """
        tmp_move = actual
        if target < 0:
            tmp_move = actual + 1
        elif target > 0:
            tmp_move = actual - 1

        return tmp_move
