"""
Game class
"""
#from _typeshed import Self
import time
import uuid
import json
import os
import csv
import numpy as np
from typing import List
from .robot import Robot
from .arene import Arene


class Game:
    """ Game class """
    arena = None
    logger = None

    def __init__(self, silent = True):
        self.lap = 0
        self.uuid = uuid.uuid4()
        self.filename = "logs/" +str(self.uuid)+".json"
        self.silent = silent

    def init_arena(self, rows=10, columns=10):
        """ Init arena """
        self.arena = Arene(rows=rows, columns=columns, logger=self.logger)
        self.arena.add_robots([Robot(), Robot(), Robot(), Robot(), Robot()])
        #print(f"goal : {self.arena.goal_position}")

    def run(self):
        """ Run the game """
        game_win = False
        current_lap = 0
        self.init_arena()

        while not game_win:
            current_lap += 1
            self.lap = current_lap
            self.arena.run(current_lap)
            game_win = self.arena.win
            if current_lap > 20: 
                break

        self.save(True,True)
        if self.silent:
            print("log env == goal: {} , Win robots: {}, nb laps: {}" 
                .format(self.arena.goal_position, self.arena.win_id, self.arena.win_nb_move))

    def save(self, tojson = True, tocsv= True):
        """
        Log main
        """
        logs_dict = {
            "main" :
             {
                "gridshape" : (self.arena.rows,self.arena.columns),
                "goal": self.arena.goal_position,
                "win" : self.arena.win_id,
                'laps': self.lap
            },
            'robots' : [robot.positionlist for robot in self.arena.robots]
        }
        self.logs_dict = logs_dict
        #print(self.logs_dict)
        
        if tojson : 
            with open(self.filename, "w") as outfile:
                json.dump(self.logs_dict, outfile)
        
        if tocsv:
            data = {
                "filename": self.filename,
                'nb_lap': self.lap,
                "nb_agents": len(self.arena.robots)
                }
            filename = "results.csv"
            header = ['filename', 'nb_lap', 'nb_agents']
            write_header = False
            if not os.path.exists(filename):
                write_header = True

            with open(filename, 'a', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=header)
                if write_header:
                    writer.writeheader()
                writer.writerow(data)