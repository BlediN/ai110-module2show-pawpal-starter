from pawpal_system import Pet, Task


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