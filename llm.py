from pydantic import BaseModel 
from openai import OpenAI 
import os
from dotenv import load_dotenv
load_dotenv()
API_KEY =os.getenv("API_KEY")
client = OpenAI(api_key = API_KEY)

class GithubReleaseNotes(BaseModel):
    name: str 
    version: str 
    body: str


def get_changelog(body:str) -> str :
    try:
        completion = client.beta.chat.completions.parse(
            model= "gpt-5",
            messages= [
                {"role": "system", "content": "from this release note, can you extract the most important information from this json and present in an easily digestible way. Essentially, I need to know the latest version and see if there is any action i need to take regarding updating to this version and why"},

                {"role": "user", "content": body}
            ],
            response_format= GithubReleaseNotes,
        )
        release_note = completion.choices[0].message.parsed
        return str(release_note)
    except Exception as e:
        print(f"Could not connect to openai due to {e}")
        return "" 
