# Order Processing System\*\*

This is a Django application that allows users to process orders in TSV format.

## Features

Allows users to input TSV data through a form
Processes each row of the TSV data and checks that the header is correct and the order date is after a certain date
Creates a dictionary with the customer name as the key, and the values being the order id, order date and line items, which includes the product url and revenue
If there are any errors, they are added to a list
The data and error responses are returned in a serialized format through a REST API

## Prerequisites

- Python 3.x
- Django 3.x
- Django REST framework

### Getting started

- Clone the repository using :
  `git clone https://github.com/yourusername/order-processing-system.git`

- Change into the project directory
- Create a virtual environment: python -m venv env
- Activate the virtual environment: source env/bin/activate
- Install the required dependencies: `pip install -r requirements.txt`
- Run Server: `python manage.py runserver`
  - Running the above command will install django and django-rest-framework which are required to run this application locally.

NOTE: Based on your Python ALIS you may have to use `python` or `python3` to run the above commands. Same would apply when running pip commands. Use `pip` or `pip3` to run

## Contact
For any further questions or inquiries, feel free to contact me at shreyesathreya@gmail.com