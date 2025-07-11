from django import template

register = template.Library()

@register.filter
def inr_format(value):
    """
    Converts a numeric value into human-readable Indian currency format:
    - 45,000 → 45K
    - 4,50,000 → 4.5 Lakhs
    - 1,20,00,000 → 1.2 Cr
    """

    try:
        value = float(value)
    except (ValueError, TypeError):
        return "N/A"

    if value >= 10_000_000:  # 1 crore
        return f"{value / 10_000_000:.1f} Cr"
    elif value >= 100_000:  # 1 lakh
        return f"{value / 100_000:.1f} Lakhs"
    elif value >= 1_000:  # 1 thousand
        return f"{value / 1_000:.0f}K"
    else:
        return f"{int(value):,}"  # e.g., 999 → 999

