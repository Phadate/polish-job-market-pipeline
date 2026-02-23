import json
import os

folder = "data/bronze/justjoin/2026-02-23"
files = os.listdir(folder)

# exclude the checkpoint file
json_files = [f for f in files if f.endswith(".json")]

print(f"Total files: {len(json_files)}")

# open 5 random files and check structure
import random
for filename in random.sample(json_files, 5):
    with open(f"{folder}/{filename}", encoding="utf-8") as f:
        job = json.load(f)
    print({
        "title": job.get("title"),
        "city": job.get("city"),
        "skills": len(job.get("requiredSkills", [])),
        "salaries": len(job.get("employmentTypes", [])),
        "has_body": bool(job.get("body"))
    })