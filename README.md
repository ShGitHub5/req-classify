# req-classify
Azure OpenAI-based solution for automated requirement classification(Functional, Non-Functional, Compliance)

# Azure OpenAI MDM Requirements Generator
Generate structured **Functional**, **Non-Functional**, and **Compliance** requirements for a Master Data Management (MDM) solution using **Azure OpenAI**.

---

## 📁 Project Structure
```
.
├── myaihonors.py        # Python script that calls Azure OpenAI
├── .env                 # Environment variables 
├── sample_output.md     # Full example: request & response from API
└── README.md            # This documentation
```

---

## 🚀 Features
- Generates complete requirement sets for MDM (Functional / Non-Functional / Compliance).
- Covers entities **HCO**, **HCP**, **Clinical Study** and key processes (JSON normalization, DQ, match & merge, survivorship, golden record, Snowflake export).
- Tuned parameters to reduce truncation.

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
Capture the output to a file (optional):
```bash
python myaihonors.py > sample_output.md
```

See **`sample_output.md`** for a full example of the request and response that this project produced.

---

## 🖥️ Script (excerpt)
```python
from openai import AzureOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_VERSION = os.getenv("OPENAI_API_VERSION") #For app user: you need to pass the version configured by the admin

AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT") #Eg: {BASE_URL}/api/azureai

AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY") #For App User: use the app-registration key along with the app configuration unique key name eg. app123key-configName, For Api User: Substitute the key generated from Key Config Panel


client = AzureOpenAI()


res = client.chat.completions.create(
    model="gpt-4o", #Allowed values for ApiUser: gpt-4o,gpt-4o-mini
    messages=[{"role":"system","content":"You are a helpful assistant who writes complete, structured requirements.Always provide full sections: Functional, Non-Functional, and Compliance.Use clear headings, numbered lists, and avoid truncation."},{"role":"user","content":"I have requirements of MDM(master data management). I have 3 entities used in the MDM. There are 2 data sources from where we load the data to the entities of MDM. Before loading data to MDM, the data is converted to JSON format and the JSON is then loaded into MDM. Then the attribute mapping and data quality check is done inside the MDM. The 3 entities which are used are HCO(Health care organization), HCP (Health care profession) & CLINICAL STUDY. There are match and merge as well as survivorship rules which are considered to get a concrete Operation value(golden record). This golden record is then dumped into the snowflake database from where it can be used for further use. I want to create requirements and classify them as functional, non-functional and compliance category."}],
    temperature= 0.2,
    max_tokens= 3000,
    top_p= 1.0,
    frequency_penalty= 0.0)

print(res)
print("------------------------------------------------------------------------")
print(res.choices[0].message.content)    
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
https://github.com/ShGitHub5/req-classify
```

---

## 📝 License
Add a license if you plan to share (e.g., MIT).

---

## 🙌 Credits
Created by **Shilpa Chetan Desai** using Azure OpenAI.



