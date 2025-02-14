from guardrails import Guard
import json
import re
import jsonschema

class StudyConfigKeyModifier:
    def __init__(self, study_config, schema):
        """Initialize the Guardrails instance, study config, and validation schema."""
        self.guard = Guard()
        self.study_config = study_config
        self.schema = schema

    def get_system_prompt(self, relevant_keys):
        """Generate a system prompt that ensures modifications are made."""

        example_json = {key: self.study_config[key] for key in relevant_keys}

        return f"""
        You are an AI assistant modifying a machine learning model's configuration.

        ### **Study Configuration (Current Values)**
        {json.dumps(self.study_config, indent=2)}
        
        ### **Modification Task**
        - Adjust **only** the following relevant keys based on the user's request:
        {json.dumps(relevant_keys, indent=2)}
        - **Modify each value in a way that aligns with the user's request.**
        - **Do NOT leave all values unchanged. If the user’s request is unclear, make reasonable modifications.**
        - Ensure all values conform to these constraints:
        
        ### **Valid Ranges and Constraints**
        {json.dumps(self.schema, indent=2)}
        
        ### **Strict Output Format**
        - **Your entire response must be a valid JSON object.**
        - **Ensure that ALL relevant keys are included in the response.**
        - **DO NOT return explanations, notes, or any additional text.**
        - **DO NOT wrap the JSON in Markdown formatting (e.g., ```json ... ```).**
        - **At least some values must change based on user intent.**
        - The response should look exactly like this:
        
        {json.dumps(example_json, indent=2)}
        
        BUT with some modifications applied to reflect the user's request.
        """

    def modify_config(self, user_prompt, relevant_keys):
        """Ask LLM to modify the extracted keys based on user input."""
        messages = [
            {"role": "system", "content": self.get_system_prompt(relevant_keys).strip()},
            {"role": "user", "content": user_prompt}
        ]

        print("⏱️Sending request to LLM for modification...")
        result = self.guard(messages=messages, model="gpt-4o")

        print("🛜Raw LLM Response:")
        print(result.validated_output)
        return self.validate_output(result.validated_output)

    def validate_output(self, raw_output):
        """Cleans, parses, and validates the modified config against the schema."""
        clean_output = re.sub(r"```json\n|\n```", "", raw_output)

        try:
            modified_config = json.loads(clean_output)
            jsonschema.validate(instance=modified_config, schema=self.schema)
            return modified_config
        except (json.JSONDecodeError, jsonschema.ValidationError) as e:
            print("🔴Validation Error:", str(e))
            return None