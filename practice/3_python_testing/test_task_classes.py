"""
Write tests for classes in 2_python_part_2/task_classes.py (Homework, Teacher, Student).
Check if all methods working correctly.
Also check corner-cases, for example if homework number of days is negative.
"""
import pytest
import datetime
from unittest.mock import patch
import task_classes


# ------------------------------ FIXTURES --------------------------------------

@pytest.fixture(scope='function')
@patch(f'{task_classes.__name__}.datetime', wraps=datetime)
def homework(mocked_datetime_now, request):
    mocked_datetime_now.datetime.now.return_value = \
        datetime.datetime(2019, 5, 26, 16, 44, 30, 688762)
    return task_classes.Homework("create 2 simple classes", request.param)


@pytest.fixture
def teacher():
    return task_classes.Teacher('Nowak', 'Jan')


@pytest.fixture
def student():
    return task_classes.Student('Kowalska', 'Anna')


# ------------------------------ TESTING HOMEWORK ------------------------------

@pytest.mark.parametrize('homework, expected_days',
                         ([5, 5], [0, 0], [-5, -5], [1, 1]),
                         indirect=['homework'])
def test_homework_init(homework, expected_days):
    assert homework.text == 'create 2 simple classes'
    assert homework.created == datetime.datetime(2019, 5, 26, 16, 44, 30, 688762)
    assert homework.deadline == datetime.timedelta(days=expected_days)


@pytest.mark.parametrize('homework, active',
                         ([5, True], [0, False], [-5, False], [1, False]),
                         indirect=['homework'])
@patch(f'{task_classes.__name__}.datetime', wraps=datetime)
def test_homework_is_active(mocked_datetime_now, homework, active):
    mocked_datetime_now.datetime.now.return_value = \
        datetime.datetime(2019, 5, 28, 16, 44, 30, 688762)
    assert homework.is_active() is active


# ------------------------------ TESTING TEACHER -------------------------------


def test_teacher_init(teacher):
    assert teacher.first_name == 'Jan'
    assert teacher.last_name == 'Nowak'


@patch(f'{task_classes.__name__}.datetime', wraps=datetime)
def test_create_homework(mocked_datetime_now, teacher):
    mocked_datetime_now.datetime.now.return_value = \
        datetime.datetime(2019, 5, 26, 16, 44, 30, 688762)
    teachers_homework = teacher.create_homework('random task', 5)
    assert isinstance(teachers_homework, task_classes.Homework)
    assert teachers_homework.text == 'random task'
    assert teachers_homework.created == datetime.datetime(2019, 5, 26, 16, 44,
                                                          30, 688762)
    assert teachers_homework.deadline == datetime.timedelta(days=5)


# ------------------------------ TESTING STUDENT -------------------------------


def test_student_init(student):
    assert student.first_name == 'Anna'
    assert student.last_name == 'Kowalska'


@pytest.mark.parametrize('homework', (5,), indirect=['homework'])
@patch('task_classes.Homework.is_active', return_value=True)
def test_do_active_homework(mocked_active, homework, student):
    assert student.do_homework(homework) == homework


@pytest.mark.parametrize('homework', (5,), indirect=['homework'])
@patch('task_classes.Homework.is_active', return_value=False)
def test_do_expired_homework(mocked_active, homework, student, capfd):
    result = student.do_homework(homework)
    out, err = capfd.readouterr()
    assert result is None
    assert out == 'You are late\n'
