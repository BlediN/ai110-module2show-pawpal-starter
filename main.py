from pawpal_system import Owner, Pet, Scheduler, Task


def build_demo_owner() -> Owner:
    """Create a sample owner with two pets and several tasks."""

    owner = Owner(name="Jordan")

    biscuit = Pet(name="Biscuit", species="dog", age=4)
    mittens = Pet(name="Mittens", species="cat", age=2)

    biscuit.add_task(Task("Evening walk", "19:00", 30, priority="medium", frequency="daily"))
    biscuit.add_task(Task("Morning walk", "07:30", 30, priority="high", frequency="daily"))
    biscuit.add_task(Task("Breakfast", "08:15", 10, priority="high", frequency="daily"))

    mittens.add_task(Task("Medication", "08:00", 5, priority="medium", frequency="daily"))
    mittens.add_task(Task("Playtime", "08:00", 20, priority="low", frequency="weekly"))

    owner.add_pet(biscuit)
    owner.add_pet(mittens)

    completed_task = biscuit.tasks[0]
    biscuit.complete_task(completed_task)
    return owner


def main() -> None:
    """Print a readable daily schedule for the demo data."""

    owner = build_demo_owner()
    scheduler = Scheduler()
    schedule = scheduler.build_daily_schedule(owner)

    print(f"PawPal+ demo for {owner.name}")
    print()

    print("Sorted Tasks")
    sorted_tasks = scheduler.sort_by_time(owner.get_all_tasks())
    for task in sorted_tasks:
        print(f"{task.time} | {task.description} ({task.frequency}, due {task.due_date.isoformat()})")

    print()
    print("Filtered Tasks for Biscuit")
    print(scheduler.format_task_list(scheduler.filter_tasks(owner, pet_name="Biscuit")))

    print()
    print("Conflict Warnings")
    warnings = scheduler.detect_conflicts(owner)
    if warnings:
        for warning in warnings:
            print(warning)
    else:
        print("No conflicts found.")

    print()
    print(scheduler.format_schedule(schedule))


if __name__ == "__main__":
    main()