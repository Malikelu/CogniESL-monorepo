"""
theme_generator.py — Generates a unique visual "Theme DNA" per lesson.

Each CogniESL generation gets a fresh, cohesive theme: color palette, font pairing,
background style, and decorative direction — all determined by the grammar point's
"mood" category.  No LLM calls: Python color theory + controlled randomness produces
a unique palette every time (96+ combinations) while keeping every slide in the
same generation visually consistent via CSS custom properties written to ``_theme.css``.

Integration:
  QueueGenerationJob calls ``generate_and_write_theme()`` BEFORE any slide generation
  begins.  Each ModifySlide call then receives the populated ``_theme.css`` and the
  html_writer_instructions.md tells the LLM to use those CSS variables — not its own raw
  colors — for every slide.
"""

import colorsys
import logging
import random
from pathlib import Path

logger = logging.getLogger(__name__)

# ── Mood Categories ──────────────────────────────────────────────────────────
# Each mood maps grammar keywords → a colour-wheel region + visual style.

_GRAMMAR_MOOD_MAP: list[tuple[list[str], str]] = [
    # Timeless — facts, routines, schedules, existence
    (["present simple", "live commentary", "narrative present", "historic present",
      "timeless", "general truth", "when", "while", "before", "after", "until",
      "since", "still", "yet", "already", "every", "each", "none", "all",
      "existence", "there is", "there are", "existential"], "timeless"),
    # Nostalgic — past events, memory, habit, biography
    (["past", "was", "were", "used to", "would (past)", "biography",
      "narrative review", "narrative tense", "ed clause", "past participle clause",
      "past ability"], "nostalgic"),
    # Forward — future plans, prediction, intention
    (["future", "going to", "will", "shall", "about to", "due to",
      "prediction", "plan", "intention", "arrangement",
      "first conditional"], "forward"),
    # Flowing — ongoing action, progress, process
    (["continuous", "progressive", "ongoing", "process", "action in progress",
      "stative", "mental state", "coordination", "conjunction", "connector",
      "-ing clause", "participle clause"], "flowing"),
    # Polished — completion, perfection, detail, refinement
    (["perfect", "have", "has", "had", "gerund", "infinitive", "-ing", "to",
      "possessive", "own", "self", "reflexive", "causative",
      "affix", "prefix", "suffix", "word formation", "compound",
      "collocation", "phrasal"], "polished"),
    # Dreamy — hypotheticals, conditions, possibility
    (["conditional", "would", "if", "unless", "provided", "supposing",
      "even if", "alternatives to if", "subjunctive", "wish",
      "hypothetical", "unreal", "improbable", "formal conditional",
      "were he", "should you", "had i", "inversion condition",
      "despite", "although", "though", "even though", "concession"], "dreamy"),
    # Empowering — ability, permission, capability, commands
    (["can", "could", "able", "ability", "permission", "imperative",
      "command", "instruction", "deduction", "must can",
      "non-canonical"], "empowering"),
    # Advisory — advice, recommendation, obligation, prohibition
    (["should", "ought", "must", "have to", "need to", "had better",
      "supposed to", "advice", "recommend", "obligation", "prohibition",
      "mustn", "mandative"], "advisory"),
    # Speculative — probability, possibility, uncertainty
    (["might", "may", "maybe", "perhaps", "probably", "possibly",
      "speculate", "uncertain", "concession may"], "speculative"),
    # Clean — articles, determiners, quantity, precision
    (["article", "a/an", "the", "countable", "uncountable", "some", "any",
      "determiner", "demonstrative", "this", "that", "these", "those",
      "possessive pronoun", "quantity", "number", "much", "many",
      "few/little", "both", "either", "neither", "another", "other",
      "adjective without noun", "attributive", "predicative",
      "capitalization", "punctuation", "contraction", "negation",
      "negative", "no/none"], "clean"),
    # Spatial — location, direction, position, relationships
    (["preposition", "in/on/at", "place", "position", "location",
      "direction", "movement", "spatial", "dependent preposition",
      "adverb position", "adverb placement", "extraposition",
      "postposing", "fronting", "inversion adverb"], "spatial"),
    # Dynamic — comparisons, choices, alternatives
    (["comparative", "superlative", "as as", "than", "like", "as if",
      "similar", "different", "alternative", "choice", "preference",
      "adjective order"], "dynamic"),
    # Rhythmic — frequency, manner, style, degree
    (["adverb", "frequency", "always", "never", "sometimes", "rarely",
      "seldom", "hardly", "manner", "degree", "very", "quite", "too",
      "enough", "extremely", "however adverb", "negative adverb",
      "time adverb"], "rhythmic"),
    # Curious — questions, inquiry, emphasis, exclamation
    (["question", "interrogative", "wh-", "how", "cleft", "pseudo-cleft",
      "embedded question", "indirect question", "negative question",
      "exclamation", "tag question", "echo question", "emphasis",
      "emphatic"], "curious"),
    # Structured — passive, systematic, rules, formal
    (["passive", "by", "reporting verb", "reported passive",
      "two objects", "bare infinitive", "infinitive", "verb pattern",
      "clause", "relative", "defining", "non-defining",
      "complex noun", "complex report"], "structured"),
    # Narrative — storytelling, reported speech, discourse
    (["reported", "indirect speech", "say", "tell", "narrative",
      "discourse", "cohesion", "comment clause", "story",
      "reporting verb say tell"], "narrative"),
]


