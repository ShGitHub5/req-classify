# req-classify
Azure OpenAI-based solution for automated requirement classification(Functional, Non-Functional, Compliance)

# Azure OpenAI MDM Requirements Generator
Generate structured **Functional**, **Non-Functional**, and **Compliance** requirements for a Master Data Management (MDM) solution using **Azure OpenAI**. It supports:
•	Manual text input
•	Single or multiple file uploads (.txt format)
•	Dynamic output file saving based on user options
•	Validation for empty files and unsupported file types
•	Ambiguity detection in requirements (flags unclear items as “Needs clarification”)



---

## 📁 Project Structure
```
myaihonors/
│
├── myaihonors.py        # Main script
├── upload1.txt          # Example input file
├── upload2.txt          # Example input file
├── empty.txt            # Example empty file for negative test
├── Hello_yellow.png     # Example unsupported file for negative test
├── sample_output1.md    # Generated output for option1
├── sample_output2.md    # Generated output for option2
├── sample_output3.md    # Generated output for option3
└── .env                 # Environment variables
└── README.md            # This documentation
```

---

## 🚀 Features
✅ Accepts manual text input or file uploads
✅ Handles multiple documents and merges content
✅ Detects empty files and shows error
✅ Rejects unsupported file types (.png, .jpg, .pdf, etc.)
✅ Adds clarification notes for ambiguous requirements
✅ Saves API response to different output files based on user option

---

## ✅ Prerequisites
- Python **3.12** (or compatible)
- Azure OpenAI resource and **deployment** (e.g., `gpt-4o`)
- Packages: `openai`, `python-dotenv`

Install dependencies:
```bash
python -m pip install --upgrade pip
pip install openai python-dotenv
```

> If you use a virtual environment:
```bash
python -m venv .venv
.venv\\Scripts\\activate  # Windows
# source .venv/bin/activate  # macOS/Linux
pip install openai python-dotenv
```

---

## 🔐 Environment Variables (.env)
Create a `.env` file in the project root (same folder as `myaihonors.py`). Real data like openAI endpoint/secret key is not disclosed below due to security reasons.

```env
OPENAI_API_VERSION=2024-02-01
AZURE_OPENAI_ENDPOINT=<{BASE_URL}/api/azureai>
AZURE_OPENAI_API_KEY=<your-secret-key>
```

## 🧠 Usage
Run the script:
```bash
python myaihonors.py
```
Example Cases
Case 1: Manual Text Input
process_inputs(
    text_input="I have requirements of MDM(master data management)...",
    options="option1"
)
✅ Output saved to sample_output1.md
Case 2: Single File Upload
process_inputs(
    file_names=["upload1.txt"],
    options="option2"
)
✅ Output saved to sample_output2.md
Case 3: Multiple Files
process_inputs(
    file_names=["upload1.txt", "upload2.txt"],
    options="option3"
)
✅ Output saved to sample_output3.md
Dynamic Output File Logic
options="option1" → sample_output1.md
options="option2" → sample_output2.md
options="option3" → sample_output3.md
Else → sample_output_default.md
Error Handling
Empty file → Logs error: Invalid input: file is empty
Unsupported file type → Logs error: Unsupported file type
Ambiguous requirements → Adds note: Needs clarification

---

