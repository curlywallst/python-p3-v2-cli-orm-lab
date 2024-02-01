from models.department import Department
from models.employee import Employee


def exit_program():
    print("Goodbye!")
    exit()

def list_departments():
    print_separator()
    print("Departments:")
    print("------------")
    print(" ")
    for i, department in enumerate(Department.get_all(), start=1):
        print(f'{i}. {department.name}')
    print_separator()


def find_department_by_name():
    name = input("Enter the department's name: ")
    department = Department.find_by_name(name)
    print(department) if department else print(
        f'Department {name} not found')

def select_department():
    list_departments()
    print(" ")
    print("Enter number of department from list above:")
    number = input("> ")
    try:
        department = Department.get_all()[int(number)-1]
        return department
    except Exception:
        print("No department found")

def list_department(department):
    print_separator()
    print(f'You have selected {department.name}!')
    print(f"It's location is {department.location}")
    print(' ')
    print(f"Employees of {department.name}:")
    print("------------")
    print(" ")
    for i, employee in enumerate(department.employees(), start=1):
        print(f'{i}. {employee.name}')
    print_separator()

def print_separator():
    print(' ')
    print("****************")
    print(' ')


def create_department():
    name = input("Enter the department's name: ")
    location = input("Enter the department's location: ")
    try:
        department = Department.create(name, location)
        print(f'Success: {department}')
    except Exception as exc:
        print("Error creating department: ", exc)


def update_department():
    id_ = input("Enter the department's id: ")
    if department := Department.find_by_id(id_):
        try:
            name = input("Enter the department's new name: ")
            department.name = name
            location = input("Enter the department's new location: ")
            department.location = location

            department.update()
            print(f'Success: {department}')
        except Exception as exc:
            print("Error updating department: ", exc)
    else:
        print(f'Department {id_} not found')


def delete_department():
    id_ = input("Enter the department's id: ")
    if department := Department.find_by_id(id_):
        department.delete()
        print(f'Department {id_} deleted')
    else:
        print(f'Department {id_} not found')


# You'll implement the employee functions in the lab

def list_employees():
    pass


def find_employee_by_name():
    pass


def find_employee_by_id():
    pass


def create_employee():
    pass


def update_employee():
    pass


def delete_employee():
    pass


