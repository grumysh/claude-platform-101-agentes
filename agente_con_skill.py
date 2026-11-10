from pathlib import Path

from dotenv import load_dotenv
import anthropic
from anthropic.lib import files_from_dir

load_dotenv()

client = anthropic.Anthropic()

SKILL_NAME = "daily-status-report"
SKILL_DIR = Path(__file__).parent / "skills" / SKILL_NAME

skill = next(
    (s for s in client.skills.list(source="custom") if s.display_name == SKILL_NAME),
    None,
)

if skill is None:
    skill = client.skills.create(files=files_from_dir(SKILL_DIR))
    print(f"Skill creada: {skill.id}")
else:
    print(f"Skill existente: {skill.id}")

activity_log = """
2026-11-10
09:12 Ana merged PR #42 (login page redesign)
09:40 Luis started working on the payments API
11:05 Marta reported the staging database is down, cannot run tests
13:30 Ana fixed bug #57 (wrong totals in cart)
15:20 Luis still on payments API, 60% done
16:45 Marta waiting on DevOps to restore staging
"""

runner = client.beta.messages.tool_runner(
    model="claude-opus-5",
    max_tokens=16000,
    container={
        "skills": [
            {
                "type": "custom",
                "skill_id": skill.id,
                "version": "latest",
            }
        ]
    },
    tools=[
        {
            "type": "code_execution_20250825",
            "name": "code_execution",
        }
    ],
    messages=[
        {
            "role": "user",
            "content": f"Generate the daily status report from this activity log:\n\n{activity_log}",
        }
    ],
)

response = runner.until_done()

for block in response.content:
    if block.type == "text":
        print(block.text)
