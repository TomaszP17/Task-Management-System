#Author: Tomasz Pluciński
from datetime import datetime


#Errors:
class InvalidDateError(Exception):
    """Raised when the input value is not in correct range"""
    pass


class TaskNotFoundError(Exception):
    """Raised when the task is not found"""
    pass


class InvalidDeadlineError(Exception):
    """Raised when the deadline is not in correct format"""
    pass


#Classes:

#this class represent task model
class Task:
    def __init__(self, title, priority, deadline, category, description):
        self.title = title
        self.priority = priority
        self.deadline = deadline
        self.category = category
        self.description = description
        #new tasks are not done
        self.is_done = False
        #created date is a current date using datetime lib
        self.created_date = datetime.now().strftime('%d-%m-%Y')
        #at the beginning end_date is None cause task is not done
        self.end_date = None

    #print task
    def show_task(self):
        return f"{self.title} | {self.priority} | {self.deadline} | {self.category} | {self.description} | {self.is_done} | {self.created_date}"

    def mark_as_done(self):
        self.is_done = True
        self.end_date = datetime.now().strftime('%d-%m-%Y')


pass


#this class operate on tasks and do some methods on them
class TaskManager:
    def __init__(self):
        self.tasks = []

    #display all tasks in tasks list
    def show_tasks(self):
        for i, task in enumerate(self.tasks):
            print(f"{i}: {task.show_task()}")

    #add new one task into tasks list
    def add_task(self, task):
        self.tasks.append(task)

    #delete task on specific index id
    def delete_task(self, index):
        self.tasks.pop(index)


pass


#this class is responsible for work with files
class FileHandler:
    def __init__(self, file_name):
        self.file_name = file_name

    def save_to_file(self, tasks):
        with open(self.file_name, 'w') as file:
            for task in tasks:
                # for all tasks in list we change format by adding a comma between task values and write it into file
                #string format
                task_data = (f"{task.title},{task.priority},{task.deadline},{task.category},{task.description},"
                             f"{task.is_done},{task.created_date},{task.end_date}")
                file.write(task_data + '\n')

    def read_from_file(self):
        tasks = []
        try:
            with open(self.file_name, 'r') as file:
                for line in file:
                    #list of task values
                    parts = line.strip().split(',')
                    if len(parts) == 8:
                        title, priority, deadline, category, description, is_done, created_date, end_date = parts
                        task = Task(title, priority, deadline, category, description)
                        #check if is_done is True or False
                        task.is_done = is_done.strip() == 'True'
                        #add created date
                        task.created_date = created_date
                        #task.created_date = created_date.strip()
                        task.end_date = end_date
                        tasks.append(task)
                    else:
                        print("Invalid line")
        except FileNotFoundError:
            print("File not found. Starting with an empty task list.")
        return tasks


pass


def print_menu():
    print("---------------")
    print("MENU:")
    print("0. EXIT")
    print("1. Add new task")
    print("2. Delete task")
    print("3. Update task")
    print("4. Mark completed tasks")
    print("5. Display tasks")
    print("6. Display filtered tasks")
    print("7. Save updates into file")
    print("8. Generate stats about tasks")
    print("---------------")


def choose_priority():
    is_priority_chosen = False
    chosen_priority = ""
    while not is_priority_chosen:
        print("Pick priority for this task: ")
        print("1. Very Important")
        print("2. Important")
        print("3. Not Important")
        t_category = input("Enter a priority number: ")
        match t_category:
            case '1':
                chosen_priority = "Very Important"
                is_priority_chosen = True
            case '2':
                chosen_priority = "Important"
                is_priority_chosen = True
            case '3':
                chosen_priority = "Not Important"
                is_priority_chosen = True
            case _:
                print("You chose bad number of priority, try again!")
    return chosen_priority


def choose_category():
    is_category_chosen = False
    chosen_category = ""
    while not is_category_chosen:
        print("Pick category for this task: ")
        print("1. Job")
        print("2. Private")
        print("3. Hobby")
        t_category = input("Enter a category number: ")
        match t_category:
            case '1':
                chosen_category = "Job"
                is_category_chosen = True
            case '2':
                chosen_category = "Private"
                is_category_chosen = True
            case '3':
                chosen_category = "Hobby"
                is_category_chosen = True
            case _:
                print("You chose bad number of category, try again!")
    return chosen_category


def enter_deadline():
    is_deadline_correct = False

    while not is_deadline_correct:
        try:
            deadline = input("Enter a deadline in format DD-MM-YYYY: ")
            if len(deadline) == 10 and deadline[2] == '-' and deadline[5] == '-':
                day, month, year = deadline[0:2], deadline[3:5], deadline[6:10]
                if day.isnumeric() and month.isnumeric() and year.isnumeric():
                    if int(year) < datetime.now().year:
                        raise InvalidDeadlineError
                    if 1 <= int(day) <= 31 and 1 <= int(month) <= 12:
                        is_deadline_correct = True
                        return deadline
                    else:
                        raise InvalidDeadlineError
                else:
                    raise InvalidDeadlineError
            else:
                raise InvalidDeadlineError
        except InvalidDeadlineError:
            print("Invalid Deadline Error")


def add_new_task():
    t_title = input("Enter a task title: ")
    t_priority = choose_priority()
    t_deadline = enter_deadline()
    t_category = choose_category()
    t_description = input("Enter a task description: ")
    #is_done is stupid to input by user, i think if someone add new task its not done

    task = Task(t_title, t_priority, t_deadline, t_category, t_description)

    task_manager.add_task(task)


