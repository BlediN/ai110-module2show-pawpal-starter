from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, time
from typing import Iterable


PRIORITY_ORDER = {
    "high": 0,
    "medium": 1,
    "low": 2,
}


def _parse_clock(clock_text: str) -> time:
    """Convert a HH:MM string into a time object."""

    try:
        return datetime.strptime(clock_text.strip(), "%H:%M").time()
    except ValueError as exc:
        raise ValueError("Time must use 24-hour HH:MM format.") from exc


def _format_clock(clock_value: time) -> str:
    """Format a time object for display."""

    return clock_value.strftime("%H:%M")


def _add_minutes(clock_value: time, minutes: int) -> time:
    """Add minutes to a time value and return the new time."""

    anchor = datetime.combine(datetime.today(), clock_value)
    return (anchor + timedelta(minutes=minutes)).time()


@dataclass
class Task:
    description: str
    time: str
    duration_minutes: int
    priority: str = "medium"
    frequency: str = "once"
    due_date: date = field(default_factory=date.today)
    completed: bool = False

    def mark_complete(self) -> Task | None:
        """Mark the task as completed and create the next recurring task if needed."""

        self.completed = True
        return self.next_occurrence()

    def mark_incomplete(self) -> None:
        """Mark the task as not completed."""

        self.completed = False

    def scheduled_time(self) -> time:
        """Return the task time as a time object."""

        return _parse_clock(self.time)

    def priority_rank(self) -> int:
        """Return a numeric rank for sorting priorities."""

        return PRIORITY_ORDER.get(self.priority.lower(), PRIORITY_ORDER["medium"])

    def is_recurring(self) -> bool:
        """Return True when the task repeats."""

        return self.frequency.lower() != "once"

    def next_occurrence(self) -> Task | None:
        """Create the next task instance for daily or weekly recurring tasks."""

        next_due_date: date | None = None
        if self.frequency.lower() == "daily":
            next_due_date = self.due_date + timedelta(days=1)
        elif self.frequency.lower() == "weekly":
            next_due_date = self.due_date + timedelta(days=7)

        if next_due_date is None:
            return None

        return Task(
            description=self.description,
            time=self.time,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            frequency=self.frequency,
            due_date=next_due_date,
        )

    def summary(self) -> str:
        """Return a one-line description of the task."""

        return (
            f"{self.time} - {self.description} ({self.duration_minutes} min, "
            f"priority: {self.priority}, due: {self.due_date.isoformat()})"
        )


@dataclass
class Pet:
    name: str
    species: str
    age: int | None = None
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a task to this pet."""

        self.tasks.append(task)

    def complete_task(self, task: Task) -> Task | None:
        """Mark a task complete and append the next recurring occurrence if needed."""

        next_task = task.mark_complete()
        if next_task is not None:
            self.tasks.append(next_task)
        return next_task

    def task_count(self) -> int:
        """Return the number of tasks assigned to the pet."""

        return len(self.tasks)

    def pending_tasks(self) -> list[Task]:
        """Return the tasks that have not been completed yet."""

        return [task for task in self.tasks if not task.completed]


@dataclass
class Owner:
    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's household."""

        self.pets.append(pet)

    def get_pet(self, pet_name: str) -> Pet | None:
        """Return a pet by name if it exists."""

        normalized_name = pet_name.strip().lower()
        for pet in self.pets:
            if pet.name.lower() == normalized_name:
                return pet
        return None

    def get_all_tasks(self) -> list[Task]:
        """Return every task across all pets."""

        tasks: list[Task] = []
        for pet in self.pets:
            tasks.extend(pet.tasks)
        return tasks

    def pet_count(self) -> int:
        """Return the number of pets the owner has."""

        return len(self.pets)


@dataclass(frozen=True)
class ScheduleItem:
    pet_name: str
    task_description: str
    planned_start: str
    planned_end: str
    note: str


