"""
Arene class
"""
import uuid
import string
from typing import List
import numpy as np
from model.robot import Robot


class Arene:
    """
    Arene class
    """
    # pylint: disable=too-many-instance-attributes
    rows = 0
    columns = 0
    grid = robots = []
    goal_position = ()
    win = False
    win_id = []
    win_nb_move = []
    logger = None
    uuid = None

    def __init__(self, rows=0, columns=0, logger=None):
        """
        docstring
        """
        self.win_id = []
        self.win_nb_move = []
        self.uuid = uuid.uuid4()
        self.rows = rows
        self.columns = columns
        self.logger = logger
        self.grid = np.zeros((rows, columns), dtype=int)
        self.goal_position = self.generate_position()
        self.grid[self.goal_position] = 99


    def add_robots(self, robots: List[Robot] = None):
        """
        Add Robots to the arena
        """
        if robots is None:
            robots = []
        for index, robot in enumerate(robots):
            robot.ident = index+1
            robot.logger = self.logger
            robot.goal_position = self.goal_position
            robot.position = self.generate_position()
            robot.positionlist.append(robot.position)
            self.grid[robot.position] = robot.ident
            

        for robot in robots:
            robot.grid = self.grid

        self.robots = robots

    def generate_position(self):
        """
        Generate position on grid
        """
        i, j = np.where(self.grid == 0)
        position = (int(np.random.choice(i)), int(np.random.choice(j)))

        return position

    def run(self, lap):
        """
        Run game
        """
        for robot in self.robots:
            robot.grid = self.grid
            if robot.move():
                self.grid = robot.grid
                
                if robot.win:
                    self.win = True
                    self.win_id.append(robot.ident)
                    self.win_nb_move.append(robot.nb_move)
            #robot.position = (int(robot.position[0]), int(robot.position[1]))
            #print(robot.position)
            robot.positionlist.append(robot.position)
            #print(robot.positionlist)
            #print(type(robot.position[0]))
        #print(self.grid)
        
