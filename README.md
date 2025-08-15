# Laboratory Database Project

This project is a Laboratory Management System developed for SJSU CMPE 138 (Fall 2021, Team 12). It provides a command-line interface for managing laboratory equipment, personnel, and experiment assignments using a MySQL database.

## Features

- Role-based actions for Lab Associates, Principal Investigators, Research Scientists, and Test Subjects
- Equipment monitoring and maintenance tracking
- Experiment assignment and management
- SQL scripts for database initialization and population
- Modular Python code for database operations

## Project Structure

```
admin.py                  # Admin role actions
lab_associate.py          # Lab Associate role actions
principal_investigator.py # Principal Investigator role actions
research_scientist.py     # Research Scientist role actions
test_subject.py           # Test Subject role actions
main.py                   # Entry point for the CLI application
utils.py                  # Utility functions for DB operations
proj_init.sql             # SQL script to initialize the database schema
proj_populate.sql         # SQL script to populate the database with sample data
requirements.txt          # Python dependencies
db.log                    # Log file for database operations
```

## Lab Associate Role Example

The `lab_associate.py` file contains functions for Lab Associates, such as:

- Viewing monitored equipment by different filters (all, others, logged-in user)
- Signing up to monitor equipment
- Viewing maintained equipment
- Viewing current and past equipment allocations

Example function:
```python
def view_equipment_by_monitor(cursor, user):
    options = """View monitored equipment for:
1. All
2. Others
3. Logged in user
4. Exit
"""
    query = """select emp_lname as 'Last Name', emp_id as 'Employee ID', equ_name as 'Equipment' \
                from (assigned_to JOIN employee as emp on monitor_id = emp_id) \
                JOIN equipment on assigned_to.equ_id = equipment.equ_id """
    # ...existing code...
```

## Setup Instructions

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/Laboratory-DBproject.git
   cd Laboratory-DBproject
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Set up the MySQL database:**
   - Run `proj_init.sql` to create the schema.
   - Run `proj_populate.sql` to insert sample data.

4. **Configure database connection:**
   - Update connection details in `utils.py` as needed.

5. **Run the application:**
   ```sh
   python main.py
   ```

## Usage

- Select your role and follow the prompts to perform actions such as viewing equipment, signing up for monitoring, and managing experiments.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is for educational purposes.
