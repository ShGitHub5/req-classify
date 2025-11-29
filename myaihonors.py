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