class Scheduler:
    def __init__(self, workday_start: str = "06:00", workday_end: str = "22:00") -> None:
        """Set the scheduling window for the day."""

        self.workday_start = workday_start
        self.workday_end = workday_end

    def sort_by_time(self, tasks: Iterable[Task]) -> list[Task]:
        """Return tasks ordered by HH:MM time, then by priority and description."""

        return sorted(
            tasks,
            key=lambda task: (task.scheduled_time(), task.priority_rank(), task.description.lower()),
        )

    def _collect_pending_tasks(self, owner: Owner) -> list[tuple[Pet, Task]]:
        """Collect all unfinished tasks from the owner's pets."""

        collected: list[tuple[Pet, Task]] = []
        for pet in owner.pets:
            for task in pet.pending_tasks():
                collected.append((pet, task))
        return collected

    def filter_tasks(
        self,
        owner: Owner,
        pet_name: str | None = None,
        completed: bool | None = None,
        due_on_or_before: date | None = None,
    ) -> list[tuple[Pet, Task]]:
        """Filter tasks by pet name and/or completion status."""

        normalized_pet_name = pet_name.strip().lower() if pet_name else None
        filtered: list[tuple[Pet, Task]] = []

        for pet in owner.pets:
            if normalized_pet_name is not None and pet.name.lower() != normalized_pet_name:
                continue

            for task in pet.tasks:
                if completed is not None and task.completed != completed:
                    continue
                if due_on_or_before is not None and task.due_date > due_on_or_before:
                    continue
                filtered.append((pet, task))

        return filtered

    def detect_conflicts(self, owner: Owner) -> list[str]:
        """Return warning messages for tasks that share the same scheduled time."""

        conflicts: dict[str, list[str]] = {}
        for pet, task in self.filter_tasks(owner, completed=False, due_on_or_before=date.today()):
            conflicts.setdefault(task.time.strip(), []).append(f"{pet.name}: {task.description}")

        warnings: list[str] = []
        for time_text, descriptions in conflicts.items():
            if len(descriptions) > 1:
                warnings.append(
                    f"Warning: {len(descriptions)} tasks share {time_text}: "
                    + "; ".join(descriptions)
                )

        return warnings

    def build_daily_schedule(self, owner: Owner) -> list[ScheduleItem]:
        """Build a schedule ordered by time and priority."""

        pending = self.filter_tasks(owner, completed=False, due_on_or_before=date.today())
        pending.sort(
            key=lambda pair: (
                pair[1].scheduled_time(),
                pair[1].priority_rank(),
                pair[0].name.lower(),
                pair[1].description.lower(),
            )
        )

        current_time = _parse_clock(self.workday_start)
        end_of_day = _parse_clock(self.workday_end)
        schedule: list[ScheduleItem] = []

        for pet, task in pending:
            requested_start = task.scheduled_time()
            planned_start = max(current_time, requested_start)
            planned_end = _add_minutes(planned_start, task.duration_minutes)

            if planned_start >= end_of_day:
                continue

            if planned_end > end_of_day:
                continue

            if planned_start > requested_start:
                note = "moved later to avoid overlap with earlier tasks"
            elif task.priority_rank() == 0:
                note = "high priority"
            else:
                note = "scheduled as requested"

            schedule.append(
                ScheduleItem(
                    pet_name=pet.name,
                    task_description=task.description,
                    planned_start=_format_clock(planned_start),
                    planned_end=_format_clock(planned_end),
                    note=note,
                )
            )
            current_time = planned_end

        return schedule

    def format_schedule(self, items: Iterable[ScheduleItem]) -> str:
        """Format scheduled items for terminal or UI output."""

        lines = ["Today's Schedule"]
        for item in items:
            lines.append(
                f"{item.planned_start} - {item.planned_end} | "
                f"{item.pet_name}: {item.task_description} [{item.note}]"
            )
        if len(lines) == 1:
            lines.append("No tasks scheduled.")
        return "\n".join(lines)

    def format_task_list(self, tasks: Iterable[tuple[Pet, Task]]) -> str:
        """Format a filtered task list for terminal output."""

        lines = []
        for pet, task in tasks:
            status = "done" if task.completed else "open"
            lines.append(f"{task.time} | {pet.name}: {task.description} [{status}]")
        if not lines:
            return "No matching tasks."
        return "\n".join(lines)