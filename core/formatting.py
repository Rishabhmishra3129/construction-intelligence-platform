"""Display formatting helpers."""


def fmt_inr(amount: float) -> str:
    """Format rupees using Indian units: Crore (10^7) and Lakh (10^5)."""
    if amount >= 1e7:
        return f"₹{amount / 1e7:,.2f} Cr"
    if amount >= 1e5:
        return f"₹{amount / 1e5:,.2f} L"
    return f"₹{amount:,.0f}"
