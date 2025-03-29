import numpy as np


class Environment:
    def __init__(self):
        self.scale = 1
        np.random.seed(42)

    def demand(self, x: np.ndarray) -> np.ndarray:
        return self.scale * np.exp(-((2 * x) ** 2))

    def objective_function(
        self, x: np.ndarray, y: np.ndarray, ly_x=0, lx_y=0
    ) -> np.ndarray:
        return x * self.demand_x(x, y, ly_x) + y * self.demand_x(y, x, lx_y)

    def demand_x(self, x: np.ndarray, y: np.ndarray, l=0) -> np.ndarray:
        return self.demand(x) + l * self.demand(y)

    def sample(self, X, noise=True):
        if noise:
            noise = np.random.normal(0, self.scale * 0.1, X[0].shape)
        else:
            noise = 0
        return self.objective_function(X[0], X[1]) + noise

    def sample_demand_x(self, X, noise=True, l=0):
        if noise:
            noise = np.random.normal(0, self.scale * 0.1, X[0].shape)
        else:
            noise = 0
        return self.demand_x(X[0], X[1], l=l) + noise