def _get_mood(grammar_point: str) -> str:
    """Map a grammar point to its mood category.

    First tries keyword matching against the full grammar name.
    Falls back to a smart analysis of the grammar topic's distinctive final word.
    """
    gp = grammar_point.lower().strip()
    for keywords, mood in _GRAMMAR_MOOD_MAP:
        for kw in keywords:
            if kw in gp:
                return mood

    # Smart fallback: analyze the most distinctive word in the name
    # Split into words, remove common filler words, check the final meaningful word
    words = [w for w in gp.replace("(", "").replace(")", "").split()
             if w not in ("a", "an", "the", "and", "or", "of", "for", "in", "to", "with", "without")]
    if words:
        last = words[-1]
        # Word-ending cues
        if last.endswith("ing"):
            return "flowing"
        if last.endswith("ed") or last.endswith("ion"):
            return "polished"
        if last.endswith("ly"):
            return "rhythmic"
        if last.endswith("al") or last.endswith("ar") or last.endswith("ic"):
            return "clean"
        if last.endswith("ous") or last.endswith("ive"):
            return "dynamic"
        if last.endswith("s"):
            return "timeless"
        # Word-meaning cues
        word_moods = {
            "nouns": "clean", "verbs": "polished", "clauses": "structured",
            "phrases": "polished", "forms": "clean", "structures": "structured",
            "patterns": "structured", "rules": "advisory",
            "uses": "timeless", "use": "timeless", "meaning": "timeless",
            "difference": "dynamic", "comparison": "dynamic",
            "problems": "advisory", "errors": "advisory", "mistakes": "advisory",
            "review": "nostalgic", "overview": "timeless",
            "advanced": "polished", "basic": "clean",
        }
        if last in word_moods:
            return word_moods[last]

    return "balanced"


# When no mood matches, balanced picks semi-randomly for variety
_BALANCED_MOODS = ["timeless", "clean", "polished", "dreamy", "spatial", "dynamic"]


def _resolve_mood(grammar_point: str) -> str:
    """Resolve a mood, with balanced choosing semi-randomly for variety."""
    mood = _get_mood(grammar_point)
    if mood == "balanced":
        # Deterministic-ish: seed from grammar point name hash so same topic
        # always gets the same fallback mood (caching-friendly), but different
        # topics get different moods.
        idx = abs(hash(grammar_point)) % len(_BALANCED_MOODS)
        mood = _BALANCED_MOODS[idx]
    return mood


# ── Mood Definitions ─────────────────────────────────────────────────────────
# Each mood defines:
#   base_hue_range    (min, max)      — hue wheel range for the primary colour
#   saturation_range  (min, max)      — how vivid the colours are
#   lightness_range   (min, max)      — base lightness (for primary)
#   is_dark           bool            — whether the background is dark or light
#   accent_offset     int             — hue offset for the accent colour (complementary ≈ 180)

_MoodDef = dict[str, int | bool | tuple[int, int]]

