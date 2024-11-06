import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

with open("data/requirement-preset.txt", "r") as f:
    PRESETS = f.read()


def extract_requirement(jd):
    client = OpenAI(api_key=os.environ.get("OPENSI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": PRESETS,
            },
            {
                "role": "user",
                "content": jd,
            },
        ],
        max_tokens=1024,
        n=1,
        stop=None,
    )

    return response.choices[0].message.content


if __name__ == "__main__":

    with open("data/examples/airbnb.json", "r") as f:
        data = json.loads(f.read())

    with open("data/jobs/{}".format(data["Job Description"]), "r") as f:
        jd = f.read()

    requires = extract_requirement(jd)

    print(requires)
