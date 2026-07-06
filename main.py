from pawpal_system import Owner, Pet, Scheduler, Task


def build_demo_owner() -> Owner:
    """Create a sample owner with two pets and several tasks."""

    owner = Owner(name="Jordan")

    biscuit = Pet(name="Biscuit", species="dog", age=4)
    mittens = Pet(name="Mittens", species="cat", age=2)

    biscuit.add_task(Task("Morning walk", "07:30", 30, priority="high", frequency="daily"))
    biscuit.add_task(Task("Breakfast", "08:15", 10, priority="high", frequency="daily"))
    mittens.add_task(Task("Medication", "08:00", 5, priority="medium", frequency="daily"))
    mittens.add_task(Task("Playtime", "09:00", 20, priority="low", frequency="daily"))

    owner.add_pet(biscuit)
    owner.add_pet(mittens)
    return owner


def main() -> None:
    """Print a readable daily schedule for the demo data."""

    owner = build_demo_owner()
    scheduler = Scheduler()
    schedule = scheduler.build_daily_schedule(owner)

    print(f"PawPal+ demo for {owner.name}")
    print(scheduler.format_schedule(schedule))


if __name__ == "__main__":
    main()