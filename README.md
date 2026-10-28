<<<<<<< HEAD
# Project1

## Multimodal Construction Intelligence Platform

A Streamlit decision-support application that uses a multimodal model (Google Gemini) to:

- Audit construction site photos for PPE compliance (helmets, high-visibility vests, steel-toe boots, harnesses) and identify hazards, referencing OSHA and IS 456.
- Classify concrete and masonry cracks (Hairline, Settlement, Structural Shear, Thermal Expansion, Spalling) with estimated width, root causes, and repairs.
- Estimate project budget, capex incurred, asset valuation in INR (Lakhs and Crores), and steel and cement requirements.
- Provide weather-aware site protocols and a multi-turn engineering assistant.

The app runs in **demonstration mode** without an API key, so it works out of the box.

## Project layout

```
construction-intelligence/
├── app.py                  # Entry point: layout, tabs, page setup
├── config/
│   ├── settings.py         # Branding, model name, rate tables, limits
│   └── prompts.py          # Prompt templates with pinned JSON contracts
├── core/                   # Pure Python, no Streamlit imports
│   ├── cost_engine.py      # Budget, capex, valuation, materials
│   ├── llm_client.py       # Gemini wrapper with demo fallback
│   ├── parsing.py          # Robust JSON extraction and validation
│   ├── images.py           # Upload validation and resizing
│   ├── render_prompt.py    # Pollinations rendering prompts and URLs
│   ├── weather.py          # Weather protocols
│   ├── demo_data.py        # Demonstration outputs and offline chat
│   └── formatting.py       # INR formatting
├── ui/                     # Streamlit components and tab renderers
├── tests/                  # Unit tests and an end-to-end smoke test
├── .streamlit/             # Theme, server settings, secrets template
├── requirements.txt
└── requirements-dev.txt
```

The `core/` package has no UI dependencies, so business logic can be tested and reused independently of Streamlit.

## Quick start

Requires Python 3.9 or newer.

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
streamlit run app.py
```

Open http://localhost:8501. To enable live AI analysis, paste a Gemini API key into the sidebar, or set `GEMINI_API_KEY` in `.streamlit/secrets.toml` (copy from `secrets.toml.example`).

## Running tests

```bash
pytest
```

The suite covers JSON parsing, cost calculations, INR formatting, image validation, prompt building, the LLM fallback path, and a headless run of the whole app.

## Deploying to Streamlit Community Cloud

1. Push the project to a public or private GitHub repository. `.gitignore` already excludes secrets.
2. At share.streamlit.io, create a new app pointing to `app.py` on your main branch.
3. Under **Advanced settings → Secrets**, add `GEMINI_API_KEY = "..."`. Leave it out to deploy in demonstration mode.

## Design notes

- **Structured output contracts.** Every model prompt specifies the exact JSON shape. Responses are parsed tolerant of markdown fences, checked for required fields, and fall back to demo data with a visible warning if anything fails.
- **Deterministic economics.** Costs and valuations are calculated in code, not by the model, so figures are reproducible and testable.
- **Safe rendering.** All model-generated text is HTML-escaped before display.
- **No database.** Results live in Streamlit session state for the duration of a browser session.

## Assumptions and limitations

- Cost rates, market values, and material factors in `config/settings.py` are planning assumptions. Replace them with current local data before use.
- Asset valuation is a pro-rata estimate and is not a registered-valuer assessment.
- Crack widths and hazard detections are visual estimates from a language model. They must be verified by a qualified engineer or safety officer. The app is decision support, not a substitute for professional inspection.
- Concept renderings from Pollinations AI are illustrative only.
=======
# construction-intelligence-platform
AI-powered construction intelligence platform for PPE safety audits, crack detection, project cost estimation, weather-aware protocols, and engineering assistance using Streamlit and Google Gemini.
>>>>>>> 9cd4a3412d62feaef7518c669a248634a77201a9
