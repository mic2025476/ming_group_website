Step‑by‑Step Guide to Clone, Configure and Run the Django “ming_group_website” Project updated

1. What Is This Repository?
- Framework: Django (a Python toolkit for building websites)
- Name: ming_group_website
- Contents at a glance:
  - manage.py – main Django command‑line tool
  - requirements.txt – list of Python libraries required
  - db.sqlite3 – local file‑based database
  - Folders:
    - static/ (images, CSS, JavaScript)
    - templates/ (HTML layout files)
    - company_logos/ and companies/ (data folders)

2. Prerequisites

Option A: Local Python Setup
1. Install Python 3.10+ (from python.org)
2. Install Git (from git‑scm.com)
3. Know how to open a terminal or command prompt

3. Clone the Code

1. Open your terminal (PowerShell on Windows, Terminal on macOS/Linux).
2. Navigate to a working folder, for example:
   cd ~/Projects
3. Clone this repository and enter its folder:
   git clone https://github.com/mic2025476/ming_group_website.git
   cd ming_group_website

4A. Running Locally with Python + SQLite

1. Create a virtual environment:
   python3 -m venv venv
2. Activate it:
   - macOS/Linux: source venv/bin/activate
   - Windows: venv\Scripts\activate
3. Upgrade pip and install dependencies:
   pip install --upgrade pip
   pip install -r requirements.txt
4. Configure environment variables:
   - In the project root, create a file named .env containing:
     SECRET_KEY=<your‑random‑string>
     DEBUG=True
     ALLOWED_HOSTS=localhost,127.0.0.1
   - To generate a secret key, run:
     python3 - <<<'import secrets; print(secrets.token_urlsafe())'
5. Run database migrations:
   python manage.py migrate
6. Create the Django admin user:
   python manage.py createsuperuser
   Follow the prompts to set username and password.
7. Collect static files:
   python manage.py collectstatic --noinput
8. Start the development server on port 8000:
   python manage.py runserver 8000
9. View in your browser:
   - Front‑end site: http://127.0.0.1:8000
   - Admin panel:   http://127.0.0.1:8000/admin

5. Quick‑Reference Command Table

| Task                     | Local (Python) Command                         | Docker Command                         |
|--------------------------|------------------------------------------------|----------------------------------------|
| Clone repo               | git clone … && cd ming_group_website           | Same as local                          |
| Install dependencies     | pip install -r requirements.txt                | _Not needed_                           |
| Run server               | python manage.py runserver 8000                | docker-compose up --build              |
| Open site                | http://127.0.0.1:8000                          | http://localhost                       |
| Admin login              | http://127.0.0.1:8000/admin                    | http://localhost/admin                 |
| Stop server              | Ctrl + C                                       | docker-compose down                    |

6. What’s Happening Under the Hood?
1. Django reads your .env file to configure settings (secret key, debug mode, database host, etc.).
2. Migrations apply database schema changes automatically.
3. collectstatic copies all static assets (CSS, JS, images) into a single folder for easy serving.
4. runserver (or Gunicorn behind Nginx) listens on the specified port and serves pages when you point your browser to it.


