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

Sorted Tasks
07:30 | Morning walk (daily, due 2026-07-05)
08:00 | Medication (daily, due 2026-07-05)
08:00 | Playtime (weekly, due 2026-07-05)
08:15 | Breakfast (daily, due 2026-07-05)
19:00 | Evening walk (daily, due 2026-07-05)
19:00 | Evening walk (daily, due 2026-07-06)

Filtered Tasks for Biscuit
19:00 | Biscuit: Evening walk [done]
07:30 | Biscuit: Morning walk [open]
08:15 | Biscuit: Breakfast [open]
19:00 | Biscuit: Evening walk [open]

Conflict Warnings
Warning: 2 tasks share 08:00: Mittens: Medication; Mittens: Playtime

Today's Schedule
07:30 - 08:00 | Biscuit: Morning walk [high priority]
08:00 - 08:05 | Mittens: Medication [scheduled as requested]
08:05 - 08:25 | Mittens: Playtime [moved later to avoid overlap with earlier tasks]
08:25 - 08:35 | Biscuit: Breakfast [moved later to avoid overlap with earlier tasks]
```

## ✨ Features

- Sorts pet care tasks by time, priority, and description.
- Filters tasks by pet name, completion status, and due date.
- Flags start-time conflicts with helpful warnings.
- Creates the next daily or weekly task when a recurring task is completed.
- Shows a readable daily schedule for terminal and Streamlit use.

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
python -m pytest

# Run with coverage:
pytest --cov
```

These tests cover the main scheduler behaviors: task ordering, filtering by pet/status, recurring-task rollover, and exact-time conflict detection.

```
============================= test session starts =============================
platform win32 -- Python 3.13.0, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\HP-B\Documents\GDrive\Computing\CodePath\AI110\Assignments\ai110-module2show-pawpal-starter
plugins: anyio-4.14.1
collected 6 items

tests\test_pawpal.py ......                                              [100%]

============================== 6 passed in 0.09s ==============================
```

Confidence Level: ★★★★☆

## 📐 Smarter Scheduling

The scheduler now sorts tasks by requested time first and then by priority, filters tasks by pet or completion status, creates the next occurrence for recurring tasks, and warns when tasks share the same start time.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Sorts by `HH:MM`, then priority, then description. |
| Filtering | `Scheduler.filter_tasks()` | Filters by pet name, completion status, and due date. |
| Conflict handling | `Scheduler.detect_conflicts()` | Returns warning messages for exact time matches. |
| Recurring tasks | `Task.next_occurrence()` / `Pet.complete_task()` | Daily and weekly tasks create the next due task when completed. |

## 🎬 Demo Walkthrough

PawPal+ opens in Streamlit with a simple workflow: enter or update the owner name, add pets, and create care tasks with a time, duration, priority, and frequency. The app keeps the owner and pet data in session state, so the list stays available as you add more items.

Example workflow:

1. Add a pet such as Biscuit or Mittens.
2. Schedule tasks like a morning walk, medication, or feeding.
3. Use the sorting panel to see tasks ordered by time.
4. Use the filter controls to narrow the list by pet or completion status.
5. Review conflict warnings if two tasks share the same time.
6. Generate today's schedule to see the final ordered plan.

Key Scheduler behaviors shown in the app:

- Sorting by time with `Scheduler.sort_by_time()`.
- Filtering by pet and status with `Scheduler.filter_tasks()`.
- Conflict warnings with `Scheduler.detect_conflicts()`.
- Recurring task rollover with `Pet.complete_task()` and `Task.next_occurrence()`.

Sample CLI output from `main.py`:

```
PawPal+ demo for Jordan

Sorted Tasks
07:30 | Morning walk (daily, due 2026-07-05)
08:00 | Medication (daily, due 2026-07-05)
08:00 | Playtime (weekly, due 2026-07-05)
08:15 | Breakfast (daily, due 2026-07-05)
19:00 | Evening walk (daily, due 2026-07-05)
19:00 | Evening walk (daily, due 2026-07-06)

Filtered Tasks for Biscuit
19:00 | Biscuit: Evening walk [done]
07:30 | Biscuit: Morning walk [open]
08:15 | Biscuit: Breakfast [open]
19:00 | Biscuit: Evening walk [open]

Conflict Warnings
Warning: 2 tasks share 08:00: Mittens: Medication; Mittens: Playtime

Today's Schedule
07:30 - 08:00 | Biscuit: Morning walk [high priority]
08:00 - 08:05 | Mittens: Medication [scheduled as requested]
08:05 - 08:25 | Mittens: Playtime [moved later to avoid overlap with earlier tasks]
08:25 - 08:35 | Biscuit: Breakfast [moved later to avoid overlap with earlier tasks]
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
