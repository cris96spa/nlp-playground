import numpy as np


class Environment:
    """
    Environment class that models a simple economic interaction with
    demand functions and objective evaluations based on input variables.
    """

    def __init__(self):
        """
        Initializes the Environment with a fixed demand scale and sets a random seed
        for reproducibility in sampling noise.
        """
        self.scale = 1
        np.random.seed(42)

    def demand(self, x: np.ndarray) -> np.ndarray:
        """
        Computes the base demand as a Gaussian-like function.

        Parameters:
            x (np.ndarray): Input values for which demand is evaluated.

        Returns:
            np.ndarray: Demand values computed as scale * exp(-((2 * x)^2)).
        """
        return self.scale * np.exp(-((2 * x) ** 2))

    def objective_function(
        self, x: np.ndarray, y: np.ndarray, ly_x=0, lx_y=0
    ) -> np.ndarray:
        """
        Computes the objective function as a linear combination of x and y,
        weighted by their respective adjusted demands.

        Parameters:
            x (np.ndarray): Input values for the x-variable.
            y (np.ndarray): Input values for the y-variable.
            ly_x (float): Cross-effect coefficient for y's demand added to x's.
            lx_y (float): Cross-effect coefficient for x's demand added to y's.

        Returns:
            np.ndarray: Computed objective values.
        """
        return x * self.demand_x(x, y, ly_x) + y * self.demand_x(y, x, lx_y)

    def demand_x(self, x: np.ndarray, y: np.ndarray, l=0) -> np.ndarray:
        """
        Adjusts the demand for x by incorporating a linear combination of x's
        and y's demand, allowing for interaction effects.

        Parameters:
            x (np.ndarray): Primary input values.
            y (np.ndarray): Secondary input values to influence demand.
            l (float): Coefficient for y's demand influence on x's.

        Returns:
            np.ndarray: Adjusted demand values.
        """
        return self.demand(x) + l * self.demand(y)

    def sample(self, X, noise=True):
        """
        Samples from the objective function, optionally adding Gaussian noise.

        Parameters:
            X (tuple of np.ndarray): Tuple (X[0], X[1]) representing x and y inputs.
            noise (bool): Whether to add noise to the sampled values.

        Returns:
            np.ndarray: Noisy or noise-free samples from the objective function.
        """
        if noise:
            noise = np.random.normal(0, self.scale * 0.1, X[0].shape)
        else:
            noise = 0
        return self.objective_function(X[0], X[1]) + noise

    def sample_demand_x(self, X, noise=True, l=0):
        """
        Samples from the adjusted demand_x function, optionally adding Gaussian noise.

        Parameters:
            X (tuple of np.ndarray): Tuple (X[0], X[1]) representing x and y inputs.
            noise (bool): Whether to add noise to the demand values.
            l (float): Coefficient for cross-influence of y on x in demand.

        Returns:
            np.ndarray: Noisy or noise-free samples from demand_x.
        """
        if noise:
            noise = np.random.normal(0, self.scale * 0.1, X[0].shape)
        else:
            noise = 0
        return self.demand_x(X[0], X[1], l=l) + noise
