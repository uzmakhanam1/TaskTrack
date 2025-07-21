class CleanupTask:
    def __init__(self, task_id, description, status, duration, assigned_team):
        self.task_id = task_id
        self.description = description
        self.status = status
        self.duration = duration
        self.assigned_team = assigned_team

    def display_task_details(self):
        print(f"Task ID: {self.task_id}, Description: {self.description}, Status: {self.status}, Duration: {self.duration}, Assigned Team: {self.assigned_team}")


class CleanupCoordinator:
    def __init__(self):
        self.tasks = []
        self.file_path = "tasks.txt"  # File to store tasks

    def load_tasks_from_file(self):
        try:
            with open(self.file_path, "r") as file:
                for line in file:
                    if line.startswith("Team ID") or line.strip() == "":
                        continue
                    task_data = line.strip().split(',')
                    if len(task_data) == 5:
                        task = CleanupTask(*task_data)
                        self.tasks.append(task)
            print("Tasks loaded successfully.")
        except FileNotFoundError:
            print("No tasks file found. Starting with an empty task list.")

    def save_tasks_to_file(self):
        tasks_by_team = {}
        for task in self.tasks:
            if task.assigned_team not in tasks_by_team:
                tasks_by_team[task.assigned_team] = []
            tasks_by_team[task.assigned_team].append(task)

        with open(self.file_path, "w") as file:
            for team, team_tasks in tasks_by_team.items():
                file.write(f"Team ID: {team}\n")
                for task in team_tasks:
                    file.write(f"{task.task_id},{task.description},{task.status},{task.duration},{task.assigned_team}\n")
                file.write("\n")
        print("Tasks saved successfully.")

    def add_task(self, task):
        if any(t.task_id == task.task_id for t in self.tasks):
            print("Task with ID", task.task_id, "already exists.")
        else:
            self.tasks.append(task)
            self.save_tasks_to_file()
            print("Task added successfully.")

    def update_task_details(self, task_id, new_description, new_duration, new_assigned_team):
        task_found = False
        for task in self.tasks:
            if task.task_id == task_id:
                task.description = new_description
                task.duration = new_duration
                task.assigned_team = new_assigned_team
                task_found = True
                self.save_tasks_to_file()
                print("Task details updated successfully.")
                break
        if not task_found:
            print("Task with ID", task_id, "does not exist.")

    def update_task_status(self, task_id, new_status):
        task_found = False
        for task in self.tasks:
            if task.task_id == task_id:
                task.status = new_status
                task_found = True
                self.save_tasks_to_file()
                print("Task status updated successfully.")
                break
        if not task_found:
            print("Task with ID", task_id, "does not exist.")

    def remove_task(self, task_id):
        for task in self.tasks:
            if task.task_id == task_id:
                self.tasks.remove(task)
                self.save_tasks_to_file()
                print("Task removed successfully.")
                return
        print("Task with ID", task_id, "does not exist.")

    def list_tasks(self):
        if not self.tasks:
            print("No tasks available.")
        else:
            for task in self.tasks:
                task.display_task_details()

    def plan_cleanup(self, assigned_team):
        if not any(task.assigned_team == assigned_team for task in self.tasks):
            print(f"Team '{assigned_team}' doesn't exist.")
            return

        total_duration = sum(int(task.duration) for task in self.tasks if task.assigned_team == assigned_team)
        print(f"Total duration planned for {assigned_team}: {total_duration} hours.")

    def track_efficiency(self):
        teams = set(task.assigned_team for task in self.tasks)

        for team in teams:
            completed_tasks = [task for task in self.tasks if task.status == "Completed" and task.assigned_team == team]
            pending_tasks = [task for task in self.tasks if task.status != "Completed" and task.assigned_team == team]

            completed_duration = sum(int(task.duration) for task in completed_tasks)
            pending_duration = sum(int(task.duration) for task in pending_tasks)

            print(f"Team: {team}")
            print(f"Total duration of completed tasks: {completed_duration} hours.")
            print(f"Total duration of pending tasks: {pending_duration} hours.")


def main():
    coordinator = CleanupCoordinator()
    coordinator.load_tasks_from_file()

    while True:
        print("\nMenu:")
        print("1. Add Task")
        print("2. Update Task")
        print("3. Remove Task")
        print("4. List Tasks")
        print("5. Plan Cleanup for Team")
        print("6. Track Efficiency")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            task_id = input("Enter Task ID: ")
            if any(task_id == task.task_id for task in coordinator.tasks):
                print("Task with ID", task_id, "already exists.")
            else:
                description = input("Enter Description: ")
                status = input("Enter Status: ")
                duration = input("Enter Duration: ")
                assigned_team = input("Enter Assigned Team: ")
                task = CleanupTask(task_id, description, status, duration, assigned_team)
                coordinator.add_task(task)

        elif choice == '2':
            print("Select an option:")
            print("1. Update Task Details")
            print("2. Update Task Status")
            update_option = input("Enter your choice: ")
            if update_option == '1':
                task_id = input("Enter Task ID to update: ")
                new_description = input("Enter New Description: ")
                new_duration = input("Enter New Duration: ")
                new_assigned_team = input("Enter New Assigned Team: ")
                coordinator.update_task_details(task_id, new_description, new_duration, new_assigned_team)
            elif update_option == '2':
                task_id = input("Enter Task ID to update: ")
                new_status = input("Enter New Status: ")
                coordinator.update_task_status(task_id, new_status)
            else:
                print("Invalid option.")

        elif choice == '3':
            task_id = input("Enter Task ID to remove: ")
            coordinator.remove_task(task_id)

        elif choice == '4':
            coordinator.list_tasks()

        elif choice == '5':
            assigned_team = input("Enter Team to plan cleanup for: ")
            coordinator.plan_cleanup(assigned_team)

        elif choice == '6':
            coordinator.track_efficiency()

        elif choice == '7':
            coordinator.save_tasks_to_file()
            print("Exiting program.")
            break

        else:
            print("Invalid choice. Please enter a number from 1 to 7.")


if __name__ == "__main__":
    main()

