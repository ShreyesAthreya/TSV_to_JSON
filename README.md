# Order Processing System

This is a Django application that allows users to process orders in TSV format.

## Features

- Allows users to input TSV data through a form.
- Processes each row of the TSV data and returns a JSON response with orders information for each customer.
- Reponse from api includes processed rows, errors of rows that cannot be processed
The data and error responses are returned in a serialized format through a REST API

### Dependency version used during build
- python=3.10
- django=4.1
- djangorestframework=3.14
## Prerequisites

- Python 3.x
- Django 3.x and above
- Django REST Framework

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


### Usage
- To run the application, start server `python manage.py runserver` 
- The app defaults running on localhost:8000 and the UI endpoint to access the application is using
  - https://localhost:8000/process_orders/

- User will be promted with a textarea form to submit the TSV data.
- Headers like [Row ID, Customer Name, Order, Revenue] are optional. Application will process data regardless.


To test the application by hitting the API endpoints directly without a presentation layer,
- `http://localhost:8000/process_orders/` with key as `tsv_data` and the value will be the TSV data the user sends.

The response will be in the format of 
```json
{
    "id": 1,
    "data": {
        "Claire Gute": {
            "orders": [
                {
                    "order_id": "CA-2016-152156",
                    "order_date": "2016-11-08T00:00:00",
                    "line_items": [
                        {
                            "product_url": "https://www.foo.com/Furniture/Bookcases/FUR-BO-10001798",
                            "revenue": 261.96
                        },
                        {
                            "product_url": "https://www.foo.com/Furniture/Chairs/FUR-CH-10000454",
                            "revenue": 731.94
                        }
                    ]
                }
            ]
        }
    },
    "errors": [
        "Error in row ['23', 'CA-2016-137330', '12/09/2016', '12/13/16', 'Standard Class', 'KB-16585', 'Ken Black', 'Corporate', 'United States', 'Fremont', 'Nebraska', '68025', 'Central', 'OFF-AP-10001492', 'Office Supplies', 'Appliances', \"Acco Six-Outlet Power Strip, 4' Cord Length\", 'Art', '7', '0', '15.6884']. 'Art' is not in list"
    ]
}
```
<br>
The order_date is in USO 8601 format without any timezone data.

- 2016-11-08**T00:00:00**

### get_orders
Similarly to retrive information about a particular order, 
```
  http://localhost:8000/get_orders/pk
```
The PK will be the 'id' returned from earlier response.

### get_all_orders
To retrive information about all stored orders, 
```
  http://localhost:8000/get_orders/
```
Sending a GET request without the PK/id will return all available responses, the size of total responses, and all errors.

```json
  {
      "size": n,
      "data": [{...}, {...}],
      "errors": [[..], [..]]
  }
```


## Contact
For any further questions or inquiries, feel free to contact me at shreyesathreya@gmail.com