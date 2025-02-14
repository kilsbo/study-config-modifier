from guardrails import Guard
import json
import re

class StudyConfigKeyExtractor:
    def __init__(self, study_config):
        """Initialize the Guardrails instance with a provided study configuration."""
        self.guard = Guard()
        self.study_config = study_config
        self.valid_keys = set(study_config.keys())

    def get_system_prompt(self):
        """Generate the system prompt for the LLM."""
        return f"""
        You are an AI assistant analyzing a machine learning model's configuration.

        Below is a JSON configuration for an ML model that simulates study performance:

        {json.dumps(self.study_config, indent=2)}

        ### **Task:**
        - Identify which configuration values in the JSON should be **adjusted** or are **relevant** to answering this question.
        - Output **ONLY** a JSON array of relevant keys from the configuration.
        - Do **NOT** include explanations, additional text, or any formatting other than a valid JSON array.

        ### **Example Output Format:**
        ["hours_per_week", "lectures_per_week", "self_study_hours", "max_allowed_absences", "exam_weight", "min_attendance_percentage"]
        """

    def validate_keys(self, keys):
        """Ensure that all keys returned by LLM exist in the study config."""
        invalid_keys = [key for key in keys if key not in self.valid_keys]
        if invalid_keys:
            raise ValueError(f"Invalid keys detected: {invalid_keys}")
        return keys

    def analyze_prompt(self, user_prompt):
        """Send a user prompt to the LLM and return validated keys."""
        messages = [
            {"role": "system", "content": self.get_system_prompt()},
            {"role": "user", "content": user_prompt}
        ]

        print("⏱️Sending messages to LLM...")
        result = self.guard(messages=messages, model="gpt-4o")

        raw_output = result.validated_output
        cleaned_keys = self.clean_output(raw_output)

        validated_keys = self.validate_keys(cleaned_keys)

        return validated_keys

    @staticmethod
    def clean_output(raw_output):
        """Cleans the validated output by removing markdown formatting and parsing JSON."""
        clean_output = re.sub(r"```json\n|\n```", "", raw_output)
        try:
            return json.loads(clean_output)
        except json.JSONDecodeError:
            return []