MOODS: dict[str, _MoodDef] = {
    "timeless":  {"base_hue": (195, 225), "sat": (55, 80), "lit": (35, 50), "dark": True,  "accent_offset": 170, },
    "nostalgic": {"base_hue": (25,  45),  "sat": (40, 65), "lit": (45, 60), "dark": False, "accent_offset": 150, },
    "forward":   {"base_hue": (200, 220), "sat": (40, 60), "lit": (35, 50), "dark": True,  "accent_offset": 140, },
    "flowing":   {"base_hue": (155, 185), "sat": (45, 70), "lit": (35, 50), "dark": True,  "accent_offset": 190, },
    "polished":  {"base_hue": (260, 290), "sat": (50, 75), "lit": (35, 50), "dark": True,  "accent_offset": 160, },
    "dreamy":    {"base_hue": (260, 310), "sat": (55, 80), "lit": (30, 45), "dark": True,  "accent_offset": 150, },
    "speculative":{"base_hue": (230, 255), "sat": (50, 70), "lit": (30, 45),"dark": True,  "accent_offset": 160, },
    "empowering":{"base_hue": (15,  40),  "sat": (65, 85), "lit": (40, 55), "dark": True,  "accent_offset": 195, },
    "advisory":  {"base_hue": (110, 145), "sat": (45, 70), "lit": (35, 50), "dark": True,  "accent_offset": 170, },
    "clean":     {"base_hue": (195, 215), "sat": (30, 50), "lit": (55, 70), "dark": False, "accent_offset": 180, },
    "spatial":   {"base_hue": (80,  130), "sat": (40, 60), "lit": (40, 55), "dark": True,  "accent_offset": 160, },
    "dynamic":   {"base_hue": (330, 20),  "sat": (60, 85), "lit": (40, 55), "dark": True,  "accent_offset": 150, },
    "rhythmic":  {"base_hue": (30,  50),  "sat": (55, 75), "lit": (35, 50), "dark": True,  "accent_offset": 140, },
    "curious":   {"base_hue": (45,  75),  "sat": (60, 85), "lit": (45, 60), "dark": False, "accent_offset": 180, },
    "structured":{"base_hue": (210, 230), "sat": (35, 55), "lit": (35, 50), "dark": True,  "accent_offset": 170, },
    "narrative": {"base_hue": (15,  35),  "sat": (40, 60), "lit": (40, 55), "dark": False, "accent_offset": 200, },
    "balanced":  {"base_hue": (210, 230), "sat": (35, 55), "lit": (40, 55), "dark": True,  "accent_offset": 170, },
}

# Pre-approved font pairings — rotate randomly each generation.
_FONT_PAIRS: list[tuple[str, str]] = [
    ("Space Grotesk", "Inter"),
    ("Inter", "Merriweather"),
    ("Urbanist", "Lora"),
    ("Clash Display", "Inter"),
    ("Poppins", "Lora"),
    ("Montserrat", "Merriweather"),
    ("Playfair Display", "Inter"),
    ("Space Grotesk", "Lora"),
]

_BG_PATTERNS: list[str] = [
    "solid",
    "subtle-gradient",
    "radial-glow",
    "split-diagonal",
    "mesh-gradient",
]

# ── HSL utilities ────────────────────────────────────────────────────────────

def _rand_in_range(r: tuple[int, int] | list[int]) -> int:
    return random.randint(r[0], r[1])


def _rand_hue(r: tuple[int, int]) -> int:
    """Pick a random hue, handling wrap-around ranges (e.g. 330→20 crosses 0°)."""
    lo, hi = r
    if lo <= hi:
        return random.randint(lo, hi)
    # Wrap-around: pick from [lo, 360) or [0, hi]
    return random.choice([random.randint(lo, 359), random.randint(0, hi)])


def _hsl(h: int, s: int, l: int) -> str:
    return f"hsl({h},{s}%,{l}%)"


def _adjust_lightness(h: int, s: int, l: int, delta: int) -> tuple[int, int, int]:
    return (h, s, max(0, min(100, l + delta)))


# ── Public API ───────────────────────────────────────────────────────────────

