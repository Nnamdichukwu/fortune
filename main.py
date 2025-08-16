"""
1. I want to hit the github api endpoint to get the latest release
2. Check if we have the endpoint_state.json stored. If we do, then check if the version in the latest release is same as endpoint.json
3. If its the same version then do nothing -- print "Same version"
4. If not same version, then use LLM to summarise the release notes. 
5. Save release notes to endpoint_output.json
6. Update endpoint_state.json with the latest version

"""
from packaging.version import Version, InvalidVersion
import requests
import os, json
from pathlib import Path
from typing import Any
from llm import get_changelog
def get_latest_release(owner: str, repo: str, path:str) -> str:
    api_str = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
    resp = requests.get(api_str)
    api = resp.json()
    is_file = is_file_exists(owner,path)
    print(f"Is file is: {is_file} ")
    file_path =  os.path.join(path, f"{owner}_state.json")
    Path(path).mkdir(parents=True, exist_ok=True)
    body = api['body']
    new_version =extract_version(api)
    print(new_version)
    is_file = is_file_exists(owner, path)
    if is_file:
        print("file exists")
        data= read_json_file(file_path)
        old_version = data['version']
        
        if compare_versions(old_version, new_version):
            print("There is a new version")
            try:
                release_note = get_changelog(body)
            except Exception as e:
                print(f"Error generating changelog: {e}")
            update_version(file_path, new_version)
        
            print("Updated version")
            p = Path(f"{owner}_output.txt")
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(release_note, encoding="utf-8")
        
        else: 
            return "No new change"
    try:
        print("File not exist")
        release_note = get_changelog(body)
        print("Updated release notes")
        update_version(file_path, new_version)
        print("Updated version")
    except Exception as e:
        print(f"Error generating changelog: {e}")

    output_path = os.path.join(path, f"{owner}_output.json")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(release_note)
 

    update_version(file_path, new_version)

    

def is_file_exists(owner,path)-> bool:
    path= f"{path}/{owner}_state.json"
    print(path)
    try:
        does_exist = os.path.isfile(path)
        print(f"does {path} exist: {does_exist}")
        return does_exist
    except Exception as e:
        print(f"Cannot check file due to {e}")
        
def read_json_file(path: str) -> Any:
    p = Path(path)
    try:
        with p.open("r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {p.resolve()}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {p}: {e.msg}") from e

def extract_version(output: dict ) -> str:
    return output['name']

def compare_versions(old_version: str, new_version: str ) -> bool:
   try:
       is_less_than = Version(old_version) < Version(new_version)
       return is_less_than
   except InvalidVersion as e:
       print(f"Failed to check version due to {e}")
       return False
def update_version(path: str, new_version: str):
    p = Path(path)
    
    p.parent.mkdir(parents=True, exist_ok=True)


    if p.exists():
        try:
            with p.open("r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError):
            data = {}  
    else:
        data = {}

    
    data["version"] = new_version

   
    with p.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
