# Django Project Setup for AppGenixtask

## Project Setup

This Django project provides API functionality for user management and post creation, as well as an admin setup.

### Prerequisites

- Python 3.x
- Django 3.x or higher
- Django REST Framework
- Other dependencies listed in `requirements.txt`

---

## Steps to Set Up the Project

### 1. Clone the Repository

Clone the project repository to your local machine:

```bash
git clone https://github.com/durgesh253/appgenixtask.git
cd appgenixtask

# For Linux/macOS
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
.\venv\Scripts\activate



3. Install Dependencies
pip install -r requirements.txt


4. Database Setup
Run the following commands to make migrations and migrate the database:


# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

5. Create Superuser (Admin)
Create a superuser for the Django admin panel:


python manage.py createsuperuser


6. Run the Development Server
Start the Django development server:

python manage.py runserver


Default Admin Setup
By default, after running migrations, the following admin user will be set up:
   email='admin@example.com',  # set a default admin email
    password="adminpassword",
    username='admin'
You can log into the Django admin panel using these credentials.

