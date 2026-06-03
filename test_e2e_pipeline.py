"""
End-to-end pipeline test — calls the background generation directly.

Tests 3 grammar point + L1 combinations to stress the pipeline.
Skips the HTTP/auth layer — tests the core generation logic.
"""
import asyncio
import logging
import os
import sys
import time
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("e2e_test")

# ── Path setup ───────────────────────────────────────────────────────────────
ROOT = Path(__file__).parent.resolve()
AGENT = ROOT / "agent"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(AGENT) not in sys.path:
    sys.path.insert(0, str(AGENT))

# Now normal imports work
from agent.slides_tools.slide_plan import compute_slide_plan, build_all_task_briefs
from agent.slides_tools.ModifySlide import ModifySlide
from agent.slides_tools.BuildOfflineBundle import BuildOfflineBundle
from agent.validation_tools.ValidateSlideSet import ValidateSlideSet
from agent.tools.SearchGrammarTool import SearchGrammarTool
from agent.tools.GetL1InterferenceTool import GetL1InterferenceTool
from agent.slides_tools.slide_file_utils import get_project_dir
from agent import jobs as _jobs


def _load_grammar(grammar_point: str) -> dict:
    result = SearchGrammarTool(topic=grammar_point).run()
    return result if isinstance(result, dict) else {}


def _load_l1_data(grammar_point: str, l1_languages: str) -> list[dict]:
    l1_data_list = []
    gram_slug = grammar_point.lower().strip().replace(" ", "_").replace("-", "_")
    for l1 in [l.strip() for l in l1_languages.split(",") if l.strip()]:
        try:
            result = GetL1InterferenceTool(grammar_point=gram_slug, language=l1).run()
            if isinstance(result, dict):
                l1_data_list.append(result)
        except Exception as e:
            logger.warning(f"Failed to load L1 YAML for {l1}: {e}")
    return l1_data_list


BATCH_SIZE = 3


async def _run_slide_batch(
    project_name: str,
    slide_files: list[Path],
    task_briefs: dict[int, str],
    batch_idx: int,
    total_batches: int,
) -> list[tuple[int, int]]:
    """Generate one batch of slides in parallel."""
    tasks = []
    for path in slide_files:
        idx = int(''.join(c for c in path.stem if c.isdigit()))
        brief = task_briefs.get(idx, "")
        tool = ModifySlide(project_name=project_name, slide_name=path.name, task_brief=brief)
        tasks.append(tool.run())  # async call

    await asyncio.gather(*tasks)
    result = []
    for path in slide_files:
        idx = int(''.join(c for c in path.stem if c.isdigit()))
        result.append((idx, path.stat().st_size))
        logger.info(f"  [{batch_idx+1}/{total_batches}] slide_{idx:02d}: {path.stat().st_size:,}B")
    return result


