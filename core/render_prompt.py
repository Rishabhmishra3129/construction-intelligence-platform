"""Builds prompts and URLs for conceptual 3D renderings via Pollinations AI."""

from urllib.parse import quote

from config.settings import POLLINATIONS_BASE_URL


def build_render_prompt(structure: str, built_up_sqft: float, tier: str) -> str:
    city_class = tier.split(" (")[0]
    return (
        f"conceptual 3D architectural rendering of a {structure.lower()} building, "
        f"{built_up_sqft:,.0f} square feet, {city_class} Indian city context, "
        "daylight, photorealistic, clean facade"
    )


def build_render_url(prompt: str, width: int = 1024, height: int = 640) -> str:
    return f"{POLLINATIONS_BASE_URL}{quote(prompt)}?width={width}&height={height}&nologo=true"
