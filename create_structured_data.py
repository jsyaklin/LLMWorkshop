from pydantic import BaseModel, Field

from llama_index.core.settings import Settings
from llama_index.core.llms import ChatMessage
from llama_index.llms.gemini import Gemini
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding

import json
from pathlib import Path
from typing import List, Optional
import os

# Class for structured output
class Professor(BaseModel):
    name: Optional[str] = None
    emails: List[str] = Field(default_factory=list)
    titles: List[str] = Field(default_factory=list)
    courses: List[str] = Field(default_factory=list) # e.g., ["ECE 120", "CS/ECE 374"]
    office: Optional[str] = None
    links: List[str] = Field(default_factory=list) # any URLs found (dept page, scholar, linkedin, etc.)
    source_filename: Optional[str] = None

#----------------------

GOOGLE_API_KEY = ""  # add your GOOGLE API key here
os.environ["GOOGLE_API_KEY"] = "AIzaSyBHoN7nIQswCc1Ie25dmbNyfSf8VKAhNHc"


Settings.llm  = GoogleGenAI(
    model="models/gemini-2.5-flash",
    # api_key="some key",  # uses GOOGLE_API_KEY env var by default
)

#  Make sure to run pip install llama-index-embeddings-gemini

Settings.embed_model = GoogleGenAIEmbedding(
    model="text-embedding-004",
    api_key=GOOGLE_API_KEY
)


def load_professors(path: str | Path = OUT_PATH) -> List[Professor]:
    """Read the single JSON file and return a list[Professor] (Pydantic)."""
    p = Path(path)
    data = json.loads(p.read_text(encoding="utf-8"))
    return [Professor.model_validate(obj) for obj in data]


def extract_professor(text: str) -> Professor:
    """Use Gemini to extract structured data from a professor profile text."""
    return None



# ----------------------
# Settings & constants
# ----------------------
Settings.llm = GoogleGenAI(model="models/gemini-2.5-flash")
DATA_DIR = Path("data")
OUT_DIR = Path("out")
OUT_PATH = OUT_DIR / "professors.json"
LIMIT = 0  # 0 = all, otherwise only first N professors

# ----------------------
# Main: process data/*.txt and write one JSON array
# ----------------------

def main(limit: int = LIMIT) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    txt_files = sorted(DATA_DIR.glob("*.txt"))
    if limit and limit > 0:
        txt_files = txt_files[:limit]

    all_profs: List[dict] = []
    for fp in txt_files:
        raw = fp.read_text(encoding="utf-8", errors="ignore").strip()
        if not raw:
            continue
        prof = extract_professor(raw)
        prof.source_filename = fp.name
        all_profs.append(prof.model_dump())

    OUT_PATH.write_text(json.dumps(all_profs, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(all_profs)} profiles to {OUT_PATH}")

if __name__ == "__main__":
    main(5)
