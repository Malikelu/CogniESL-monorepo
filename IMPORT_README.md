# CogniESL Database Import Guide

## Overview

This guide helps you import curated grammar and L1 interference YAML files into the SQLite database (`cogniesl.db`). Currently, content is loaded from static YAML files — this import enables:

- Faster querying
- Version control for content updates  
- Future: API endpoints for content discovery
- Future: Admin UI for content management

## Files Created

1. **`agent/db_schema.py`** — Creates database tables for grammar and L1 data
2. **`agent/import_content.py`** — Imports YAML files into the database
3. **`agent/content_queries.py`** — Query functions to read imported data
4. **`IMPORT_README.md`** — This file

## Quick Start

### 1. Initialize Database Schema

```bash
cd /path/to/CogniESL
python -c "from agent.db_schema import init_content_db; init_content_db()"
```

This creates tables in `cogniesl.db` if they don't already exist.

### 2. Import YAML Files

```bash
python -m agent.import_content
```

This reads all YAML files from:
- `/data/grammar/*.yaml` (302 files)
- `/data/l1-interference/*.yaml` (36 files)

And populates the database tables.

### 3. Verify Import

```bash
python -c "from agent.content_queries import import_status; import(import_status())"
```

Expected output:
```
{
  'grammar_points': 302,
  'l1_languages': 36,
  'grammar_errors': ~500,
  'l1_patterns': ~1500
}
```

## Database Schema

### Tables

**`grammar_points`**
- `id` (UUID) — primary key
- `title` (TEXT) — grammar point name (e.g., "Present Simple")
- `level` (TEXT) — CEFR level (A1, A2, B1, etc.)
- `description` (TEXT) — short description
- `core_meaning` (TEXT) — pedagogical meaning
- `raw_yaml` (TEXT) — full YAML content (for reference)
- `imported_at` (TEXT) — ISO timestamp
- `version` (INTEGER) — for tracking updates

**`grammar_errors`**
- `id` (UUID) — primary key
- `grammar_id` (FK) — references grammar_points
- `error` (TEXT) — incorrect example
- `correction` (TEXT) — correct example
- `explanation` (TEXT) — why it's wrong
- `l1_groups` (TEXT) — comma-separated L1s that make this error
- `reliability` (TEXT) — source reliability rating

**`l1_interference`**
- `id` (UUID) — primary key
- `language` (TEXT) — language name (e.g., "Spanish")
- `l1_code` (TEXT) — ISO 639-1 code (e.g., "es")
- `total_grammar_points` (INTEGER) — count of grammar points in file
- `raw_yaml` (TEXT) — full YAML content
- `imported_at` (TEXT) — ISO timestamp
- `version` (INTEGER) — for tracking updates

**`l1_patterns`**
- `id` (UUID) — primary key
- `l1_id` (FK) — references l1_interference
- `grammar_point` (TEXT) — which grammar point (e.g., "present_simple")
- `pattern` (TEXT) — the interference pattern description
- `frequency` (INTEGER) — 1-5 rating
- `persistence` (INTEGER) — 1-5 rating
- `communicative_impact` (INTEGER) — 1-5 rating
- `example_wrong` (TEXT) — incorrect example
- `example_correct` (TEXT) — correct example
- `explanation` (TEXT) — linguistic reason

## Query Examples

### Get a grammar point

```python
from agent.content_queries import get_grammar_by_title

grammar = get_grammar_by_title("Present Simple")
print(grammar['core_meaning'])
```

### Get all errors for a grammar point

```python
from agent.content_queries import get_grammar_errors_for_point

errors = get_grammar_errors_for_point(grammar['id'])
for error in errors:
    print(f"{error['error']} → {error['correction']}")
```

### Get L1 interference patterns

```python
from agent.content_queries import get_l1_patterns_for_grammar

patterns = get_l1_patterns_for_grammar(l1_id, "present_simple")
for pattern in patterns:
    print(f"Pattern: {pattern['pattern']}")
    print(f"Frequency: {pattern['frequency']}/5")
```

### List all imported content

```python
from agent.content_queries import get_all_grammar_titles, get_all_l1_languages

grammars = get_all_grammar_titles()
languages = get_all_l1_languages()

print(f"Grammar points: {len(grammars)}")
print(f"L1 languages: {len(languages)}")
```

## Production Deployment

On Railway:

1. **Set environment variable**: `COGNIESL_STATIC_DIR=/app/static-data`
   - This points to your static data directory (outside the Volume mount)
   
2. **Run import on startup** (in your deployment script):
   ```bash
   python -m agent.import_content
   ```

3. **The database is persisted** at `/app/data/cogniesl.db` (on Railway's Volume)

## Next Steps

- [ ] Update `SearchGrammarTool` to query database instead of reading files
- [ ] Update `SearchL1Tool` (when created) to query database
- [ ] Add API endpoints for content queries (`/api/grammar/{id}`, etc.)
- [ ] Add admin UI for content versioning and updates

## Troubleshooting

**Issue**: "Database is locked"
- Solution: Ensure only one process is writing at a time. Close other connections.

**Issue**: "No such table"
- Solution: Run `init_content_db()` first to create the schema.

**Issue**: "KeyError: 'grammar_points'"
- Solution: Make sure the YAML files are valid. Check `raw_yaml` column for actual content.

## Files Status (May 30, 2026)

✓ `spanish_interference.yaml` — Ready for import
✓ `present_simple.yaml` — Ready for import
✓ 300 other grammar files — Ready for import
✓ 35 other L1 interference files — Ready for import

After running `python -m agent.import_content`, all content will be available via database queries.
