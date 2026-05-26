"""File existence and safety checks for CogniESL database operations."""

from pathlib import Path
from typing import List, Tuple, Optional


class FileSafetyChecker:
    """Validates file existence and accessibility before operations."""

    def __init__(self, data_root: Optional[Path] = None):
        """Initialize with optional data root directory."""
        self.data_root = data_root or Path(__file__).parent.parent / "data"
        self.grammar_dir = self.data_root / "grammar"
        self.l1_interference_dir = self.data_root / "l1-interference"
        self.activities_dir = self.data_root / "activities"

    def verify_grammar_file_exists(self, grammar_topic: str) -> Tuple[bool, str]:
        """Check if grammar YAML file exists.

        Args:
            grammar_topic: Grammar point name (e.g., 'present_simple')

        Returns:
            (exists: bool, file_path_or_error: str)
        """
        # Normalize topic name: convert spaces to underscores, lowercase
        normalized = grammar_topic.lower().replace(" ", "_")

        # Try different possible filenames
        possible_names = [
            f"{normalized}.yaml",
            f"{normalized}.yml",
            grammar_topic.lower().replace(" ", "-") + ".yaml",
        ]

        for filename in possible_names:
            file_path = self.grammar_dir / filename
            if file_path.exists():
                return True, str(file_path)

        return False, (
            f"Grammar file not found: '{grammar_topic}'. "
            f"Checked in {self.grammar_dir}"
        )

    def verify_l1_interference_file_exists(self, l1_language: str) -> Tuple[bool, str]:
        """Check if L1 interference YAML file exists.

        Args:
            l1_language: Language name (e.g., 'Spanish', 'Chinese')

        Returns:
            (exists: bool, file_path_or_error: str)
        """
        # Normalize language name
        normalized = l1_language.lower().replace(" ", "_")

        possible_names = [
            f"{normalized}.yaml",
            f"{normalized}.yml",
            l1_language.lower().replace(" ", "-") + ".yaml",
        ]

        for filename in possible_names:
            file_path = self.l1_interference_dir / filename
            if file_path.exists():
                return True, str(file_path)

        return False, (
            f"L1 interference file not found: '{l1_language}'. "
            f"Checked in {self.l1_interference_dir}"
        )

    def verify_activities_file_exists(self, activity_name: str) -> Tuple[bool, str]:
        """Check if activity YAML file exists.

        Args:
            activity_name: Activity name

        Returns:
            (exists: bool, file_path_or_error: str)
        """
        normalized = activity_name.lower().replace(" ", "_")

        possible_names = [
            f"{normalized}.yaml",
            f"{normalized}.yml",
            activity_name.lower().replace(" ", "-") + ".yaml",
        ]

        for filename in possible_names:
            file_path = self.activities_dir / filename
            if file_path.exists():
                return True, str(file_path)

        return False, (
            f"Activity file not found: '{activity_name}'. "
            f"Checked in {self.activities_dir}"
        )

    def list_available_grammar_topics(self) -> List[str]:
        """List all available grammar topics in database."""
        if not self.grammar_dir.exists():
            return []
        files = list(self.grammar_dir.glob("*.yaml")) + list(
            self.grammar_dir.glob("*.yml")
        )
        return sorted([f.stem for f in files])

    def list_available_l1_languages(self) -> List[str]:
        """List all available L1 languages in database."""
        if not self.l1_interference_dir.exists():
            return []
        files = list(self.l1_interference_dir.glob("*.yaml")) + list(
            self.l1_interference_dir.glob("*.yml")
        )
        return sorted([f.stem for f in files])

    def list_available_activities(self) -> List[str]:
        """List all available activities in database."""
        if not self.activities_dir.exists():
            return []
        files = list(self.activities_dir.glob("*.yaml")) + list(
            self.activities_dir.glob("*.yml")
        )
        return sorted([f.stem for f in files])

    def verify_all_l1_languages(self, l1_list: List[str]) -> Tuple[List[str], List[str]]:
        """Verify all specified L1 languages exist.

        Args:
            l1_list: List of L1 language names

        Returns:
            (valid_languages, missing_languages)
        """
        valid = []
        missing = []

        for lang in l1_list:
            exists, _ = self.verify_l1_interference_file_exists(lang)
            if exists:
                valid.append(lang)
            else:
                missing.append(lang)

        return valid, missing

    def suggest_grammar_topic(self, user_input: str) -> Optional[str]:
        """Suggest a grammar topic based on user input (fuzzy matching).

        Args:
            user_input: User's grammar topic request

        Returns:
            Suggested topic name or None
        """
        available = self.list_available_grammar_topics()
        user_normalized = user_input.lower().replace(" ", "_")

        # Exact match
        if user_normalized in available:
            return user_normalized

        # Partial match
        for topic in available:
            if user_normalized in topic or topic in user_normalized:
                return topic

        return None

    def suggest_l1_language(self, user_input: str) -> Optional[str]:
        """Suggest an L1 language based on user input.

        Args:
            user_input: User's L1 language name

        Returns:
            Suggested language name or None
        """
        available = self.list_available_l1_languages()
        user_normalized = user_input.lower().replace(" ", "_")

        # Exact match
        if user_normalized in available:
            return user_normalized

        # Partial match
        for lang in available:
            if user_normalized in lang or lang in user_normalized:
                return lang

        return None