def delete_task():
    #user_input needs to be checked, because user could choose input out of range
    try:
        user_input = int(input("Enter a task index to delete: "))
        if user_input < 0 or user_input >= len(task_manager.tasks):
            raise InvalidDateError
        else:
            task_manager.delete_task(user_input)
            print("Task deleted successfully.")
    except InvalidDateError:
        print("Invalid Date Error:")


def update_task():
    if len(task_manager.tasks) == 0:
        print("You don't have any tasks!")
    else:
        print("Here are your tasks: ")
        task_manager.show_tasks()
        print("-------")
        try:
            chosen_index = int(input("Choose which task you want to update: "))
            if 0 <= chosen_index < len(task_manager.tasks):
                old_task = task_manager.tasks[chosen_index]
                print("Chosen task: ", old_task.show_task())
                print("What do you want to edit: ")
                print("1. Title")
                print("2. Priority")
                print("3. Deadline")
                print("4. Category")
                print("5. Description")

                try:
                    user_input = (int)(input("Enter your choice: "))
                    if user_input == 1:
                        new_title = input("Enter a new title: ")
                        old_task.title = new_title
                    elif user_input == 2:
                        new_priority = choose_priority()
                        old_task.priority = new_priority
                    elif user_input == 3:
                        new_deadline = enter_deadline()
                        old_task.deadline = new_deadline
                    elif user_input == 4:
                        new_category = choose_category()
                        old_task.category = new_category
                    elif user_input == 5:
                        new_description = input("Enter a new description: ")
                        old_task.description = new_description
                    else:
                        raise ValueError

                except ValueError:
                    print("You chose bad number :<")
            else:
                raise TaskNotFoundError
        except ValueError:
            print("Please enter a valid integer.")
        except TaskNotFoundError:
            print("There is no task with the provided index.")


#print all tasks
def show_tasks():
    print("Tasks list:")
    print("[Title, Priority, Deadline, Category, Description, Is done, Created date]")
    task_manager.show_tasks()


#change is_done to True if its not done
def mark_completed_task():
    chosen_task_id = (int)(input("Which task do you want to mark as Done"))
    #check if the id of chosen task is correct
    try:
        if 0 <= chosen_task_id < len(task_manager.tasks):
            if task_manager.tasks[chosen_task_id].is_done:
                print("You can't do that, because this task is already done!")
            else:
                #task_manager.tasks[chosen_task_id].is_done = True
                task_manager.tasks[chosen_task_id].mark_as_done()
                print("You've done this task, congratulations!")
        else:
            raise InvalidDateError
    except InvalidDateError:
        print("You chose bad index out of range")


def filter_tasks():
    #do filter on tasks and show it
    #only for these 3 elements
    print("---------")
    print("1. Priority")
    print("2. Deadline")
    print("3. Is_Done [status]")
    print("---------")
    chosen_filter = input("On which field you want to filter your tasks: ")
    match chosen_filter:
        case "1":
            #filter on priority
            typed_priority = input("Enter a searched priority: ").lower()
            searched_tasks = list(filter(lambda task: task.priority.lower() == typed_priority, task_manager.tasks))
            for task in searched_tasks:
                print(task.show_task())
        case "2":
            #filter on deadline
            typed_deadline = input("Enter a searched deadline: ").lower()
            searched_tasks = list(filter(lambda task: task.deadline.lower() == typed_deadline, task_manager.tasks))
            for task in searched_tasks:
                print(task.show_task())
        case "3":
            #filter on is_done
            typed_is_done = input("Enter a searched is_done [status]: ")
            # Convert the string to a boolean value
            typed_is_done = typed_is_done.lower() in ['true', '1']
            searched_tasks = list(filter(lambda task: task.is_done == typed_is_done, task_manager.tasks))
            for task in searched_tasks:
                print(task.show_task())
        case _:
            print("You chose bad option")


#Info about program [name, author, version]

print("<><><><><><><><><><><><><><><>")
print("Welcome in the Task Management System")
print("Created by: Tomasz Plucinski")
file_handler = FileHandler("tasks.txt")
task_manager = TaskManager()
task_manager.tasks = file_handler.read_from_file()
#Main menu
while True:
    print_menu()
    try:
        user_input = int(input("Enter your choice: "))
        print(user_input)

        match user_input:
            case 0:
                break
            case 1:
                add_new_task()
            case 2:
                delete_task()
            case 3:
                update_task()
            case 4:
                mark_completed_task()
            case 5:
                show_tasks()
            case 6:
                filter_tasks()
            case 7:
                file_handler.save_to_file(task_manager.tasks)
            case 8:
                print("Generating stats about tasks.")
                #how many tasks are done (percantage)
                counter_done = 0
                counter_not_done = 0
                for task in task_manager.tasks:
                    if task.is_done:
                        counter_done += 1
                print(f"Percentage of done tasks: {counter_done/len(task_manager.tasks) * 100}%")
                #avarage time for tasks
                sum_days = 0
                for task in task_manager.tasks:
                    if task.is_done:
                        created_date = datetime.strptime(task.created_date, '%d-%m-%Y')
                        end_date = datetime.strptime(task.end_date, '%d-%m-%Y')
                        sum_days += (end_date - created_date).days
                print(f"Avarage time for tasks: {sum_days / counter_done} days")

                #the most common priorities
                priorities = {}
                for task in task_manager.tasks:
                    if task.priority in priorities:
                        priorities[task.priority] += 1
                    else:
                        priorities[task.priority] = 1
                print("The most common priorities:", max(priorities, key=priorities.get))

            case _:
                print("Invalid choice, please enter a number from 1 to 8.")
    except ValueError:
        print("Please enter a valid integer.")
