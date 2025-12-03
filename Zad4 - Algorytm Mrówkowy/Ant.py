import random

import numpy as np

'''Klasa mrówki'''
class Ant:
    def __init__(self,
                 attractionID: int,
                 matrix: np.ndarray,
                 alpha: float,
                 beta: float,
                 p_random: float,):
        self.attractionID = attractionID,
        self.alpha = alpha,
        self.beta = beta
        self.matrix = matrix
        self.p_random = p_random

        # Wartości początkowe dla wędrówki
        self.visited = {attractionID}
        self.attractionID = attractionID
        self.trackLength = 0

    ''' Funkcja wyboru nastepnej atrakcji do odwiedzenia przez mrowke '''
    def nextAttraction(self):
        # wybor losowej atrakcji
        p = random.random()
        if p < self.p_random:
            # TODO: wybor losowej atrakcji
        # TODO: wybor atrakcji na podstawie matrix