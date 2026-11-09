from typing import List, Tuple, Dict, Any, Optional
import numpy as np
from sklearn.linear_model import LinearRegression


class BaselineForecaster:
    """
    Autoregressive and linear-trend baseline model for financial metrics.
    Robust to small sample sizes commonly found in annual financial statements.
    """

    def __init__(self):
        self.model = LinearRegression()
        self.residual_std = 0.0

    def fit_predict(
        self,
        historical_values: List[float],
        forecast_steps: int = 3,
    ) -> Tuple[List[float], float]:
        """
        Fits trend regression on historical sequence and forecasts next N steps.
        Returns (predicted_values, residual_std).
        """
        if len(historical_values) < 2:
            raise ValueError(f"Insufficient historical data: {len(historical_values)} points. Minimum 2 required.")

        y = np.array(historical_values, dtype=np.float64)
        X = np.arange(len(y)).reshape(-1, 1)

        self.model.fit(X, y)
        in_sample_preds = self.model.predict(X)
        residuals = y - in_sample_preds
        self.residual_std = float(np.std(residuals)) if len(residuals) > 1 else float(y[-1] * 0.05)

        # Predict future steps
        future_X = np.arange(len(y), len(y) + forecast_steps).reshape(-1, 1)
        future_preds = self.model.predict(future_X)

        return [round(float(p), 2) for p in future_preds], self.residual_std

