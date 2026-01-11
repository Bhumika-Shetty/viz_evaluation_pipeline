# generate_llama_dashboards_parity.py
# Prompt-parity dashboard generation for Llama 3.1 via Ollama.
# Creates TWO outputs:
#   1) Bad-context dashboard code
#   2) Good-context dashboard code
#
# Run from repo root:
#   python generate_llama_dashboards_parity.py
#
# Requirements:
#   - Ollama running locally: http://localhost:11434
#   - Model name matches `ollama list` (default below: llama3.1)

import os
import requests

# --- CONFIG ---
MODEL = "llama3.1"  # change if your `ollama list` shows a different name
OUTPUT_DIR = "outputs/llama3.1_local"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- PROMPTS (EXACTLY as you specified) ---

PROMPT_BAD = """
The Titanic dataset contains passenger information from the RMS Titanic disaster of 1912.
This is a sociodemographic dataset with approximately 891 passenger records.
Create a comprehensive dashboard visualization showing multiple different insights about survival patterns in the data.
Provide ONLY the Python code wrapped in triple backticks.
""".strip()

PROMPT_GOOD = """
Prompt :
You are an expert data scientist.

## Dataset Context:
(Use the same Titanic context as before...)

## Your Task: Comprehensive Titanic Dashboard

Create a multi-panel dashboard showing 4-6 different aspects of the Titanic data.

**Specific Requirements:**
- Use subplots to create a dashboard layout (2x3 or 3x2)
- Include: survival by class, by gender, age distribution, fare distribution, family size, embarkation
- Make it publication-ready with consistent styling
- Add a main title: "Titanic Disaster: Comprehensive Survival Analysis"
- Ensure all subplots are properly labeled

**Expected Insights:**
- Comprehensive view of all major factors affecting survival
- Visual story of the disaster
- Multiple patterns visible at once

## Output Format:
Provide ONLY the Python code wrapped in triple backticks.
""".strip()


def extract_code(raw_text: str) -> str:
    """Extract python code from ```python ...``` or ``` ...``` blocks; fallback to raw text."""
    if "```python" in raw_text:
        return raw_text.split("```python", 1)[1].split("```", 1)[0].strip()
    if "```" in raw_text:
        return raw_text.split("```", 1)[1].split("```", 1)[0].strip()
    return raw_text.strip()


def generate_code(prompt: str, filename_base: str) -> str:
    print(f"Generating {filename_base} with model={MODEL} ...")
    resp = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": MODEL, "prompt": prompt, "stream": False},
        timeout=180,
    )
    resp.raise_for_status()
    data = resp.json()
    raw = data.get("response", "")
    code = extract_code(raw)

    out_path = os.path.join(OUTPUT_DIR, f"{filename_base}.py")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(
            "'''\n"
            "Prompt (parity, verbatim):\n"
            f"{prompt}\n"
            "'''\n\n"
        )
        f.write(code)
        f.write("\n")
    print(f"✔ Saved: {out_path}")
    return out_path


if __name__ == "__main__":
    generate_code(PROMPT_BAD, "llama_dashboard_bad_parity")
    generate_code(PROMPT_GOOD, "llama_dashboard_good_parity")
