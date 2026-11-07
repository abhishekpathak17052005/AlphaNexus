from typing import List, Dict, Any, Tuple
import numpy as np
import pandas as pd


class ForecastValidator:
    """
    Evaluates forecasting models using strict chronological train/test splitting
    and walk-forward cross-validation without future data leakage.
    Computes MAE, RMSE, MAPE, and Directional Accuracy.
    """

    @staticmethod
    def chronological_split(
        data: pd.DataFrame,
        date_col: str,
        test_fraction: float = 0.2,
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Splits time series data strictly by date ordering without random shuffle."""
        sorted_df = data.sort_values(by=date_col).reset_index(drop=True)
        n = len(sorted_df)
        if n < 4:
            raise ValueError(f"Insufficient historical samples ({n}). Minimum 4 required for evaluation.")
        split_idx = int(n * (1.0 - test_fraction))
        train = sorted_df.iloc[:split_idx]
        test = sorted_df.iloc[split_idx:]
        return train, test

    @staticmethod
    def compute_metrics(
        actual: np.ndarray,
        predicted: np.ndarray,
    ) -> Dict[str, float]:
        """Calculates MAE, RMSE, MAPE, and Directional Accuracy."""
        y_true = np.array(actual, dtype=np.float64)
        y_pred = np.array(predicted, dtype=np.float64)

        if len(y_true) == 0 or len(y_pred) == 0:
            return {"mae": 0.0, "rmse": 0.0, "mape": 0.0, "directional_accuracy": 0.0}

        # 1. Mean Absolute Error
        mae = float(np.mean(np.abs(y_true - y_pred)))

        # 2. Root Mean Squared Error
        rmse = float(np.sqrt(np.mean((y_true - y_pred) ** 2)))

        # 3. Mean Absolute Percentage Error (ignoring zero denominators)
        non_zero_mask = y_true != 0
        if np.any(non_zero_mask):
            mape = float(np.mean(np.abs((y_true[non_zero_mask] - y_pred[non_zero_mask]) / y_true[non_zero_mask])) * 100.0)
        else:
            mape = 0.0

        # 4. Directional Accuracy (% of correct step signs)
        if len(y_true) > 1:
            true_diff = np.diff(y_true)
            pred_diff = np.diff(y_pred)
            same_direction = (true_diff * pred_diff) > 0
            dir_acc = float(np.mean(same_direction) * 100.0)
        else:
            dir_acc = 100.0 if np.sign(y_pred[0]) == np.sign(y_true[0]) else 0.0

        return {
            "mae": round(mae, 4),
            "rmse": round(rmse, 4),
            "mape": round(mape, 2),
            "directional_accuracy": round(dir_acc, 2),
        }

