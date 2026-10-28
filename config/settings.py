"""Central configuration: branding, model settings, and reference data."""

APP_TITLE = "Multimodal Construction Intelligence Platform"
APP_ICON = "🏗️"
MODEL_NAME = "gemini-2.5-flash"  # override in code if your key lacks access

MAX_IMAGE_DIMENSION = 1600          # px; larger photos are downscaled before upload
MAX_IMAGE_BYTES = 15 * 1024 * 1024  # 15 MB upload ceiling
CHAT_HISTORY_TURNS = 10             # messages sent to the model as context

POLLINATIONS_BASE_URL = "https://image.pollinations.ai/prompt/"

PROJECT_SQFT_MIN = 500
PROJECT_SQFT_MAX = 500_000

# Planning rates are assumptions for conceptual estimates, not quotations.
TIER_RATES = {
    "Tier 1 (Metro)": {"build_inr_per_sqft": 2800, "market_inr_per_sqft": 9500},
    "Tier 2 (Large City)": {"build_inr_per_sqft": 2200, "market_inr_per_sqft": 5800},
    "Tier 3 (Emerging City)": {"build_inr_per_sqft": 1700, "market_inr_per_sqft": 3600},
}

STRUCTURE_CONFIG = {
    "RCC Framed Residential": {"cost_factor": 1.00, "steel_kg_sqft": 4.0},
    "Load-Bearing Masonry": {"cost_factor": 0.85, "steel_kg_sqft": 1.5},
    "Steel Structure Commercial": {"cost_factor": 1.25, "steel_kg_sqft": 6.0},
    "Independent Villa": {"cost_factor": 1.30, "steel_kg_sqft": 4.5},
}

CEMENT_BAGS_PER_SQFT = 0.42  # 50 kg bags, typical RCC residential estimate

MILESTONES = (
    ("Foundation", 25),
    ("Superstructure", 60),
    ("Finishing & MEP", 90),
    ("Handover", 100),
)

SEVERITY_LEVELS = ("Critical", "High", "Medium", "Low")
WEATHER_OPTIONS = ("Normal", "High Wind", "Heavy Rain", "Extreme Heat")

PPE_REQUIRED_KEYS = ("safety_score", "overall_status", "ppe_detection", "hazards")
CRACK_REQUIRED_KEYS = ("defect_type", "estimated_crack_width_mm", "severity_score", "urgency")
