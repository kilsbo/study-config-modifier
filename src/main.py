from study_config_key_extractor import StudyConfigKeyExtractor
from study_config_key_modifier import StudyConfigKeyModifier
import json
import time

study_schema = {
    "type": "object",
    "properties": {
        "hours_per_week": {"type": "integer", "minimum": 0, "maximum": 100},
        "lectures_per_week": {"type": "integer", "minimum": 0, "maximum": 20},
        "self_study_hours": {"type": "integer", "minimum": 0, "maximum": 60},
        "max_allowed_absences": {"type": "integer", "minimum": 0, "maximum": 50},
        "exam_weight": {"type": "number", "minimum": 0.0, "maximum": 1.0},
        "min_attendance_percentage": {"type": "integer", "minimum": 0, "maximum": 100}
    },
    "required": ["hours_per_week", "lectures_per_week", "self_study_hours",
                 "max_allowed_absences", "exam_weight", "min_attendance_percentage"]
}

study_config = {
    "university_name": "Oxford University",
    "study_program": "Computer Science",
    "study_period_start": "2025-09-01",
    "study_period_end": "2028-06-30",
    "hours_per_week": 40,
    "lectures_per_week": 10,
    "self_study_hours": 20,
    "holidays_per_year": 6,
    "max_allowed_absences": 15,
    "grading_scale": "A-F",
    "assignment_weight": 0.4,
    "exam_weight": 0.6,
    "required_gpa": 3.5,
    "min_attendance_percentage": 75,
    "tuition_fees": 12000,
    "scholarship_eligibility": True,
    "online_course_availability": True,
    "weekly_project_work": 5,
    "thesis_required": True,
    "internship_mandatory": False
}

def main():
    start_time = time.time()

    user_prompt = "If I take two weeks off from my studies, how will that affect my performance in my exams?"

    # Extractor: Identify relevant keys
    extractor = StudyConfigKeyExtractor(study_config)
    relevant_keys = extractor.analyze_prompt(user_prompt)

    print("🛜Relevant Study Configuration Keys Identified:")
    print(json.dumps(relevant_keys, indent=2))

    if not relevant_keys:
        print("⚠️No relevant keys were identified. Exiting...")
        return

    # Modifier: Generate modified study config
    modifier = StudyConfigKeyModifier(study_config, study_schema)
    modified_config = modifier.modify_config(user_prompt, relevant_keys)

    if modified_config:
        print("✅Updated Study Configuration:")
        print(json.dumps(modified_config, indent=2))
    else:
        print("❌Modification failed. No valid updates generated.")

    end_time = time.time()
    elapsed_time = end_time - start_time
    minutes, seconds = divmod(int(elapsed_time), 60)
    milliseconds = int((elapsed_time - int(elapsed_time)) * 1000)
    print(f"⏱ Total execution time: {minutes}m {seconds}s {milliseconds}ms")

if __name__ == "__main__":
    main()





