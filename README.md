# 🏫 Study Configuration Analyzer

## 📌 Overview

The **Study Configuration Analyzer** is a Python application that uses **Guardrails AI** and **OpenAI** to:
1. Extract relevant study configuration parameters from a given JSON.
2. Modify selected parameters based on a user's prompt while ensuring constraints are met.

This helps simulate how different study conditions affect academic performance.

## 🛠️ Features

✅ **Extract relevant study parameters**  
✅ **Modify parameters based on user intent**  
✅ **Validate outputs using JSON schema constraints**  
✅ **Uses Guardrails AI for structured LLM responses**  

## 📂 Project Structure

```
guardrail-demo/
│── src/
│   ├── main.py                    # Entry point for the application
│   ├── study_config_key_extractor.py  # Extracts relevant config keys
│   ├── study_config_key_modifier.py   # Modifies extracted keys based on the user's prompt
│── rail_specs/
│   ├── extract_keys.rail            # (Optional) Guardrails RAIL spec for key extraction
│── README.md
│── requirements.txt
```

## 🚀 Installation & Setup

### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/yourusername/study-config-analyzer.git
cd study-config-analyzer
```

### **2️⃣ Create a Virtual Environment**
```sh
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate  # Windows
```

### **3️⃣ Install Dependencies**
```sh
pip install -r requirements.txt
```

### **4️⃣ Set Up OpenAI API Key**
Create a `.env` file in the project root:
```
OPENAI_API_KEY=your-api-key-here
```

Or set it directly:
```sh
export OPENAI_API_KEY=your-api-key-here  # macOS/Linux
set OPENAI_API_KEY=your-api-key-here  # Windows
```

## 🏃 Usage

Run the main script:
```sh
python src/main.py
```

The program will:
1. **Extract relevant study parameters** from the config JSON.
2. **Modify selected values** based on user input.
3. **Ensure validation** of outputs before applying changes.

## 🔧 Configuration

The **study configuration** and **validation schema** are set inside `main.py`.  
Modify them as needed to fit different academic environments.

## 🎯 Example Usage

**User Input:**
```
"If I take two weeks off from my studies, how will that affect my performance in my exams?"
```

**Extracted Relevant Keys:**
```json
["hours_per_week", "lectures_per_week", "self_study_hours", "max_allowed_absences", "exam_weight", "min_attendance_percentage"]
```

**Modified Study Configuration:**
```json
{
  "hours_per_week": 38,
  "lectures_per_week": 9,
  "self_study_hours": 18,
  "max_allowed_absences": 17,
  "exam_weight": 0.65,
  "min_attendance_percentage": 70
}
```
