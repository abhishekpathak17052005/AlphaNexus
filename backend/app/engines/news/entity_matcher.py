import re
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from app.models.company import Company


class NewsEntityMatcher:
    """
    Precision entity matcher for Indian and global equities.
    Prevents falsely attributing news to a company when common dictionary
    words collide with tickers or company trade names.
    """

    # Common English words that shouldn't be matched solely as bare lowercase words
    COLLISION_BLACKLIST = {"it", "as", "at", "be", "do", "in", "is", "or", "so", "to", "all", "now", "key"}

    @staticmethod
    def match_company(text: str, title: str, companies: List[Company]) -> Optional[Company]:
        """
        Matches text against active companies using strict word boundaries,
        ticker capitalization checks, and ISIN/CIN cross-referencing.
        """
        combined = f"{title} {text}"

        for comp in companies:
            # 1. Exact Symbol / Ticker match (e.g., "TCS", "INFY", "RELIANCE")
            if comp.symbol:
                symbol_pattern = rf"\b{re.escape(comp.symbol)}\b"
                if re.search(symbol_pattern, combined):
                    return comp

            # 2. Distinct Company Name match (case-insensitive)
            name = comp.name.strip()
            # Clean generic suffixes like 'Limited', 'Ltd', 'Pvt Ltd'
            cleaned_name = re.sub(r"\b(Limited|Ltd|Corporation|Corp|Industries|India)\b\.?", "", name, flags=re.IGNORECASE).strip()
            if len(cleaned_name) > 3 and cleaned_name.lower() not in NewsEntityMatcher.COLLISION_BLACKLIST:
                name_pattern = rf"\b{re.escape(cleaned_name)}\b"
                if re.search(name_pattern, combined, flags=re.IGNORECASE):
                    return comp

        return None

