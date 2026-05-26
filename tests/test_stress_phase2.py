#!/usr/bin/env python3
"""Phase 2 Stress Testing: Edge cases, multiple L1s, difficult personas."""

import sys
from pathlib import Path

# Add agent directory to path
sys.path.insert(0, str(Path(__file__).parent / "agent"))


class StressTestScenarios:
    """Comprehensive stress test scenarios for CogniESL."""

    SCENARIOS = [
        {
            "name": "Multiple L1s",
            "description": "Students with Chinese and Spanish native languages",
            "request": """
I teach a mixed group of ESL students:
- Some are native Spanish speakers
- Some are native Chinese speakers
- They're teenagers, intermediate level
I need slides and a worksheet for teaching past simple.
""",
            "expected_checks": [
                "Gathers Chinese and Spanish as L1s",
                "Retrieves L1 interference data for BOTH languages",
                "Generates L1 Oracle sections for Spanish errors",
                "Generates L1 Oracle sections for Chinese errors",
                "Validation passes for both L1s",
            ],
        },
        {
            "name": "Invalid Grammar Topic",
            "description": "Student requests non-existent grammar topic",
            "request": """
I need materials for teaching "zeptogram" to adult learners.
They're Portuguese speakers at beginner level.
Give me slides and a worksheet.
""",
            "expected_checks": [
                "Agent detects grammar topic not found",
                "Suggests similar topics available",
                "Asks teacher to clarify or choose from suggestions",
                "Does NOT proceed with generation",
            ],
        },
        {
            "name": "Invalid L1 Language",
            "description": "Requests materials for unsupported L1",
            "request": """
I'm teaching Klingon speakers English.
Topic: present continuous
Adults, intermediate level.
I need slides, worksheet, and activities.
""",
            "expected_checks": [
                "Agent detects L1 language not supported",
                "Lists available L1 languages",
                "Offers to generate without L1-specific targeting",
                "Or asks teacher to pick supported language",
            ],
        },
        {
            "name": "Incomplete Requirements - Vague Request",
            "description": "Teacher provides minimal information",
            "request": """
I need some materials.
""",
            "expected_checks": [
                "Agent asks for clarification on topic",
                "Asks about student language background",
                "Asks about age group",
                "Asks about level",
                "Asks about format needed",
                "Does NOT generate until all info provided",
            ],
        },
        {
            "name": "Contradictory Requirements",
            "description": "Teacher gives conflicting information",
            "request": """
I need materials for 'present simple' and 'past simple' at the same time.
Students are both beginner and advanced.
Can you generate for kids and adults both?
I need slides, worksheet, activities, and lesson plans.
""",
            "expected_checks": [
                "Agent clarifies: one topic or multiple?",
                "Agent confirms level: beginner or advanced?",
                "Agent confirms age group: kids or adults?",
                "Asks which formats are priorities",
                "Gets clear confirmation before proceeding",
            ],
        },
        {
            "name": "Many Corrections",
            "description": "Teacher keeps asking for changes",
            "request": """
Actually, I meant Spanish speakers, not Portuguese.
Wait, no - add Chinese speakers too.
Actually, can you make the slides more visual?
And add more practice activities.
Can you change the level to advanced?
""",
            "expected_checks": [
                "Agent tracks requirement changes",
                "Agent asks for confirmation after each change",
                "Regenerates materials when requirements finalized",
                "Does NOT regenerate on every change request",
            ],
        },
        {
            "name": "Unusual Format Request",
            "description": "Teacher asks for uncommon format",
            "request": """
I need the materials in a unusual format:
- Generate video transcripts
- Create an interactive game
- Export as a lesson plan document
Topic: conditionals
Students: Japanese speakers, advanced
""",
            "expected_checks": [
                "Agent acknowledges request",
                "Explains what formats are supported (slides, worksheet, activities)",
                "Offers closest alternative",
                "Suggests how to adapt materials for their needs",
            ],
        },
        {
            "name": "Database File Missing Scenario",
            "description": "Graceful handling if grammar file corrupted",
            "request": """
I need materials for 'present_simple_corrupted_test' (simulating missing file).
Spanish speakers, adults, beginner.
Slides and worksheet.
""",
            "expected_checks": [
                "Agent checks file exists before searching",
                "Provides helpful error message if missing",
                "Suggests alternatives",
                "Offers available grammar topics",
            ],
        },
        {
            "name": "Mixed Valid and Invalid L1s",
            "description": "Some L1s are supported, some aren't",
            "request": """
Students include:
- Native Spanish speakers (yes)
- Native Arabic speakers (maybe)
- Native Vulcan speakers (probably not)

Topic: articles
Level: intermediate
Age: adults
Slides and worksheet.
""",
            "expected_checks": [
                "Agent confirms Spanish is supported",
                "Confirms Arabic availability",
                "Notes Vulcan is not available",
                "Uses L1 Oracle for supported languages only",
                "Generates general materials without L1 targeting for unsupported",
            ],
        },
        {
            "name": "Extremely Long Context",
            "description": "Teacher provides excessive detail",
            "request": """
I've been teaching ESL for 20 years. My students are primarily young adults,
aged 18-25, from various backgrounds including Spain, Mexico, Colombia,
Venezuela, and parts of Central America. Most are Spanish speakers, though
some have mixed native language backgrounds. They're all at the intermediate
level, having completed 200+ hours of English instruction. They're preparing
for TOEIC exams. The classroom is equipped with projectors, whiteboards,
computers, and tablets. I need colorful, engaging materials. The topic is
present perfect continuous. I'd like slides with lots of visuals, a worksheet
with mixed practice types, activity cards for group work, and maybe a checklist
for self-assessment. Can you make it culturally relevant to Latin American
context? I prefer British English. The materials should take about 2 class
hours to complete.
""",
            "expected_checks": [
                "Agent extracts key info: grammar topic, L1, level, format",
                "Confirms understanding concisely",
                "Generates materials based on core requirements",
                "Notes special preferences (British English, culturally relevant)",
                "Delivers materials matching specifications",
            ],
        },
    ]

    @staticmethod
    def print_scenario(scenario: dict):
        """Print a stress test scenario."""
        print("\n" + "=" * 70)
        print(f"SCENARIO: {scenario['name']}")
        print(f"Description: {scenario['description']}")
        print("=" * 70)
        print(f"\nRequest:\n{scenario['request'].strip()}\n")
        print("Expected Behavior:")
        for i, check in enumerate(scenario["expected_checks"], 1):
            print(f"  {i}. {check}")

    @staticmethod
    def print_all_scenarios():
        """Print all stress test scenarios."""
        print("\n" * 2)
        print("╔" + "═" * 68 + "╗")
        print("║" + " " * 68 + "║")
        print("║" + "PHASE 2: STRESS TESTING SCENARIOS".center(68) + "║")
        print("║" + " " * 68 + "║")
        print("╚" + "═" * 68 + "╝")
        print()
        print(f"Total Scenarios: {len(StressTestScenarios.SCENARIOS)}\n")

        for i, scenario in enumerate(StressTestScenarios.SCENARIOS, 1):
            StressTestScenarios.print_scenario(scenario)
            print()

        print("\n" + "=" * 70)
        print("INSTRUCTIONS FOR TESTING")
        print("=" * 70)
        print("""
1. Run each scenario manually with the CogniESL agent
2. For each scenario, verify the expected behavior checklist
3. Note any issues or unexpected behavior
4. Check agent logs for proper error handling
5. Verify validation pipeline catches issues (Step 4.5)

Each scenario tests different edge cases:
- Multiple L1s: Ensures parallel L1 Oracle generation
- Invalid inputs: Graceful error handling and suggestions
- Incomplete requests: Proper clarification loop
- Contradictions: Clear confirmation before proceeding
- Database issues: Handles missing files gracefully
- Edge cases: Context length, format requests, preferences

A passing test suite means:
✓ Agent handles all edge cases gracefully
✓ No crashes or unhandled exceptions
✓ Clear user-friendly error messages
✓ Proper validation before material delivery
✓ Helpful suggestions for corrections
""")