def generate_theme(grammar_point: str, age_group: str) -> dict:
    """Produce a complete theme dict from Python colour theory — no LLM call.

    Returns a dict ready to pass to ``write_theme_css()``.
    """
    mood = _resolve_mood(grammar_point)
    m = MOODS.get(mood, MOODS["balanced"])

    # ── Pick base hue, saturation, lightness ──
    base_h = _rand_hue(m["base_hue"])  # type: ignore[arg-type]
    base_s = _rand_in_range(m["sat"])        # type: ignore[arg-type]
    base_l = _rand_in_range(m["lit"])         # type: ignore[arg-type]

    is_dark = m["dark"]
    accent_offset: int = m["accent_offset"]  # type: ignore[assignment]

    # Complementary / split-complementary accent
    accent_h = (base_h + accent_offset) % 360
    # Secondary: analogous (shifted ~30°)
    secondary_h = (base_h + 35 + 15 * random.choice([-1, 1])) % 360

    # ── Adjust lightness for light vs dark themes ──
    if is_dark:
        bg_l = 8
        card_l = 14
        text_l = 90
        muted_l = 65
    else:
        bg_l = 96
        card_l = 100
        text_l = 15
        muted_l = 45

    theme = {
        "mood": mood,
        "is_dark": is_dark,
        # Primary palette
        "primary": _hsl(base_h, base_s, base_l),
        "primary_light": _hsl(base_h, base_s, min(100, base_l + 18)),
        "primary_dark": _hsl(base_h, base_s, max(0, base_l - 14)),
        # Secondary
        "secondary": _hsl(secondary_h, base_s - 10, base_l + 10),
        # Accent
        "accent": _hsl(accent_h, min(100, base_s + 5), min(100, base_l + 5)),
        # Backgrounds
        "bg": _hsl(base_h, 15, bg_l),
        "bg_card": _hsl(base_h, 12, card_l),
        # Text
        "text_primary": _hsl(0, 0, text_l),
        "text_secondary": _hsl(0, 0, muted_l),
        # Typography
        "font_heading": random.choice(_FONT_PAIRS)[0],
        "font_body": random.choice(_FONT_PAIRS)[1],
        # Decor
        "bg_pattern": random.choice(_BG_PATTERNS),
        # Misc
        "border_radius": random.choice(["8px", "12px", "14px", "16px"]),
        "shadow": "0 8px 32px rgba(0,0,0,0.3)" if is_dark else "0 6px 24px rgba(0,0,0,0.08)",
    }
    return theme


def theme_to_css(theme: dict) -> str:
    """Convert a theme dict to a ``_theme.css`` string."""
    # Determine if we need to wrap in @media/prefers-color-scheme for light/dark.
    # ESL slides use fixed themes per generation, not system preference.
    lines = [
        "/*",
        " * CogniESL Theme DNA — auto-generated.  DO NOT EDIT.",
        f" * Mood: {theme['mood']}  |  Theme: {'dark' if theme['is_dark'] else 'light'}",
        " */",
        "",
        ":root {",
    ]

    css_vars = {
        "--primary": theme["primary"],
        "--primary-light": theme["primary_light"],
        "--primary-dark": theme["primary_dark"],
        "--secondary": theme["secondary"],
        "--accent": theme["accent"],
        "--bg": theme["bg"],
        "--bg-card": theme["bg_card"],
        "--text-primary": theme["text_primary"],
        "--text-secondary": theme["text_secondary"],
        "--font-heading": f"'{theme['font_heading']}', system-ui, sans-serif",
        "--font-body": f"'{theme['font_body']}', system-ui, sans-serif",
        "--border-radius": theme["border_radius"],
        "--shadow": theme["shadow"],
    }

    for var, val in css_vars.items():
        lines.append(f"    {var}: {val};")

    lines.append("}")
    lines.append("")

    # Add helper classes for common use
    lines.extend([
        "/* Helper classes */",
        ".slide {",
        "    position: relative;",
        f"    background: var(--bg);",
        f"    color: var(--text-primary);",
        f"    font-family: var(--font-body);",
        "}",
        "",
        ".bg-card {",
        f"    background: var(--bg-card);",
        f"    border-radius: var(--border-radius);",
        f"    box-shadow: var(--shadow);",
        "}",
        "",
        ".text-primary { color: var(--text-primary); }",
        ".text-secondary { color: var(--text-secondary); }",
        "",
        "h1, h2, h3, h4, h5, h6 {",
        f"    font-family: var(--font-heading);",
        "}",
    ])

    return "\n".join(lines)


def write_theme_css(project_dir: Path, theme: dict) -> Path:
    """Write ``_theme.css`` to the project directory."""
    css_content = theme_to_css(theme)
    theme_path = project_dir / "_theme.css"
    theme_path.write_text(css_content, encoding="utf-8")
    logger.info(f"Theme written to {theme_path} ({mood_label(theme)})")
    return theme_path


def mood_label(theme: dict) -> str:
    """Human-readable label for logging."""
    mood = theme.get("mood", "?")
    direction = "dark" if theme.get("is_dark") else "light"
    heading = theme.get("font_heading", "?")
    return f"{mood}/{direction} + {heading}"