## 🖥️ Script (excerpt)
```python
import logging
from dotenv import load_dotenv
import os
from openai import AzureOpenAI

# --- Simple Logging Setup ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load environment variables
load_dotenv()

# Read environment variables
OPENAI_API_VERSION = os.getenv("OPENAI_API_VERSION") #For app user: you need to pass the version configured by the admin

AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT") #Eg: {BASE_URL}/api/azureai

AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY") #For App User: use the app-registration key along with the app configuration unique key name eg. app123key-configName, For Api User: Substitute the key generated from Key Config Panel


# Validate env vars
if not OPENAI_API_VERSION or not AZURE_OPENAI_ENDPOINT or not AZURE_OPENAI_API_KEY:
    logging.error("Missing environment variables. Check .env file.")
    exit(1)


# Initialize client
client = AzureOpenAI()


# Log start
logging.info("Starting Azure OpenAI request...")

# Supported file types
SUPPORTED_EXTENSIONS = {".txt"}
UNSUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".pdf", ".docx"}

BASE_SYSTEM_PROMPT = ("You are a helpful assistant who writes complete, structured requirements.Always provide full sections: Functional, Non-Functional, and Compliance.Use clear headings, numbered lists, and avoid truncation.")


# --- Utility Functions ---
def is_empty(text):
    return not text.strip()

def is_supported_file(path):
    _, ext = os.path.splitext(path.lower())
    return ext in SUPPORTED_EXTENSIONS

def detect_ambiguity(texts):
    vague_terms = ["tbd", "unclear", "approx", "maybe", "needs clarification"]
    return any(term in t.lower() for term in vague_terms for t in texts)

def read_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        logging.error(f"Error reading file {path}: {e}")
        return ""

# --- Main Logic ---
def process_inputs(text_input=None, file_names=None, options=None):
    inputs = []

    # Case 1: Manual text input
    if text_input:
        logging.info("Manual text input detected.")
        inputs.append(text_input)

    # Case 2: Files provided
    if file_names:
        for fname in file_names:
            _, ext = os.path.splitext(fname.lower())
            if ext in UNSUPPORTED_EXTENSIONS:
                logging.error(f"Unsupported file type: {fname}. Allowed: .txt only.")
                return
            if ext not in SUPPORTED_EXTENSIONS:
                logging.error(f"Invalid file type: {fname}. Allowed: .txt only.")
                return

            if not os.path.exists(fname):
                logging.error(f"File not found: {fname}")
                return

            content = read_file(fname)
            if is_empty(content):
                logging.error(f"Invalid input: {fname} is empty.")
                return

            inputs.append(content)

    if not inputs:
        logging.error("No valid input provided.")
        return


    # Define system_prompt inside the function
    system_prompt = BASE_SYSTEM_PROMPT

    # Check ambiguity
    ambiguous = detect_ambiguity(inputs)
   
    if ambiguous:
        system_prompt += " If unclear, mark as 'Needs clarification' and suggest follow-up questions."

    # Merge multiple inputs
    user_prompt = "\n\n---\n\n".join(inputs)
    # logging.info(system_prompt)
    # logging.info(user_prompt)

    # Call Azure OpenAI
    try:
    # Prepare messages
        # system_prompt = ("You are a helpful assistant who writes complete, structured requirements.Always provide full sections: Functional, Non-Functional, and Compliance.Use clear headings, numbered lists, and avoid truncation.")
        # user_prompt = ("I have requirements of MDM(master data management). I have 3 entities used in the MDM. There are 2 data sources from where we load the data to the entities of MDM. Before loading data to MDM, the data is converted to JSON format and the JSON is then loaded into MDM. Then the attribute mapping and data quality check is done inside the MDM. The 3 entities which are used are HCO(Health care organization), HCP (Health care profession) & CLINICAL STUDY. There are match and merge as well as survivorship rules which are considered to get a concrete Operation value(golden record). This golden record is then dumped into the snowflake database from where it can be used for further use. I want to create requirements and classify them as functional, non-functional and compliance category.")
        logging.info("hello")
        # logging.info(system_prompt)
        # logging.info(user_prompt)
        res = client.chat.completions.create(
        model="gpt-4o", #Allowed values for ApiUser: gpt-4o,gpt-4o-mini
        messages=[{"role":"system","content":system_prompt},{"role":"user","content":user_prompt}],
        temperature= 0.2,
        max_tokens= 3000,
        top_p= 1.0,
        frequency_penalty= 0.0)


        # Log success
        logging.info("Request completed successfully.")
        logging.info(f"Token usage: {res.usage}")

        # Print full response
        print(res)
        print("------------------------------------------------------------------------")
        output = res.choices[0].message.content
        print(output)  

       
        # Write to file (overwrite each time)
        #with open("sample_output1.md", "w", encoding="utf-8") as f:
            #f.write(output)
        #logging.info("Response saved to sample_output1.md")
       
        # Write to file based on options
        if options == "option1":
            filename = "sample_output1.md"
        elif options == "option2":
            filename = "sample_output2.md"
        elif options == "option3":
            filename = "sample_output3.md"
        else:
            filename = "sample_output_default.md"  # fallback if option is not recognized

        # Overwrite the file every time
        with open(filename, "w", encoding="utf-8") as f:
            f.write(output)

        logging.info(f"Response saved to {filename}")


    except Exception as e:
        logging.error(f"Error during API call: {e}")

# --- Example Usage ---
if __name__ == "__main__":
    # CASE 1: Manual text input
      process_inputs(text_input="I have requirements of MDM(master data management). I have 3 entities used in the MDM. There are 2 data sources from where we load the data to the entities of MDM. Before loading data to MDM, the data is converted to JSON format and the JSON is then loaded into MDM. Then the attribute mapping and data quality check is done inside the MDM. The 3 entities which are used are HCO(Health care organization), HCP (Health care profession) & CLINICAL STUDY. There are match and merge as well as survivorship rules which are considered to get a concrete Operation value(golden record). This golden record is then dumped into the snowflake database from where it can be used for further use. I want to create requirements and classify them as functional, non-functional and compliance category.",options="option1")

    # CASE 2: Single file
      process_inputs(file_names=["upload1.txt"],options="option2")

    # CASE 3: Multiple files
      process_inputs(file_names=["upload1.txt", "upload2.txt"],options="option3")

    # CASE 4: Unsupported file type
      process_inputs(file_names=["Hello_yellow.png"])

    # CASE 5: Empty file
      process_inputs(file_names=["empty.txt"])
 
    # For now, run manual text example:
    # process_inputs(text_input="I have requirements of MDM(master data management). I have 3 entities used in the MDM. There are 2 data sources from where we load the data to the entities of MDM. Before loading data to MDM, the data is converted to JSON format and the JSON is then loaded into MDM. Then the attribute mapping and data quality check is done inside the MDM. The 3 entities which are used are HCO(Health care organization), HCP (Health care profession) & CLINICAL STUDY. There are match and merge as well as survivorship rules which are considered to get a concrete Operation value(golden record). This golden record is then dumped into the snowflake database from where it can be used for further use. I want to create requirements and classify them as functional, non-functional and compliance category.")


```

---

## 🔎 Troubleshooting
- **ModuleNotFoundError: openai** → `pip install openai python-dotenv`.
- **Truncated output** → Increase `max_tokens` (e.g., 2000+), reduce penalties.
- **401/403** → Verify API key, endpoint.
- **Env not loading** → `.env` must be in the same directory, and `load_dotenv()` must be called.
- **Interpreter mismatch** → Confirm VS Code interpreter (Python 3.12).

---

## 🔒 Security
- **Never** commit real secrets. Use placeholders in `.env`.
- Prefer **Azure Key Vault** or environment variables in CI/CD for production.

---

## 📦 Publish to GitHub
Initialize and push:
```bash
git init
git add .
git commit -m "Initial commit: Azure OpenAI MDM requirements generator"
git branch -M main
git remote add origin https://github.com/<your-username>/<repo-name>.git
git push -u origin main
```

Your repository link (FQDN) for slides:
```
https://github.com/<your-username>/<repo-name>
```

---

## 📝 License
Add a license if you plan to share (e.g., MIT).

---

## 🙌 Credits
Created by **Shilpa Chetan Desai** using Azure OpenAI.



