# CogniESL — Tools Reference

> Complete reference for all tools available to the CogniESL Agent.

---

## 1. Custom Database Search Tools

These tools were built specifically for CogniESL to search the YAML database.

### SearchGrammarTool

**Location**: `agent/tools/SearchGrammarTool.py`
**Purpose**: Search the grammar database by topic name with fuzzy matching.

**Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `topic` | string | Yes | Grammar topic (e.g., "present simple", "passive voice") |

**Matching Strategy** (tried in order):
1. Exact slug match: `present_simple` → `present_simple.yaml`
2. Case-insensitive filename match
3. Title match: compares against `title` field in YAML
4. Fuzzy word overlap: splits into words, finds best intersection
5. Partial title match: substring search

**Returns**: Full grammar data dictionary, or error message with available topics.

**Example output**:
```python
{
  "grammar_point": "present_simple",
  "title": "Present Simple",
  "meaning": {"core_meaning": "...", "ccqs": [...]},
  "form": {"affirmative": {...}, "negative": {...}, "questions": {...}},
  "sub_rules": [...]
}
```

---

### GetL1InterferenceTool

**Location**: `agent/tools/GetL1InterferenceTool.py`
**Purpose**: Get L1 interference patterns for a specific grammar point and language.

**Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `grammar_point` | string | Yes | Grammar point slug (e.g., "present_simple") |
| `language` | string | Yes | L1 language name (e.g., "Portuguese", "Spanish") |

**Matching Strategy**:
1. Language: case-insensitive match against filename (e.g., "portuguese" → `portuguese_interference.yaml`)
2. Grammar point: exact match → case-insensitive → substring match

**Returns**: Interference patterns dictionary with examples, teacher tips, and exercise suggestions. If grammar point not found, returns list of available grammar points for that language.

**Example output**:
```python
{
  "language": "Portuguese",
  "grammar_point": "present_simple",
  "data": {
    "interference_patterns": [...],
    "examples": [...],
    "why_it_happens": "...",
    "teacher_tips": {...}
  }
}
```

---

### SearchActivitiesTool

**Location**: `agent/tools/SearchActivitiesTool.py`
**Purpose**: Search activities by topic, level, age group, or L1 language.

**Parameters**:
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `topic` | string | No | "" | Grammar topic or keyword |
| `level` | string | No | "" | "beginner", "intermediate", "advanced" |
| `age_group` | string | No | "" | "kids", "teens", "adults" |
| `l1_language` | string | No | "" | L1 language to filter by |
| `max_results` | int | No | 5 | Maximum results to return |

**Matching Logic**:
- Topic: searches `name`, `description`, `targetStructures`, `keywords`
- Level: matches against `bestForLevels` (case-insensitive)
- Age: keyword-based detection in `description` and `groupSize`
- L1: checks `l1Enhanced` flag and `keywords`

**Returns**: Single activity dict (if 1 result) or `{count, activities}` dict. Error message if none found.

---

## 2. Slides Tools

These tools generate and manipulate PowerPoint presentations. All are in `agent/slides_tools/`.

### InsertNewSlides
Creates new slide placeholders in a presentation project.

### ModifySlide
Modifies content of an existing slide. Used to set titles, body text, images, etc.

### BuildPptxFromHtmlSlides
**Core tool for PPTX generation.** Converts HTML slide files into a final PPTX presentation.
- Takes a list of HTML file paths
- Applies theme/styling
- Outputs a single `.pptx` file

### ManageTheme
Manages presentation themes (colors, fonts, layouts). Uses CSS-based theme definitions.

### CheckSlide
Validates slide content for common issues (overflow, formatting errors).

### CheckSlideCanvasOverflow
Specifically checks if content overflows the slide canvas boundaries.

### SlideScreenshot
Renders a slide to an image (PNG) for preview/validation.

### ReadSlide
Reads the content of an existing slide.

### DeleteSlide
Removes a slide from the presentation.

### RestoreSnapshot
Restores the presentation to a previously saved snapshot state.

### CreatePptxThumbnailGrid
Creates a thumbnail overview image of all slides in a presentation.

### GenerateImage
Generates images using AI models (Gemini). Supports two modes:
- Complex diagrams (flowcharts, pyramids)
- Concept art (illustrations, atmosphere)

### ImageSearch
Searches the web for images.

### DownloadImage
Downloads an image from a URL to local storage.

