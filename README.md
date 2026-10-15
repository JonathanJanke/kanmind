# Kanmind

Kanmind is a Django REST API for boards, tasks, and users. The database is SQLite by default.

## Requirements

- Python 3.13 is recommended for the dependencies specified in `requirements.txt`.
- Git

## Clone the project

```bash
git clone <REPOSITORY-URL>
cd kanmind
```

Replace `<REPOSITORY-URL>` with the project's clone URL.

## Setup on Windows (PowerShell)

Run these commands from the project directory:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

If PowerShell blocks activation because of the execution policy, use `.venv\Scripts\python.exe` instead of `python` for the following Python commands, for example:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py runserver
```

## Setup on Unix (Linux/macOS)

Run these commands from the project directory:

```bash
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
cp .env.example .env
```

If `python3.13` is not available, use an installed Python version that is compatible with the Django dependencies in `requirements.txt`.

## Environment variables

Open the newly created `.env` file. Set a unique Django secret key for your local installation and keep `DEBUG=True` enabled for local development. You can generate a secret key with the following command after installing the dependencies:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Add the output to `.env`:

```dotenv
SECRET_KEY=<GENERATED-SECRET-KEY>
DEBUG=True
```

The `.env` file contains local configuration and secrets. Do not share it or commit it to the repository.

## Set up the database and start the server

The development configuration uses SQLite. Create or update the database using the existing migrations:

```bash
python manage.py migrate
```

You can optionally create an admin user:

```bash
python manage.py createsuperuser
```

Start the development server:

```bash
python manage.py runserver
```

The API will then be available at <http://127.0.0.1:8000/api/>. The Django admin interface is available at <http://127.0.0.1:8000/admin/>.

To stop the server, press `Ctrl+C`. Exit the virtual environment with `deactivate`.

## Tests

Run the Django tests from the activated virtual environment and project directory:

```bash
python manage.py test
```

## Security note

`DEBUG=True` is intended for local development only. Before using the application publicly or in production, you must at least disable `DEBUG`, set a secure secret key, and configure `ALLOWED_HOSTS` appropriately in `core/settings.py`. Do not use Django's development server as a production server.
