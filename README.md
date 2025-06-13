Here's a comprehensive, professional README documentation for your Smart Task Scheduler project:

# Smart Task Scheduler with Prioritization

## Table of Contents
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Technology Stack](#technology-stack)
4. [System Architecture](#system-architecture)
5. [Database Schema](#database-schema)
6. [Installation Guide](#installation-guide)
7. [Usage Instructions](#usage-instructions)
8. [Team Members](#team-members)
9. [Future Enhancements](#future-enhancements)

## Project Overview
The Smart Task Scheduler is a desktop application designed to help Pan-Atlantic University Computer Science students manage their academic and extracurricular responsibilities effectively. The system provides intuitive task management with prioritization based on deadlines and importance levels.

## Features
### Core Functionality
- **Task Management**:
  - Add new tasks with title, description, priority, deadline, and duration
  - Edit existing tasks
  - Delete tasks
- **Smart Prioritization**:
  - Automatic sorting by priority (High/Medium/Low)
  - Urgency-based sorting (proximity to deadline)
- **Visual Indicators**:
  - Color-coded display for overdue (red) and completed (green) tasks
  - Clear status indicators (✓ Completed, ⚬ Pending, ⚠ Overdue)
- **Comprehensive Views**:
  - List view with all task details
  - Task description preview
  - Statistics dashboard

### User Experience
- Intuitive GUI with ttkbootstrap styling
- Keyboard shortcuts for common operations
- Context menu for quick actions
- Responsive design with clear status messages
- Help system with usage instructions

## Technology Stack
| Component          | Technology Used |
|--------------------|-----------------|
| Programming Language | Python 3.x |
| GUI Framework | Tkinter (with ttkbootstrap for modern styling) |
| Database | PostgreSQL |
| Database Connector | psycopg2 |
| Date/Time Handling | Python datetime module |

## System Architecture
```
Smart Task Scheduler Architecture
┌─────────────────────────────────────────────────────────────────────┐
│                            Presentation Layer                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────────┐  │
│  │   main.py   │  │ form_ui.py  │  │      task_display.py        │  │
│  └─────────────┘  └─────────────┘  └─────────────────────────────┘  │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                            Business Logic Layer                     │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                          engine.py                            │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                            Data Access Layer                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────────┐  │
│  │ schemas.sql │  │ init_db.py  │  │      connection.py          │  │
│  └─────────────┘  └─────────────┘  └─────────────────────────────┘  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Database Schema
```sql
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    priority TEXT CHECK (priority IN ('Low', 'Medium', 'High')),
    deadline TIMESTAMP,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

Key Features:
- Data integrity enforced through CHECK constraints
- Automatic timestamping of task creation
- Flexible storage for task details

## Installation Guide

### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- pip package manager

### Setup Instructions
1. **Database Setup**:
   ```bash
   # Create database
   createdb task_scheduler_db

   # Set up tables
   psql -d task_scheduler_db -f schemas.sql
   ```

2. **Python Environment**:
   ```bash
   # Install dependencies
   pip install psycopg2-binary ttkbootstrap

   # Run the application
   python main.py
   ```

## Usage Instructions
### Basic Operations
1. **Adding a Task**:
   - Fill in task details in the input form
   - Click "Add Task" or press Ctrl+N

2. **Editing a Task**:
   - Select task from list
   - Click "Edit Task"
   - Modify fields and click "Update Task"

3. **Deleting a Task**:
   - Select task from list
   - Click "Delete Task" or press Delete key

### Advanced Features
- **Sorting**: Click on column headers to sort
- **Quick Actions**: Right-click on tasks for context menu
- **Search**: Use the search box to filter tasks
- **Completion**: Toggle task completion with Spacebar

### Keyboard Shortcuts
| Shortcut       | Action                  |
|----------------|-------------------------|
| Ctrl+N         | Create new task         |
| Delete         | Delete selected task    |
| Space          | Toggle completion       |
| F5             | Refresh task list       |
| Double-click   | View full description   |

## Team Members
| Name & ID                            | Role                      | Components Developed                        |
|--------------------------------------|---------------------------|---------------------------------------------|
| EMMANUEL Daniel (24120111035)        | Team Lead                 | main.py, engine.py, overall architecture    |
| DELE-LAWAL Momooreoluwa (24120111029)| UI Specialist             | form_ui.py                                  |
| OLADIPUPO Oluwatamilore (24120111079)| Database Engineer         | schemas.sql, init_db.py, connection.py      |
| OSEGHALE Nehireme (24120112048)      | Display Specialist        | task_display.py                             |
| BOBMANUEL Tomba (24120112016)        | Documentation In-Charge   | Incharge of the documentation               |


## Future Enhancements
1. **User Accounts**: Multi-user support with authentication
2. **Calendar Integration**: Sync with academic calendar
3. **Mobile Version**: Cross-platform availability
4. **Advanced Analytics**: Time management insights
5. **Notification System**: Desktop alerts for deadlines
6. **Task Dependencies**: Set prerequisite relationships
7. **File Attachments**: Support for adding reference files

## Acknowledgments
Special thanks to Dr Desmond Moru & Mr. George Uwagbale (COS 102 Lecturers) for guidance on this project.

---