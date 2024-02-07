# CLI Lab

## Learning Goals

- Implement a **client facing** CLI for an ORM application

---

## Instructions

This is **not** a test-driven lab. You will test your code using a command line
interface (CLI).

Run `pipenv install` to create your virtual environment and `pipenv shell` to
enter the virtual environment.

In the previous lesson we created a command line interface to the company ORM application that could be used by a developer for testing of their ORM methods.  For this lab, we will reimagine our CLI to be used by the manager of a company (not a developer) to keep track of departments and their employees.  

The models represent the backend of our application, while the cli and its helpers represent the client facing frontend.

The formatting and client flow through the application is where your creativity can be shown!  Think about what the user would want to see, how it should be laid out and the ease of use!

<!-- We'll continue to add a command line interface to the company ORM application
from the previous lesson:

![company erd](https://curriculum-content.s3.amazonaws.com/7134/python-p3-v2-orm/department_employee_erd.png) -->

The directory structure remains as follows:

```console
.
└── lib
    ├── models
        ├── __init__.py
        ├── department.py
    │   └── employee.py
    ├── testing
        ├── conftest.py
        ├── department_orm_test.py
        ├── department_property_test.py
        ├── employee_orm_test.py
    │   └── employee_property_test.py
    ├── cli.py
    ├── company.db
    ├── debug.py
    ├── helpers.py
    └── seed.py
├── Pipfile
├── Pipfile.lock
├── pytest.ini
├── README.md
```

### Seeding the database with sample data

The file `lib/seed.py` contains code to initialize the database with sample
departments and employees. Run the following command to seed the database:

```bash
python lib/seed.py
```

You can use the SQLITE EXPLORER extension to explore the initial database
contents. (Another alternative is to run `python lib/debug.py` and use the
`ipbd` session to explore the database)

In this lab we will consider the **user experience**.  We will create a CLI for a user that is not a developer testing ORM methods as was the case in the previous code along.  We want to show the user data in a way that a non-developer would expect and think about the ease of use from the user's point of view.  Here we will not show users objects returned from the __repr__ method, but take the objects returned from the ORM methods in the backend and format them in the frontend, much like react receives json from the backend and formats it for the user view.  We need to think about who the user is and how they will use our app.  

For this lab we have imagined the user to be a company manager who is tasked with creating and managing company departments and their repective employees.

The manager is presented with the list of all the departments and given the option to see the list again, see the details of one department, create a department, delete a department, update a department or exit the app.

We will still use helper functions to call ORM methods in the `Employee` and `Department`
classes.

Let's explore a few differences in this newly imagined app from the previous code along lesson:

---

### `cli.py` and `helpers.py`

The file `lib/cli.py` contains a command line interface outline for our client facing company database
application. The CLI displays a menu of commands for the user to select from.

Upon startup, our **main()** method prints a greeting and calls the **main_menu_loop()**.  Here the user will be shown the possible choices and prompted to pick one.  As always, we must check the user input and give an error message with a chance to pick again if they enter an invalid choice!  Don't forget to stress test as you build to make sure an invalid choice does not cause your app to error out.

```
def main():
    print('')
    print('Welcome to the Department and Employee Management App')
    print('-- This app can be used by company management to keep track of departments and their employees')
    print('')
    main_menu_loop()

def main_menu_loop():
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
```

Run `python lib/cli.py` to see the starting menus.  Now the user is greeted upon startup and given department related choices as shown below:

```bash

Welcome to the Department and Employee Management App
-- This app can be used by company management to keep track of departments and their employees

Please select an option:

0. Exit the program
1. List all departments
2. Select a department to see details
3: Create department
4: Update department
5: Delete department
```

### `list_departments()`

As before, the `list_departments()` function in `lib/helpers.py` should get all departments stored in the database, then print each department on a new line.  But now, we will format this data as we print it to be shown to a non-developer.  We will number the list numerically, rather than exposing the database id to the user and format it in a more readable way as shown in the code below:

```py
def list_departments():
    print_separator()
    print("Departments:")
    print("------------")
    print(" ")
    for i, department in enumerate(Department.get_all(), start=1):
        print(f'{i}. {department.name}')
    print_separator()
```

`print_separator()` is a simple formatting method that prints a blank line, a line of asterisks and another blank line. This function was created just to keep our code DRY

Test the list_departments method by selecting option `1` when you run `python lib/cli.py`:

```bash

****************
 
Departments:
------------
 
1. Payroll
2. Human Resources
 
****************
 
 
Please select an option:
 
0. Exit the program
1. List all departments
2. Select a department to see details
3: Create department
4: Update department
5: Delete department
```

Now even if a department has been deleted, the numbers will be in numeric order starting from 1.  They now represent the **relative position** in the list of all departments.  If the user wants to see the details of the Payroll department they will pick 1 (which is index postion 0 in the list of all departments currently in the database and returned by our get_all ORM method in the Department model).

At this point, when a user is looking at a numbered list of all departments, they will want the ability exit the app, to see one department, or to add, update or delete a department.  In our cli.py we have called this the **departments_menu**. 

```py
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
```

If the user chooses to see the details of a single department they pick 2.  This sends us to another looping function, the `department_selection_loop` that will let the user choose a department, see the details of the chosen department and be presented with a different set of options relevant to one chosen department.

### `department_selections_loop()`

```py
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
```

Firstly the method `select_department()` prompts the user to pick a department from the list generated by list_departments and prints the information for that department (including a list of employees of the selected department), or print an error message if the department does not exist.  If the department does exist it is returned and stored in a variable `department` which is passed to the `list_department` function to print out the details of the chosen department **including its employees**.

```py
def select_department():
    while True:
        list_departments()
        print(" ")
        print("Enter number of department from list above:")
        number = input("> ")
        try:
            department = Department.get_all()[int(number)-1]
            return department
        except Exception:
            print("That number is not valid - please try again")
```

For example, if the user selects the department which is numbered 1 in the list of all departments (in our example 1 is the Payroll Department), we know it is the 1st department in the list of all departments returned by the ORM method get_all.  To access the 1st department we need to use index of 0 to retrieve the correct department object from the list of all department objects.  If the user wants the 2nd department it would be index 1 in the list, and so forth.  Department.get_all() returns the list and Department.get_all()[int(number)-1] retrieves the proper department object from the list of objects to display.  The chosen department is passed to the `list_department` function to print out the details of the chosen deparment **including its employees**.


### `list_department()`

```py
def list_department(department):
    print_separator()
    print(f'You have selected {department.name}!')
    print(f"It's location is {department.location}")
    list_department_employees(department)
```

In list department, after we print the details of the selected department, we call the `list_department_employees` function to print the employees for that department.

```py

def list_department_employees(department):
    print_separator()
    print(f"Employees of {department.name}:")
    print("------------")
    print(" ")
    for i, employee in enumerate(department.employees(), start=1):
        print(f'{i}. {employee.name}')
    print_separator()
```

Now we see the Payroll Department, its location and its employees.  Thinking about what a user would want to do at this point, they would want the ability to see the employees of the Payroll Department again, select one employee to see their details, add a new employee to the Payroll Department or return to the main_menu_loop.  There is no need, when adding an employee, to ask the user which department to add them to - we know we are talking about the Payroll Department!  This menu is printed by the `employees_menu`


```py
def employees_menu(department): 
    print(" ")
    print("Please select an option:")
    print(" ")
    print("0. Exit the program")  
    print(f"1. List all employees of {department.name}")
    print(f"2. Select a {department.name} employee from the list above to see details")
    print(f"3. Add new employee to {department.name}")
    print(f"4: Go back to list of departments")```

```

Test the code by selecting `1` from the list of all departments (after having chosen `2` in the main_menu to select a department to see its details).  You will see the following:

```
 
****************
 
You have selected Payroll!
It's location is Building A, 5th Floor
 
Employees of Payroll:
------------
 
1. Amir
2. Bola
 
****************
 
 
Please select an option:
 
0. Exit the program
1. List all employees of Payroll
2. Select a Payroll employee from the list above to see details
3. Add new employee to Payroll
4: Go back to list of departments
> 
```

Now if the user wants to add an employee, we know they want to add an employee to THIS department.  We do not need to prompt the user for the department.  We have used string interpolation in the employees_menu() to clarify this for the user.

### `create_employee()`

The function `create_employee()` should:

1. Prompt for and read in a name, job title, and department id.
2. Create and persist a new `Employee` class instance, surrounding the code in a
   `try/except` block in case an exception is thrown by the `name`, `job_title`,
   or `department_id` property setter methods.
3. Print a message indicating that the `Employee` object was successfully
   created, or print an error message if an exception is thrown.

When the user picks `3` in the `department_selections_loop()`, the create_employee function is called, passing along the selected department.

```py
def create_employee(department):
    name = input("Employee name:  ")
    title = input("Job Title:  ")
    Employee.create(name, title, department.id)
    list_department_employees(department)
```

Test the function by selecting option `3` in the `department_selections_loop()`.  After adding a new employee to the given department, we call `list_department_employees` to rerender the list of the chosen department's employees that now includes the new employee.

Next, if we want to see the details of an existing employee in the selected department we select 2, "Select a Payroll employee from the list above to see details".  






















Try entering a name that exists in the database:

```bash
> 8
Enter the employee's name: Dani
<Employee 4: Dani, Benefits Coordinator, Department ID: 2>
```

Try entering a name not in the database:

```bash
> 8
Enter the employee's name: Fred
Employee Fred not found
```



Test the function by selecting option `10` when you run `python lib/cli.py`.

```bash
> 10
Enter the employee's name: Ira
Enter the employee's job title: Manager
Enter the employee's department id:1
Success: <Employee 6: Ira, Manager, Department ID: 1>
```

Confirm the employee was added to the database by selecting option `7` to list
all employees:

```bash
> 7
<Employee 1: Amir, Accountant, Department ID: 1>
<Employee 2: Bola, Manager, Department ID: 1>
<Employee 3: Charlie, Manager, Department ID: 2>
<Employee 4: Dani, Benefits Coordinator, Department ID: 2>
<Employee 5: Hao, New Hires Coordinator, Department ID: 2>
<Employee 6: Ira, Manager, Department ID: 1>
```

Try entering invalid data for name or job title:

```bash
> 10
Enter the employee's name:
Enter the employee's job title: Programmer
Enter the employee's department id: 1
Error creating employee:  Name must be a non-empty string
```

Try entering an invalid department id:

```bash
> 10
Enter the employee's name: Jani
Enter the employee's job title: Accountant
Enter the employee's department id:99
Error creating employee:  department_id must reference a department in the database
```

### `update_employee()`

The function `update_employee()` should:

1. Prompt for and read in the employee id.
2. Print an error message if the employee is not in the database. If the
   employee is in the database, attempt to do the following steps within a
   `try-except` block to catch any exceptions, printing an error message if an
   exception is thrown.
3. Prompt for a new name to update the `name` attribute (property setter may
   throw an exception).
4. Prompt for a new job title to update the `job_title` attribute (property
   setter may throw an exception).
5. Prompt for the employee's new department id to update the `department_id`
   attribute (property setter may throw an exception).
6. Update the employee in the database.
7. Print a success message after a successful update, or print an appropriate
   error message if an exception is thrown.

Test the function by selecting option `11` when you run `python lib/cli.py`.

```bash
> 11
Enter the employee's id: 3
Enter the employees's new name: Charles
Enter the employee's new job title:Director
Enter the employees's new department id: 1
Success: <Employee 3: Charles, Director, Department ID: 1>
```

Confirm the database was updated by listing all employees:

```bash
> 7
<Employee 1: Amir, Accountant, Department ID: 1>
<Employee 2: Bola, Manager, Department ID: 1>
<Employee 3: Charles, Director, Department ID: 1>
<Employee 4: Dani, Benefits Coordinator, Department ID: 2>
<Employee 5: Hao, New Hires Coordinator, Department ID: 2>
<Employee 6: Ira, Manager, Department ID: 1>
```

Try entering an invalid employee id:

```bash
> 11
Enter the employee's id: 99
Employee 99 not found
```

Try entering an invalid name:

```bash
> 11
Enter the employee's id: 4
Enter the employees's new name:
Error updating employee:  name must be a non-empty string
```

Try entering an invalid job title:

```bash
> 11
Enter the employee's id: 4
Enter the employees's new name: Danielle
Enter the employee's new job title:
Error updating employee:  job_title must be a non-empty string
```

Try entering an invalid department id:

```bash
> 11
Enter the employee's id: 4
Enter the employees's new name: Danielle
Enter the employee's new job title:Senior Benefits Coordinator
Enter the employees's new department id: 99
Error updating employee:  department_id must reference a department in the database
```

### `delete_employee()`

The function `delete_employee()` should prompt for the employee `id` and delete
the employee from the database if it exists and print a confirmation message, or
print an error message if the employee is not in the database.

Test the function by selecting option `12` when you run `python lib/cli.py`.

```bash
> 12
Enter the employee's id: 1
Employee 1 deleted
```

Confirm the employee was deleted by listing all employees:

```bash
> 7
<Employee 2: Bola, Manager, Department ID: 1>
<Employee 3: Charles, Director, Department ID: 1>
<Employee 4: Dani, Benefits Coordinator, Department ID: 2>
<Employee 5: Hao, New Hires Coordinator, Department ID: 2>
<Employee 6: Ira, Manager, Department ID: 1>
```

Try entering a non-existent employee id:

```bash
> 12
Enter the employee's id: 99
Employee 99 not found

```

### `list_department_employees()`

You may want to reseed the database to get the same output.

The function `list_department_employees()` should:

1. prompt for a department id.
2. find the department with that id from the database.
3. if the department exists in the database, get the department's employees
   (HINT: call the `employees()` instance method) and loop to print each
   employee's data on a separate line.
4. if the department does not exist in the database, print an error message.

Test the function by selecting option `13` when you run `python lib/cli.py`.

```bash
> 13
Enter the department's id: 1
<Employee 1: Amir, Accountant, Department ID: 1>
<Employee 2: Bola, Manager, Department ID: 1>
```

```bash
> 13
Enter the department's id: 2
<Employee 3: Charlie, Manager, Department ID: 2>
<Employee 4: Dani, Benefits Coordinator, Department ID: 2>
<Employee 5: Hao, New Hires Coordinator, Department ID: 2>
```

Try an id that does not match an existing department:

```bash
> 13
Enter the department's id: 99
Department 99 not found
```

---

Success! Use git to push and submit your lab to Canvas.

---
