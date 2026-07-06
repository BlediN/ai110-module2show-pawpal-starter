# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
PawPal+ demo for Jordan
Today's Schedule
07:30 - 08:00 | Biscuit: Morning walk [high priority]
08:00 - 08:05 | Mittens: Medication [scheduled as requested]
08:15 - 08:25 | Biscuit: Breakfast [high priority]
09:00 - 09:20 | Mittens: Playtime [scheduled as requested]
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
============================= test session starts =============================
collected 2 items

tests/test_pawpal.py ..                                                  [100%]

============================== 2 passed in 0.05s ==============================
```

## 📐 Smarter Scheduling

The scheduler now sorts tasks by requested time first and then by priority, while also shifting later tasks if an earlier one runs long.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.build_daily_schedule()` | Orders by time, then priority, then pet/task name. |
| Filtering | `Pet.pending_tasks()` | Completed tasks are excluded from the plan. |
| Conflict handling | `Scheduler.build_daily_schedule()` | Overlapping tasks are pushed later to avoid collisions. |
| Recurring tasks | `Task.is_recurring()` | Stores whether a task is once, daily, or weekly. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. Open the Streamlit app and review the current owner and sample pets.
2. Add a new pet or keep the seeded demo pets.
3. Add one or more tasks with a time, duration, priority, and frequency.
4. Click Generate schedule to see the ordered plan for the day.
5. Compare the schedule output with the task list to confirm the backend logic is working.

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
