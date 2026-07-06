from datetime import date, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


def test_mark_complete_changes_status() -> None:
    task = Task("Feed dinner", "18:00", 10)

    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_adding_task_increases_pet_count() -> None:
    pet = Pet(name="Biscuit", species="dog")
    task = Task("Evening walk", "19:00", 25)

    assert pet.task_count() == 0

    pet.add_task(task)

    assert pet.task_count() == 1


def test_sort_by_time_orders_tasks() -> None:
    scheduler = Scheduler()
    tasks = [
        Task("Late walk", "19:00", 20),
        Task("Breakfast", "08:15", 10),
        Task("Morning walk", "07:30", 30),
    ]

    sorted_tasks = scheduler.sort_by_time(tasks)

    assert [task.description for task in sorted_tasks] == ["Morning walk", "Breakfast", "Late walk"]


def test_filter_tasks_by_pet_and_completion() -> None:
    scheduler = Scheduler()
    owner = Owner(name="Jordan")
    biscuit = Pet(name="Biscuit", species="dog")
    mittens = Pet(name="Mittens", species="cat")
    open_task = Task("Walk", "07:30", 20)
    done_task = Task("Food", "08:00", 10)
    done_task.mark_complete()

    biscuit.add_task(open_task)
    mittens.add_task(done_task)
    owner.add_pet(biscuit)
    owner.add_pet(mittens)

    filtered = scheduler.filter_tasks(owner, pet_name="Mittens", completed=True)

    assert filtered == [(mittens, done_task)]


def test_recurring_task_creates_next_occurrence() -> None:
    pet = Pet(name="Biscuit", species="dog")
    task = Task("Feed breakfast", "08:00", 10, frequency="daily")
    pet.add_task(task)

    next_task = pet.complete_task(task)

    assert task.completed is True
    assert next_task is not None
    assert next_task.due_date == date.today() + timedelta(days=1)
    assert next_task.completed is False
    assert pet.task_count() == 2


def test_detect_conflicts_reports_same_time_tasks() -> None:
    scheduler = Scheduler()
    owner = Owner(name="Jordan")
    biscuit = Pet(name="Biscuit", species="dog")
    mittens = Pet(name="Mittens", species="cat")
    biscuit.add_task(Task("Walk", "08:00", 20))
    mittens.add_task(Task("Medication", "08:00", 5))
    owner.add_pet(biscuit)
    owner.add_pet(mittens)

    warnings = scheduler.detect_conflicts(owner)

    assert warnings
    assert "08:00" in warnings[0]