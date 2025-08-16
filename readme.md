# GitHub Release Tracker

This project tracks the **latest release** of a GitHub repository, compares it against a locally stored state, and summarizes the release notes using an LLM.  
It ensures you are always aware of new versions and what actions (if any) you should take when updating.

---

## Features
- ✅ Fetches the latest release from the GitHub API  
- ✅ Compares the latest version with a locally stored version (`*_state.json`)  
- ✅ If versions are the same → prints **"Same version"**  
- ✅ If a new version exists:
  - Uses an LLM to **summarize the release notes**
  - Saves the summary to `*_output.json` and `*_output.txt`
  - Updates the stored version in `*_state.json`  

---

## Project Structure

- main.py - contains all the logic to get the latest releases from a repo
- llm.py - Calls the openai endpoint; can add support for other models but currently uses gpt-5