def test_case(
    name: str,
    grammar_point: str,
    l1_languages: str,
    age_group: str,
    formats: list[str],
) -> dict:
    """Run one test case through the full pipeline."""
    print(f"\n{'='*80}")
    print(f"TEST: {name}")
    print(f"  Grammar: {grammar_point} · L1(s): {l1_languages} · Age: {age_group}")
    print(f"{'='*80}\n")

    import hashlib
    slug = f"test_{grammar_point.lower().replace(' ','_')}_{l1_languages.lower().replace(', ','_')[:20]}"
    project_name = f"{slug}_{hashlib.md5(str(time.time()).encode()).hexdigest()[:8]}"
    start_time = time.time()

    # ── Step 1: Load YAML data ─────────────────────────────────────────────
    yaml_start = time.time()
    grammar_data = _load_grammar(grammar_point)
    if not grammar_data:
        logger.error("Failed to load grammar YAML — aborting")
        return {}
    l1_data_list = _load_l1_data(grammar_point, l1_languages)
    logger.info(f"YAML: {time.time()-yaml_start:.2f}s (grammar={'yes'}, L1 files={len(l1_data_list)})")

    # ── Step 2: Compute slide plan ──────────────────────────────────────────
    plan_start = time.time()
    slide_plan = compute_slide_plan(grammar_data, l1_languages, age_group)
    slide_count = len(slide_plan)
    logger.info(f"Plan: {time.time()-plan_start:.2f}s ({slide_count} slides)")

    # ── Step 3: Build task briefs ──────────────────────────────────────────
    brief_start = time.time()
    task_briefs = build_all_task_briefs(slide_plan, grammar_data, l1_data_list, age_group, l1_languages)
    total_chars = sum(len(v) for v in task_briefs.values())
    avg_chars = total_chars // max(len(task_briefs), 1)
    thin_briefs = [k for k, v in task_briefs.items() if len(v) < 200 and k != slide_count]
    logger.info(f"Briefs: {time.time()-brief_start:.2f}s (avg {avg_chars} chars)")
    if thin_briefs:
        logger.warning(f"  ⚠ THIN: {thin_briefs}")
    else:
        logger.info("  ✅ All briefs ≥200 chars")

    for idx, s in enumerate(slide_plan):
        b = task_briefs.get(idx + 1, "")
        bar = "✅" if len(b) >= 200 or s["type"] == "CLOSING_BRAND" else "⚠️"
        print(f"  {bar} slide_{idx+1:02d} ({s['type']:12s}): {len(b):>5}B")

    # ── Step 4: Create blank placeholders ──────────────────────────────────
    presentations_dir = get_project_dir(project_name)
    presentations_dir.mkdir(parents=True, exist_ok=True)
    blank_html = "<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"utf-8\"><title>Slide</title></head><body></body></html>"
    pad_width = max(2, len(str(slide_count)))
    for i in range(1, slide_count + 1):
        (presentations_dir / f"slide_{i:0{pad_width}d}.html").write_text(blank_html, encoding="utf-8")
    logger.info(f"Placeholders: {slide_count} created in {presentations_dir}")

    # ── Step 5: Generate slides in parallel batches ─────────────────────────
    slide_files = sorted(presentations_dir.glob("slide_*.html"))
    gen_start = time.time()
    all_slide_sizes = []

    for i in range(0, len(slide_files), BATCH_SIZE):
        batch = slide_files[i:i + BATCH_SIZE]
        slide_sizes = asyncio.run(_run_slide_batch(project_name, batch, task_briefs, i // BATCH_SIZE,
                                                     (len(slide_files) + BATCH_SIZE - 1) // BATCH_SIZE))
        all_slide_sizes.extend(slide_sizes)

    gen_elapsed = time.time() - gen_start
    small_slides = [s[0] for s in all_slide_sizes if s[1] < 4000 and s[0] != slide_count]
    logger.info(f"Generation: {gen_elapsed:.1f}s total ({gen_elapsed/slide_count:.1f}s/slide)")
    if small_slides:
        logger.warning(f"  ⚠ Small slides (<4KB): {small_slides}")
    else:
        logger.info("  ✅ All slides ≥4KB")

    for idx, size in sorted(all_slide_sizes):
        bar = "✅" if size >= 4000 or idx == slide_count else "⚠️"
        print(f"  {bar} slide_{idx:02d}: {size:>8,}B")

    # ── Step 6: Build offline bundle ────────────────────────────────────────
    bundle_start = time.time()
    try:
        bundle_result = BuildOfflineBundle(project_name=project_name, grammar_point=grammar_point).run()
        bundle_path = presentations_dir / f"{project_name}.html"
        bundle_size = bundle_path.stat().st_size if bundle_path.exists() else 0
        logger.info(f"Bundle: {time.time()-bundle_start:.2f}s ({bundle_size:,}B)")
    except Exception as e:
        logger.error(f"Bundle failed: {e}")
        bundle_size = 0

    # ── Step 7: Validate ────────────────────────────────────────────────────
    val_start = time.time()
    try:
        l1_list = [l.strip() for l in l1_languages.split(",") if l.strip()]
        val_result = ValidateSlideSet(
            project_name=project_name, slide_count=slide_count, l1_languages=l1_list,
        ).run()
        logger.info(f"Validation: {time.time()-val_start:.2f}s")
        # Print first 5 lines
        for line in val_result.split("\n")[:8]:
            print(f"  {line}")
    except Exception as e:
        logger.warning(f"Validation skipped: {e}")

    total_elapsed = time.time() - start_time
    print(f"\n{'─'*60}")
    print(f"SUMMARY: {name}")
    print(f"  Time: {total_elapsed:.0f}s ({total_elapsed/60:.1f} min)")
    print(f"  Slides: {slide_count} · Gen: {gen_elapsed:.0f}s · Bundle: {bundle_size:,}B")
    print(f"  📁 {presentations_dir}")
    print(f"{'─'*60}\n")

    return {
        "name": name,
        "slide_count": slide_count,
        "total_time": total_elapsed,
        "gen_time": gen_elapsed,
        "bundle_size": bundle_size,
        "output_dir": str(presentations_dir),
        "task_brief_avg": avg_chars,
        "thin_briefs": thin_briefs,
        "small_slides": small_slides,
    }


if __name__ == "__main__":
    results = []

    # Test 1: Present Simple, Chinese + Spanish, adults
    r1 = test_case("Present Simple · Chinese+Spanish · Adults",
                   "Present Simple", "Chinese, Spanish", "adults",
                   ["slides", "worksheet"])
    if r1:
        results.append(r1)

    # Test 2: Third Conditional, Japanese, teenagers
    r2 = test_case("Third Conditional · Japanese · Teenagers",
                   "Third Conditional", "Japanese", "teenagers",
                   ["slides", "worksheet", "activity guide"])
    if r2:
        results.append(r2)

    # Test 3: Articles, French + Portuguese, adults (challenging — abstract topic)
    r3 = test_case("Articles · French+Portuguese · Adults",
                   "Articles", "French, Portuguese", "adults",
                   ["slides", "worksheet", "flashcards"])
    if r3:
        results.append(r3)

    # ── Final Report ────────────────────────────────────────────────────────
    print("\n\n" + "=" * 80)
    print("FINAL REPORT")
    print("=" * 80)
    for r in results:
        if not r:
            continue
        issues = r.get("thin_briefs", []) + r.get("small_slides", [])
        status = "✅ PASS" if not issues else "⚠️ ISSUES"
        print(f"\n{status}: {r['name']}")
        print(f"  Slides: {r['slide_count']} | Time: {r['total_time']:.0f}s ({r['total_time']/60:.1f}min)")
        print(f"  Gen: {r['gen_time']:.0f}s | Bundle: {r['bundle_size']:,}B | Avg brief: {r['task_brief_avg']} chars")
        if r.get("thin_briefs"):
            print(f"  ⚠ Thin briefs: {r['thin_briefs']}")
        if r.get("small_slides"):
            print(f"  ⚠ Small slides: {r['small_slides']}")
        print(f"  📁 {r['output_dir']}")
