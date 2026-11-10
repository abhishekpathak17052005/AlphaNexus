# ALPHANEXUS – Liquid Glass UI Implementation Guide

## 1. Using Glass Cards in Streamlit

```python
from components.cards import render_metric_card

render_metric_card(
    title="RETURN ON EQUITY (FY24)",
    value="24.8%",
    delta="+180 bps YoY",
    delta_type="positive",
    subtitle="DuPont analysis reflects operating margin expansion.",
)
```

## 2. Rendering Evidentiary Chat Citations

```python
from components.chat import render_chat_message

render_chat_message(
    role="assistant",
    content="Operating revenue grew 15.2% driven by automotive and energy verticals.",
    citations=[
        {
            "document_name": "TCS_Annual_Report_FY24.pdf",
            "page_number": 42,
            "similarity_score": 0.89,
            "text_snippet": "Consolidated operating revenue grew 15.2% to Rs. 240,893 Cr...",
        }
    ],
)
```

