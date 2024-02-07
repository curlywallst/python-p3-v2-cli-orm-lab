
from helpers import (
    exit_program,
    list_departments,
    select_department,
    create_department,
    update_department,
    delete_department,
    list_department,
    # list_department_employees,
    select_employee,
    create_employee
    # update_employee,
    # delete_employee,

)

def main():
    print('')
    print('Welcome to the Department and Employee Management App')
    print('-- This app can be used by company management to keep track of departments and their employees')
    print('')
    main_menu_loop()

def main_menu_loop():
    list_departments()
    while True:
        departments_menu()
        choice = input("> ")
        if choice == "0":
            exit_program()
        elif choice == "1":
            list_departments()
        elif choice == "2":
            department_selections_loop()
        elif choice == "3":
            create_department()
        elif choice == "4":
            update_department()
        elif choice == "5":
            delete_department()
        else:
            print("Invalid choice")


def departments_menu():
    print(" ")
    print("Please select an option:")
    print(" ")
    print("0. Exit the program")
    print("1. List all departments")
    print("2. Select a department to see details")
    print("3: Create department")
    print("4: Update department")
    print("5: Delete department")

def department_selections_loop(department=None):
    if not department: department = select_department()
    list_department(department)
    while True:
        employees_menu(department)
        choice = input("> ")
        if choice == "0":
            exit_program()
        elif choice == "1":
            list_department(department)
        elif choice == "2":
            employee_selections_loop(department)
        elif choice == "3":
            create_employee(department)
        elif choice == "4":
            main_menu_loop()

def employees_menu(department): 
    print(" ")
    print("Please select an option:")
    print(" ")
    print("0. Exit the program")  
    print(f"1. List all employees of {department.name}")
    print(f"2. Select a {department.name} employee from the list above to see details")
    print(f"3. Add new employee to {department.name}")
    print(f"4: Go back to list of departments")

def employee_selections_loop(department):
    employee = select_employee(department)
    while True: 
        employee_menu()
        choice = input("> ")
        if choice == "0":
            exit_program()
        elif choice == "1":
            pass
            # update_employee(employee)
        elif choice == "2":
            pass
            # delete_employee(employee)
        elif choice == "3":
            department_selections_loop(employee.department())

def employee_menu(): 
    print(" ")
    print("Please select an option:")
    print(" ")
    print("0. Exit the program")  
    print(f"1. Update employee")
    print(f"2: Delete employee")
    print(f"3: Go back to list of employees")

if __name__ == "__main__":
    main()
