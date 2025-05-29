import json
from employee import Employee

EMPLOYEE_FILE = "data/employees.json"

def load_employees():
    """
    Loads employee data from the JSON file and returns a dictionary of Employee objects.
    If file doesn't exist or is invalid, returns an empty dict.
    """
    try:
        with open(EMPLOYEE_FILE, "r") as f:
            data = json.load(f)
            employees = {}
            for name, emp_data in data.get("employees", {}).items():
                employees[name] = Employee.from_dict(name, emp_data)
            return employees
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_employees(employees):
    """
    Saves the employee dictionary (of Employee objects) to the JSON file.
    """
    data = {
        "employees": {name: emp.to_dict() for name, emp in employees.items()}
    }
    with open(EMPLOYEE_FILE, "w") as f:
        json.dump(data, f, indent=2)

def add_employee(employees, employee):
    """
    Adds a new employee to the dictionary and saves.
    """
    employees[employee.name] = employee
    save_employees(employees)

def remove_employee(employees, name):
    """
    Removes an employee by name and saves.
    """
    if name in employees:
        del employees[name]
        save_employees(employees)
        return True
    return False

def get_employee(employees, name):
    """
    Gets an Employee object by name, or None if not found.
    """
    return employees.get(name)

def update_employee(employees, employee):
    """
    Updates an existing employee's data and saves.
    """
    employees[employee.name] = employee
    save_employees(employees)