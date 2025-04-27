# DegreeRequirement

**DegreeRequirement** is a Python-based application designed to assist students and academic advisors in tracking and managing degree requirements. By leveraging a structured database and intuitive interfaces, it ensures that users can monitor academic progress efficiently.

## Features

- **Structured Database**: Utilizes SQLite to store and manage course and degree requirement data.
- **Modular Design**: Organized into distinct modules for database operations, routing, and schema definitions.
- **Sample Data**: Includes sample datasets to demonstrate functionality and provide a starting point for users.

## Project Structure

```
DegreeRequirement/
├── Db/
│   └── Database.db       # SQLite database file
├── Router/
│   └── main.py           # Main application logic and routing
├── Sample/
│   └── sample_data.py    # Scripts to populate the database with sample data
├── Schema/
│   └── schema.sql        # SQL schema definitions for the database
├── operation/
│   └── operations.py     # Database operation functions
└── README.md             # Project documentation
```

## Getting Started

### Prerequisites

- Python 3.x installed on your system
- `pip` package manager

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/xhpmoonx/DegreeRequirement.git
   cd DegreeRequirement
   ```

2. **Create a virtual environment (optional but recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install required packages:**

   *(Note: As of now, there are no external dependencies. If future updates include dependencies, they will be listed here.)*

4. **Set up the database:**

   - Navigate to the `Db/` directory.
   - Ensure `Database.db` exists. If not, create it using the provided `schema.sql`:

     ```bash
     sqlite3 Database.db < ../Schema/schema.sql
     ```

5. **Populate the database with sample data (optional):**

   ```bash
   python Sample/sample_data.py
   ```

6. **Run the application:**

   ```bash
   python Router/main.py
   ```

## Usage

Upon running the application, users can:

- View current degree requirements.
- Add, update, or remove courses.
- Check progress towards degree completion.

*(Detailed usage instructions and interface guidelines will be provided in future updates.)*
