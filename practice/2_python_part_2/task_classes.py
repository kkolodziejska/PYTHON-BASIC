"""
Create 3 classes with interconnection between them (Student, Teacher,
Homework)
Use datetime module for working with date/time
1. Homework takes 2 attributes for __init__: tasks text and number of days to complete
Attributes:
    text - task text
    deadline - datetime.timedelta object with date until task should be completed
    created - datetime.datetime object when the task was created
Methods:
    is_active - check if task already closed
2. Student
Attributes:
    last_name
    first_name
Methods:
    do_homework - request Homework object and returns it,
    if Homework is expired, prints 'You are late' and returns None
3. Teacher
Attributes:
     last_name
     first_name
Methods:
    create_homework - request task text and number of days to complete, returns Homework object
    Note that this method doesn't need object itself
PEP8 comply strictly.
"""
import datetime
from typing import Union


class Homework:
    """
    A class used to represent homework.

    Attributes:
        text (str): description of homework
        deadline (datetime.timedelta): specifies when task should be completed
        created (datetime.datetime): specifies when task was created

    Methods:
        is_active(): checks if task already closed
    """

    def __init__(self, task_text: str, days_to_complete: int) -> None:
        self.text = task_text
        self.deadline = datetime.timedelta(days=days_to_complete)
        self.created = datetime.datetime.now()

    def is_active(self) -> bool:
        """Check if task already closed."""
        print(self.created + self.deadline)
        return self.created + self.deadline >= datetime.datetime.now()


class Teacher:
    """
    A class used to represent teacher.

    Attributes:
        last_name (str): teacher's last name
        first_name (str): teacher's first name

    Methods:
        create_homework(task_text, days_to_complete): creates homework
    """

    def __init__(self, last_name: str, first_name: str) -> None:
        self.last_name = last_name
        self.first_name = first_name

    @staticmethod
    def create_homework(task_text: str, days_to_complete: int) -> Homework:
        """Creates homework.

        :param task_text: task description
        :param days_to_complete: days to complete a task
        :return: Homework object
        """
        return Homework(task_text, days_to_complete)


class Student:
    """
    A class used to represent student.

    Attributes:
        last_name (str): student's last name
        first_name (str): student's first name

    Methods:
        do_homework(homework): returns homework or None if homework expired
    """

    def __init__(self, last_name: str, first_name: str) -> None:
        self.last_name = last_name
        self.first_name = first_name

    @staticmethod
    def do_homework(homework: Homework) -> Union[Homework, None]:
        """request Homework object and returns it,
        if Homework is expired, prints 'You are late' and returns None

        :param homework: Homework object to complete
        :return: Homework object or None, if homework expired
        """
        if homework.is_active():
            return homework
        else:
            print("You are late")
            return None


if __name__ == '__main__':
    teacher = Teacher('Dmitry', 'Orlyakov')
    student = Student('Vladislav', 'Popov')
    print(teacher.last_name)  # Daniil
    print(student.first_name)  # Petrov

    expired_homework = teacher.create_homework('Learn functions', 0)
    print(expired_homework.created)  # Example: 2019-05-26 16:44:30.688762
    print(expired_homework.deadline)  # 0:00:00
    print(expired_homework.text)  # 'Learn functions'

    # create function from method and use it
    create_homework_too = teacher.create_homework
    oop_homework = create_homework_too('create 2 simple classes', 5)
    print(oop_homework.deadline)  # 5 days, 0:00:00

    student.do_homework(oop_homework)
    student.do_homework(expired_homework)  # You are late
