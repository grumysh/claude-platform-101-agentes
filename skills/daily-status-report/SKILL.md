---
name: daily-status-report
description: Turns a raw team activity log into a daily status report. Use when the user asks for a daily status report, standup summary, or end-of-day update from an activity log.
---

# Daily Status Report

Write the report in this exact format:

```
DAILY STATUS REPORT — <date from the log>

✅ Done
- <person>: <what they finished>

🔄 In progress
- <person>: <what they are working on>

🚧 Blockers
- <person>: <what is blocking them>  (or "None")

📊 Summary: <one sentence with the overall state of the team>
```

Rules:
- Group items by section, not by person.
- One line per item, short and concrete.
- Do not invent information that is not in the log.
