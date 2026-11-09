"""
ALPHANEXUS – Liquid Glass Design Tokens
========================================
Design tokens defining specular highlights, border radiance, blur radius,
and volumetric elevation cards.
"""

GLASS_TOKENS = {
    "card_backdrop_blur": "backdrop-filter: blur(16px) saturate(180%);",
    "card_background_light": "rgba(255, 255, 255, 0.65)",
    "card_background_dark": "rgba(15, 23, 42, 0.70)",
    "card_border_light": "1px solid rgba(255, 255, 255, 0.40)",
    "card_border_dark": "1px solid rgba(255, 255, 255, 0.08)",
    "box_shadow_subtle": "0 8px 32px 0 rgba(0, 0, 0, 0.12)",
    "box_shadow_glow": "0 0 20px rgba(59, 130, 246, 0.25)",
    "border_radius_sm": "8px",
    "border_radius_md": "12px",
    "border_radius_lg": "16px",
    "border_radius_xl": "24px",
    "transition_smooth": "all 0.25s cubic-bezier(0.16, 1, 0.3, 1)",
}
