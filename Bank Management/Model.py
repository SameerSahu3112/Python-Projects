class Employee:
    def __init__(self, employee_id, name, position, salary):
        self.employee_id = employee_id
        self.name = name
        self.position = position
        self.salary = salary

    def __str__(self):
        return f"Employee ID: {self.employee_id}, Name: {self.name}, Position: {self.position}, Salary: {self.salary}"
    