Order Processing System
This is a Django application that allows users to process orders in TSV format.

Features
Allows users to input TSV data through a form
Processes each row of the TSV data and checks that the header is correct and the order date is after a certain date
Creates a dictionary with the customer name as the key, and the values being the order id, order date and line items, which includes the product url and revenue
If there are any errors, they are added to a list
The data and error responses are returned in a serialized format through a REST API
Prerequisites
Python 3.x
Django 3.x
REST framework
Getting started
Clone the repository: git clone https://github.com/yourusername/order-processing-system.git
Change into the project directory: cd order-processing-system
Create a virtual environment: python -m venv env
Activate the virtual environment: source env/bin/activate
Install the required dependencies: pip install -r requirements.txt
Run migrations: python manage.py makemigrations then python manage.py migrate
Start the development server: python manage.py runserver
Go to http://localhost:8000/ in your browser to access the application
Note
Make sure to add a secret_key.py file in the project root directory with a SECRET_KEY variable, this is used for security purpose.
You can also make use of .gitignore file to ignore sensitive files or directories that should not be tracked by Git.
Contribution
Feel free to contribute to this project by creating pull requests or reporting issues.

License
This project is licensed under the MIT License - see the LICENSE file for details.

Contact
For any further questions or inquiries, feel free to contact me at email or website.