from sklearn import linear_model
from numpy import asarray


class LinearRegression:
    @staticmethod
    def create_model(x, y):
        """
        Gets model for linear regression for 1D input (x, y),
        assuming x and y are equal length
        """
        # Reshape to spec
        x = asarray(x).reshape(-1, 1)
        y = asarray(y).reshape(-1, 1)

        # Perform regression with model
        model = linear_model.LinearRegression()
        model.fit(x, y)

        return model
