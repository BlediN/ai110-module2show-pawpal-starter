# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

I designed four core classes: `Task`, `Pet`, `Owner`, and `Scheduler`. `Task` stores the care item details and completion state, `Pet` groups a pet's tasks, `Owner` manages multiple pets, and `Scheduler` turns all of the tasks into a readable daily plan.

**b. Design changes**

Yes. I added a small `ScheduleItem` value object and formatting helpers so the scheduler could return structured results instead of raw tuples. That made the demo output easier to read and kept the logic cleaner.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers task time, task priority, and whether the task is already completed. Time matters most because the tasks are daily routines, and priority is used to break ties when tasks overlap or share the same time.

**b. Tradeoffs**

The scheduler uses exact start-time matches for conflict detection instead of trying to calculate overlapping durations. That keeps the logic easy to understand and fast to explain, which is enough for a small pet-care planner even though it will miss some partial overlaps.

---

## 3. AI Collaboration

**a. How you used AI**

I used AI to brainstorm the class relationships, draft the dataclass-based skeleton, and tighten the schedule formatting. The most helpful prompts were specific ones like asking how the `Scheduler` should retrieve tasks from the `Owner` and how to make the CLI output easier to read.

**b. Judgment and verification**

I did not accept a purely decorative UI suggestion when the backend was still missing. I verified the design by running the CLI demo and tests, and I only kept the AI suggestions that matched the actual object model and produced clear output.

**c. AI strategy**

The most effective AI features were multi-step code generation, small refactoring suggestions, and help turning vague requirements into concrete method names. I rejected suggestions that added extra complexity, such as broad optimization logic or UI flourishes that did not help the scheduler behavior.

**d. Separate chat sessions**

Using separate chat sessions for design, implementation, testing, and documentation kept each phase focused. It helped me avoid mixing architectural decisions with test debugging, and it made it easier to compare the final code against the original plan.

**e. Lead architect takeaway**

Working as the lead architect meant I had to decide when AI should generate options and when I should choose the simplest readable version. I learned that strong AI support is most useful when I keep the data model and user goals clear, then verify every major behavior with tests and a CLI demo.

---

## 4. Testing and Verification

**a. What you tested**

I tested that `mark_complete()` changes a task's status and that adding a task to a pet increases the pet's task count. Those are the smallest behaviors that prove the objects are wired together correctly.

**b. Confidence**

I am moderately confident because the demo script and tests both run successfully. Next I would test longer schedules, invalid time strings, multiple tasks at the same time, and tasks that exceed the day's available window.

---

## 5. Reflection

**a. What went well**

I am most satisfied that the backend now has a clear object model and a readable schedule output that can be used by both the CLI and Streamlit layers.

**b. What you would improve**

I would add richer constraints such as pet-specific preferences, task recurrence by weekday, and automatic conflict warnings when too many tasks are scheduled for the same window.

**c. Key takeaway**

I learned that the fastest way to get a reliable AI-assisted system is to design the data model first, then validate the behavior with a small CLI demo before polishing the UI.
