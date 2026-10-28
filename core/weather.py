"""Weather-conditioned site protocols shown on the daily assistant tab."""

from typing import Dict, List, NamedTuple


class Alert(NamedTuple):
    level: str  # "danger" or "info"
    message: str


WEATHER_PROTOCOLS: Dict[str, List[Alert]] = {
    "High Wind": [
        Alert("danger", "Suspend crane and hoist operations when sustained wind exceeds the manufacturer's limit (commonly 40 km/h)."),
        Alert("danger", "Secure loose formwork, shuttering sheets, scaffold planks, and lightweight material stockpiles."),
        Alert("info", "Inspect temporary bracing and tarpaulin anchors before resuming work."),
    ],
    "Heavy Rain": [
        Alert("danger", "Stop all live electrical work. De-energise temporary site distribution boards and keep them dry."),
        Alert("danger", "Halt pouring of fresh concrete. Cover exposed slabs and cured surfaces with polythene sheets."),
        Alert("info", "Divert surface runoff away from excavations and check trench shoring for soil saturation."),
    ],
    "Extreme Heat": [
        Alert("danger", "Begin curing immediately after finishing. Keep surfaces continuously moist for at least 7 days (14 days for blended cement, per IS 456)."),
        Alert("danger", "Schedule heavy labour between 06:00 and 11:00. Mandate shaded rest breaks and hydration every 30 minutes."),
        Alert("info", "Pour concrete in the cooler part of the day to limit plastic shrinkage and cold joints."),
    ],
    "Normal": [
        Alert("info", "Standard operations. Complete the daily PPE check and toolbox talk before work begins."),
        Alert("info", "Maintain curing schedules and routine scaffold inspections."),
    ],
}
