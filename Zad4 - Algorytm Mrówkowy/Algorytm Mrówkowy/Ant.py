import numpy as np
class Ant:
    def __init__(self,
                 attractionID: int,
                 matrix: np.ndarray,
                 alpha: float,
                 beta: float,):
        self.attractionID = attractionID,
        self.alpha = alpha,
        self.beta = beta
        self.matrix = matrix

        # Wartości początkowe dla wędrówki
        self.tour = [attractionID]
        self.visited = {attractionID}
        self.attractionID = attractionID
        self.trackLength = 0