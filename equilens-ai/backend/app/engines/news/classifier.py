import re
from typing import Tuple


class NewsEventClassifier:
    """
    Classifies corporate news and announcements into domain-specific event categories.
    Categories: Earnings, Acquisitions, Mergers, Contracts, Partnerships,
    Government orders, Regulatory action, Management changes, Fundraising, Dividends, Industry news.
    """

    CATEGORIES = {
        "Earnings": [
            r"\b(earnings|quarterly results|q[1-4]|pat up|pat down|net profit|ebitda|financial results)\b"
        ],
        "Acquisitions": [
            r"\b(acquire|acquisition|takeover|buys stake|purchased stake|acquires)\b"
        ],
        "Mergers": [
            r"\b(merger|amalgamation|consolidation|scheme of arrangement)\b"
        ],
        "Contracts": [
            r"\b(secures order|bags.*order|bags.*deal|order win|awarded contract|contract win|contract worth|deal signed|deal with)\b"
        ],
        "Government orders": [
            r"\b(defence ministry|railway tender|nhai|government order|psu tender|ministry awards)\b"
        ],
        "Partnerships": [
            r"\b(partnership|strategic alliance|mou signed|collaborates|joint venture|tie-up)\b"
        ],
        "Regulatory action": [
            r"\b(sebi|rbi notice|usfda|show cause|penalty|inspection|investigation|audit objection)\b"
        ],
        "Management changes": [
            r"\b(ceo|cfo|managing director|steps down|resigns|appointed|board appoints|executive)\b"
        ],
        "Fundraising": [
            r"\b(qip|rights issue|preferential allotment|raises funds|ipo|bond issue|debentures)\b"
        ],
        "Dividends": [
            r"\b(dividend|interim dividend|final dividend|special dividend|payout)\b"
        ],
    }

    @classmethod
    def classify(cls, title: str, description: str) -> str:
        text = f"{title} {description}".lower()
        for category, patterns in cls.CATEGORIES.items():
            for p in patterns:
                if re.search(p, text):
                    return category
        return "Industry news"
