<h1>Installing</h1>

<h3>Clone the project</h3>

<pre>git clone https://github.com/gsg27/django-interview-assignment.git
cd django-interview-assignment
</pre>



<h3>Install dependencies & activate virtualenv</h3>

<pre>
python -m venv env
.\env\Scripts\activate
python -m pip install -r requirements.txt
</pre>



<h3>Apply migrations</h3>

<pre>python manage.py migrate</pre>

<h3>To run the development server</h3>

<h3>Just run this command:</h3>

<pre>python manage.py runserver</pre>

Test API at http://127.0.0.1:8000/api/schema/swagger-ui/

API documentation available at http://127.0.0.1:8000/api/schema/redoc
