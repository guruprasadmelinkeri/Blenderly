import anthropic
import json

client = anthropic.Anthropic()

def generate_plan(user_task: str) -> list:
    system_prompt = open("system_prompt.txt").read()  # paste the system prompt there
    
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=4096,
        system=system_prompt,
        messages=[
            {
                "role": "user",
                "content": f"Task: {user_task}\n\nGenerate a complete step-by-step plan.json to accomplish this task in Blender. Start from a default Blender scene unless otherwise specified. Be thorough — include all waits, all menu navigations, and all confirmations."
            }
        ]
    )
    
    raw = response.content[0].text.strip()
    return json.loads(raw)


# Usage
plan = generate_plan("Add a UV sphere, apply subdivision surface modifier level 2, shade smooth")

with open("plan.json", "w") as f:
    json.dump(plan, f, indent=2)