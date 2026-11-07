from typing import Dict, Any, List
import numpy as np


class ScenarioGenerator:
    """
    Constructs Bullish, Base, and Bearish scenario estimates with
    80% and 95% parametric confidence intervals.
    """

    DISCLAIMER = (
        "Regulatory and Analytical Notice: Forecasts are quantitative statistical estimates "
        "derived from historical trend and time-series patterns. They do not constitute "
        "guaranteed market returns or investment recommendations."
    )

    @classmethod
    def generate_scenarios(
        cls,
        base_projection: float,
        residual_std: float,
        horizon_steps: int = 1,
        bull_multiplier: float = 1.15,
        bear_multiplier: float = 0.85,
    ) -> Dict[str, Any]:
        """
        Generates Base, Bullish, and Bearish projections with standard errors.
        """
        # Compounding uncertainty over horizon
        uncertainty = residual_std * np.sqrt(horizon_steps)
        if uncertainty == 0:
            uncertainty = base_projection * 0.05

        # 95% confidence interval bounds (z ~ 1.96)
        ci_95_lower = max(0.0, base_projection - (1.96 * uncertainty))
        ci_95_upper = base_projection + (1.96 * uncertainty)

        # 80% confidence interval bounds (z ~ 1.28)
        ci_80_lower = max(0.0, base_projection - (1.28 * uncertainty))
        ci_80_upper = base_projection + (1.28 * uncertainty)

        bullish_val = base_projection * bull_multiplier
        bearish_val = max(0.0, base_projection * bear_multiplier)

        return {
            "base": round(float(base_projection), 2),
            "bullish": round(float(bullish_val), 2),
            "bearish": round(float(bearish_val), 2),
            "confidence_intervals": {
                "ci_95": {"lower": round(float(ci_95_lower), 2), "upper": round(float(ci_95_upper), 2)},
                "ci_80": {"lower": round(float(ci_80_lower), 2), "upper": round(float(ci_80_upper), 2)},
            },
            "disclaimer": cls.DISCLAIMER,
        }

