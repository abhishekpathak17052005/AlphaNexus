# ALPHANEXUS – Econometric Forecasting Engine

## 1. Overview

The Forecasting Engine generates forward-looking estimates for revenue, EBITDA, and EPS over 1-to-8 forward quarters using econometric time-series models and Monte Carlo simulations.

---

## 2. Multi-Scenario Modeling

- **Base Case:** Historical walk-forward exponential trend with autoregressive momentum.
- **Bullish Case:** Accelerated topline expansion with margin upside multiplier (default +15%).
- **Bearish Case:** Downside scenario modeling demand contraction and cost inflation (default -15%).

---

## 3. Parametric Confidence Intervals

Constructs 80% ($z \approx 1.28$) and 95% ($z \approx 1.96$) parametric bounds that widen realistically across the forecast horizon as compounding uncertainty increases ($\sigma \cdot \sqrt{t}$).
