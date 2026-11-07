from typing import List, Dict, Any, Optional
import pandas as pd
import numpy as np


class PeerAnalyzer:
    """
    Analyzes and compares multiple companies side-by-side across
    valuation multiples, profitability, capital efficiency, and leverage.
    """

    @staticmethod
    def compare_companies(companies_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Takes a list of company metrics and computes sector averages,
        percentile rankings, and side-by-side matrices.
        """
        if not companies_data:
            return {"peers": [], "benchmarks": {}}

        df = pd.DataFrame(companies_data)

        # Calculate averages for numeric metrics
        numeric_cols = [
            "market_cap", "pe_ratio", "pb_ratio", "roe", "roce",
            "dividend_yield", "ebitda_margin", "net_profit_margin", "revenue_growth"
        ]

        benchmarks: Dict[str, Any] = {}
        for col in numeric_cols:
            if col in df.columns:
                series = pd.to_numeric(df[col], errors="coerce").dropna()
                if not series.empty:
                    benchmarks[col] = {
                        "mean": round(float(series.mean()), 2),
                        "median": round(float(series.median()), 2),
                        "min": round(float(series.min()), 2),
                        "max": round(float(series.max()), 2),
                    }

        # Add relative ranking
        peer_list = []
        for c in companies_data:
            peer_item = dict(c)
            # Add valuation score (simple z-score / ranking heuristic)
            peer_list.append(peer_item)

        return {
            "peer_count": len(companies_data),
            "benchmarks": benchmarks,
            "peers": peer_list,
        }

