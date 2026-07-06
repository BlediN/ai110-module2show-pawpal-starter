import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")
st.caption("CLI-first backend demo connected to a simple Streamlit UI.")


def get_owner() -> Owner:
    """Return the session owner, creating one if needed."""

    if "owner" not in st.session_state:
        st.session_state.owner = Owner(name="Jordan")
    return st.session_state.owner


def add_demo_data() -> None:
    """Seed the app with sample data for quick exploration."""

    owner = get_owner()
    if owner.pet_count() == 0:
        biscuit = Pet(name="Biscuit", species="dog", age=4)
        mittens = Pet(name="Mittens", species="cat", age=2)
        biscuit.add_task(Task("Morning walk", "07:30", 30, priority="high", frequency="daily"))
        biscuit.add_task(Task("Breakfast", "08:15", 10, priority="high", frequency="daily"))
        mittens.add_task(Task("Medication", "08:00", 5, priority="medium", frequency="daily"))
        owner.add_pet(biscuit)
        owner.add_pet(mittens)


add_demo_data()
owner = get_owner()
scheduler = Scheduler()

with st.expander("System overview", expanded=True):
    st.markdown(
        """
PawPal+ keeps pet care tasks organized by:
- storing owners, pets, and tasks as objects
- sorting tasks by time and priority
- shifting tasks later when earlier items run long
        """
    )

st.subheader("Owner")
owner.name = st.text_input("Owner name", value=owner.name)

st.subheader("Add Pet")
pet_name = st.text_input("Pet name", value="Mochi")
pet_species = st.selectbox("Species", ["dog", "cat", "other"])
pet_age = st.number_input("Age", min_value=0, max_value=40, value=3, step=1)

if st.button("Add pet"):
    owner.add_pet(Pet(name=pet_name, species=pet_species, age=int(pet_age)))
    st.success(f"Added {pet_name}.")

st.subheader("Add Task")
pet_options = [pet.name for pet in owner.pets] or [pet_name]
selected_pet_name = st.selectbox("Assign to pet", pet_options)
task_description = st.text_input("Task description", value="Evening walk")
task_time = st.text_input("Time (HH:MM)", value="18:00")
task_duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
task_priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
task_frequency = st.selectbox("Frequency", ["once", "daily", "weekly"], index=1)

if st.button("Add task"):
    selected_pet = owner.get_pet(selected_pet_name)
    if selected_pet is None:
        st.error("Select a valid pet before adding a task.")
    else:
        selected_pet.add_task(
            Task(
                description=task_description,
                time=task_time,
                duration_minutes=int(task_duration),
                priority=task_priority,
                frequency=task_frequency,
            )
        )
        st.success(f"Added task for {selected_pet.name}.")

st.subheader("Current Tasks")
task_rows = []
for pet in owner.pets:
    for task in pet.tasks:
        task_rows.append(
            {
                "pet": pet.name,
                "description": task.description,
                "time": task.time,
                "duration": task.duration_minutes,
                "priority": task.priority,
                "completed": task.completed,
            }
        )

if task_rows:
    st.dataframe(task_rows, width="stretch", hide_index=True)
else:
    st.info("No tasks yet.")

st.subheader("Today's Schedule")
if st.button("Generate schedule"):
    schedule = scheduler.build_daily_schedule(owner)
    st.text(scheduler.format_schedule(schedule))
else:
    st.caption("Click Generate schedule to see the ordered plan.")
