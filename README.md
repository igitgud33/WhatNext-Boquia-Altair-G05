# WhatNext

**WhatNext** is a web-based personal media backlog management system that helps users organize and track their games, movies, and books in one centralized platform.

Instead of managing separate lists across different platforms, users can browse a shared media catalog, add titles to their personal backlogs, and monitor their progress through different completion statuses.

## Core Features

### Media Catalog
- Browse available games, movies, and books.
- View media information, including titles, descriptions, release dates, and cover images.
- Submit new media items to the catalog.

### Personal Backlog Management
- Add catalog items to a personal backlog.
- View saved media in one centralized list.
- Update the status of each item:
  - Wishlisted
  - In Progress
  - On Hold
  - Dropped
  - Completed
- Remove items from a personal backlog without deleting them from the shared catalog.

### User Accounts
- Register and log in to a personal account.
- Manage personal backlog entries associated with the authenticated user.

## Technologies Used

- **Backend:** Python, Django
- **Frontend:** HTML, CSS, Bootstrap
- **Database:** PostgreSQL (for the configured deployment/final database)
- **Image Handling:** Pillow
- **Version Control:** Git and GitHub

## Project Setup

Follow these steps to run WhatNext locally.

### 1. Clone the Repository

```bash
git clone https://github.com/igitgud33/WhatNext-Boquia-Altair-G05.git
cd WhatNext-Boquia-Altair-G05
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv .venv
```

For Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project directory and provide the required environment variables for your database and Django configuration.

**Do not commit your `.env` file or expose secret keys and database credentials.**

### 5. Apply Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create an Administrator Account (Optional)

```bash
python manage.py createsuperuser
```

Follow the prompts to create an administrator account.

### 7. Run the Development Server

```bash
python manage.py runserver
```

Open the following address in your browser:

`http://127.0.0.1:8000/`

## Project Structure

```text
WhatNext-Boquia-Altair-G05/
│
├── whatnext/
│   ├── accounts/
│   ├── catalog/
│   ├── dashboard/
│   ├── templates/
│   ├── media/
│   ├── manage.py
│   └── ...
│
├── .gitignore
├── requirements.txt
└── README.md
```

## Development Notes

- The project is developed using Django's template-based architecture.
- Media catalog records and individual user backlog entries are stored separately.
- Each backlog entry belongs to a specific authenticated user.
- Removing an item from a user's backlog does not remove the corresponding catalog record.

## Contributors

**Project:** WhatNext  
**Repository:** [WhatNext-Boquia-Altair-G05](https://github.com/igitgud33/WhatNext-Boquia-Altair-G05)
