# ALPHANEXUS – Deterministic Financial Analytics Engine

## 1. Zero-Hallucination Design

Financial analysis cannot tolerate LLM arithmetic errors. All metrics, growth rates, margins, and ratios are calculated using **pure, deterministic Python mathematics** before being presented to analysts or passed to the LLM for qualitative commentary.

---

## 2. Calculated Ratios

1. **Profitability:**
   - **Return on Equity (ROE):** $\text{Net Income} / \text{Shareholders' Equity} \times 100$
   - **Return on Capital Employed (ROCE):** $\text{EBIT} / (\text{Total Assets} - \text{Current Liabilities}) \times 100$
   - **EBITDA Margin:** $\text{EBITDA} / \text{Total Revenue} \times 100$
   - **Net Profit Margin:** $\text{Net Profit} / \text{Total Revenue} \times 100$

2. **Cash Flow & Capital Structure:**
   - **Free Cash Flow (FCF):** $\text{Operating Cash Flow} - \text{Capital Expenditures}$
   - **Debt-to-Equity:** $\text{Total Debt} / \text{Total Equity}$
   - **Interest Coverage:** $\text{EBIT} / \text{Interest Expense}$

3. **DuPont Breakdown (3-Way):**
   $$\text{ROE} = \text{Net Profit Margin} \times \text{Asset Turnover} \times \text{Financial Leverage}$$