def test_file_safety_checker():
    """Test the file safety checker utility."""
    print("\n" + "=" * 70)
    print("FILE SAFETY CHECKER TEST")
    print("=" * 70)

    try:
        from file_safety import FileSafetyChecker

        checker = FileSafetyChecker()

        print("\nChecking database files...")
        print(f"Grammar files available: {len(checker.list_available_grammar_topics())}")
        print(f"L1 language files available: {len(checker.list_available_l1_languages())}")
        print(f"Activity files available: {len(checker.list_available_activities())}")

        # Test grammar search
        exists, result = checker.verify_grammar_file_exists("present_simple")
        print(f"\nGrammar 'present_simple': {'✓ Found' if exists else '✗ Not found'}")

        # Test L1 search
        exists, result = checker.verify_l1_interference_file_exists("spanish")
        print(f"L1 'spanish': {'✓ Found' if exists else '✗ Not found'}")

        print("\n✓ File safety checker working correctly")

    except Exception as e:
        print(f"✗ File safety checker test failed: {e}")


def test_error_handler():
    """Test the error handler utility."""
    print("\n" + "=" * 70)
    print("ERROR HANDLER TEST")
    print("=" * 70)

    try:
        from error_handler import ErrorHandler, ErrorSeverity

        # Test grammar not found
        error = ErrorHandler.grammar_not_found(
            "zeptogram", ["present_simple", "past_simple", "present_continuous"]
        )
        print(f"\nGrammar not found error:")
        print(f"  Severity: {error.severity.value}")
        print(f"  User message: {error.user_message}")
        print(f"  Suggestion: {error.suggestion}")

        # Test incomplete requirements
        error = ErrorHandler.incomplete_requirements(["topic", "L1 language", "level"])
        print(f"\nIncomplete requirements error:")
        print(f"  User message: {error.user_message}")

        # Test validation failed
        error = ErrorHandler.validation_failed(
            "ValidateSlideSet",
            ["Slide 5: too small", "Slide 12: missing speaker notes"],
        )
        print(f"\nValidation failed error:")
        print(f"  User message: {error.user_message}")

        print("\n✓ Error handler working correctly")

    except Exception as e:
        print(f"✗ Error handler test failed: {e}")


if __name__ == "__main__":
    print("\n" * 2)
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "PHASE 2: COMPREHENSIVE TESTING SUITE".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "═" * 68 + "╝")

    # Test utilities
    test_file_safety_checker()
    test_error_handler()

    # Print stress test scenarios
    StressTestScenarios.print_all_scenarios()

    print("\n" + "=" * 70)
    print("Phase 2 testing suite ready. Next steps:")
    print("=" * 70)
    print("""
1. Run each stress scenario with the actual agent
2. Check audit logs for all operations
3. Verify validation catches issues before delivery
4. Test error messages are helpful and clear
5. Confirm no crashes on edge cases

See audit logs in /logs/ directory after testing.
""")
