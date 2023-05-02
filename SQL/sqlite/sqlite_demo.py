import sqlite3
from employee import Employee

conn = sqlite3.connect('employee.db')
# conn = sqlite3.connect(':memory:') # in RAM

c = conn.cursor()

'''creating db'''
# c.execute("""CREATE TABLE employees (
#             first text,
#             last text,
#             pay integer
#             )""")

def insert_emp(emp):
    with conn:
        c.execute("INSERT INTO employees VALUES (:first, :last, :pay)",
                    {'first': emp.first, 'last': emp.last, 'pay': emp.pay})

def get_emps_by_name(lastname):
    c.execute("SELECT * FROM employees WHERE last=?", (lastname,))
    return c.fetchall()

def update_emp(emp, pay):
    with conn:
        c.execute("""UPDATE employees SET pay = :pay
                    WHERE first = :first AND last = :last""",
                    {'first': emp.first, 'last': emp.last, 'pay': pay})

def remove_emp(emp):
    with conn:
        c.execute("DELETE from employee WHERE first = :first AND last = :last",
                    {'first': emp.first, 'last': emp.last})


'''manually adding data'''
# c.execute("INSERT INTO employees VALUES ('mike', 'mikovich', 50_000)")
'''query db'''
# c.execute("SELECT * FROM employees WHERE last='mikovich'")
# print(c.fetchone())
# print(c.fetchmany(5))
# print(c.fetchall())
# """
'''adding data OOP'''
emp_1 = Employee('null-0', 'null', 80_000)
emp_2 = Employee('null-1', 'null', 90_000)

print(emp_1.first)
print(emp_1.last)
print(emp_1.pay)

# c.execute("INSERT INTO employees VALUES ('{}', '{}', {})".format(emp_1.first, emp_1.last, emp_1.pay)) # BAD PRACTICE vulnerable to sql-injections
c.execute("INSERT INTO employees VALUES (?, ?, ?)", (emp_1.first, emp_1.last, emp_1.pay))
c.execute("INSERT INTO employees VALUES (:first, :last, :pay)",
            {'first': emp_2.first, 'last': emp_2.last, 'pay': emp_2.pay})
# """

c.execute("SELECT * FROM employees WHERE last=?", ('mikovich',))
print(c.fetchall())
c.execute("SELECT * FROM employees WHERE last=:last", {'last': 'mikovich'})
print(c.fetchall())

conn.commit()

conn.close()