### EnsureRasterImage
Converts images to raster format (PNG/JPG) for compatibility.

### ApplyPptxTextReplacements
Performs bulk text replacements across a PPTX file.

### ExtractPptxTextInventory
Extracts all text content from a PPTX file for review.

### CreateImageMontage
Creates a montage/collage from multiple images.

### RearrangePptxSlidesFromTemplate
Rearranges slides based on a template presentation.

### Utility Files (not tools, but used by tools)
- `slide_file_utils.py` — Path resolution for slide output directories
- `deck_utils.py` — Theme loading and test deck utilities
- `html_writer_instructions.md` — HTML slide authoring guidelines
- `html2pptx_runner.js` — Node.js HTML-to-PPTX converter
- `render_slides.py` — Python slide rendering script
- `slide_html_utils.py` — HTML manipulation utilities
- `template_registry.py` — Slide template definitions

---

## 3. Docs Tools

These tools generate and manipulate Word documents and PDFs. All are in `agent/docs_tools/`.

### CreateDocument
**Core tool for DOCX generation.** Creates a Word document from HTML content.
- Takes HTML content or file path
- Applies styling and formatting
- Outputs a `.docx` file

### ConvertDocument
Converts documents between formats. Primary use: DOCX → PDF.
- Uses Playwright for PDF rendering
- Requires Chromium (installed via `playwright install chromium`)

### ModifyDocument
Modifies content of an existing DOCX document.

### ViewDocument
Reads and returns the content of a DOCX document.

### ListDocuments
Lists all generated documents in a directory.

### RestoreDocument
Restores a document to a previously saved state.

### Utils (`agent/docs_tools/utils/`)
The HTML-to-DOCX conversion engine (12 Python files):
- `doc_file_utils.py` — Path resolution for document output
- `html_docx_core.py` — Main conversion orchestrator
- `html_docx_blocks.py` — Block-level element handling
- `html_docx_css.py` — CSS parsing and application
- `html_docx_images.py` — Image handling in documents
- `html_docx_page.py` — Page layout and margins
- `html_docx_paragraphs.py` — Paragraph formatting
- `html_docx_playwright.py` — Playwright-based rendering
- `html_docx_selectors.py` — CSS selector handling
- `html_docx_shared.py` — Shared utilities
- `html_docx_tables.py` — Table conversion
- `html_docx_constants.py` — Constants and defaults
- `html_validation.py` — HTML validation

---

## 4. Shared Tools

Cross-cutting utilities in `agent/shared_tools/`.

### CopyFile
Copies files between paths. Includes path normalization for cross-platform compatibility (handles `/mnt/...` paths on Windows).

### ExecuteTool
Generic tool execution wrapper.

### FindTools
Tool discovery utility.

### ManageConnections
Connection management for external services.

### SearchTools
Tool search utility.

### model_availability.py
Checks which AI model providers/features are available based on API keys.

### openai_client_utils.py
Helpers for OpenAI client configuration and credentials.

---

## 5. Utility Tools

File system operations in `agent/utility_tools/`.

### ReadFile
Reads file contents. Supports text files, images (multimodal), and base64.

### WriteFile
Writes content to files.

### EditFile
Performs targeted edits on files (find-and-replace).

### ListDirectory
Lists directory contents.

---

## 6. Built-in Agency Swarm Tools

These come from the Agency Swarm framework and are available to the agent.

### IPythonInterpreter
Runs Python code in a Jupyter kernel. Used for data analysis, calculations, and complex file operations.

### WebSearchTool
Searches the web. Configured with `search_context_size="high"` for comprehensive results.

---

## 7. Tool Usage Patterns

### Generating Slides (Typical Flow)
```
1. InsertNewSlides — Create slide placeholders
2. ModifySlide — Populate each slide with content
3. ManageTheme — Apply visual theme
4. CheckSlide — Validate content
5. BuildPptxFromHtmlSlides — Generate final PPTX
6. SlideScreenshot — (Optional) Generate preview
```

### Generating Worksheets (Typical Flow)
```
1. CreateDocument — Create DOCX from HTML content
2. ConvertDocument — Convert DOCX to PDF
3. ViewDocument — (Optional) Verify output
```

### Searching the Database (Typical Flow)
```
1. SearchGrammarTool — Find grammar point data
2. GetL1InterferenceTool — Get L1 patterns (if L1 specified)
3. SearchActivitiesTool — Find matching activities
```
