Installing

Clone the project
git clone https://github.com/gsg27/django-interview-assignment.git
cd django-interview-assignment

Install dependencies & activate virtualenv
python -m venv env
.\env\Scripts\activate
python -m pip install -r requirements.txt

Apply migrations
python manage.py migrate


To run the development server
Just run this command:

python manage.py runserver

API available at http://127.0.0.1:8000/api/schema/swagger-ui/
API documentation available at http://127.0.0.1:8000/api/schema/redoc
