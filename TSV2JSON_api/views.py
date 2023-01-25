import csv
import datetime
import json
from io import StringIO
from urllib.parse import quote

from django import forms
from django.shortcuts import render
from rest_framework import viewsets, serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response


#
# def home(request):
#     return render(request, 'process_orders.html')


class OrderSerializer(serializers.Serializer):
    tsv_data = serializers.CharField()

    # def create(self, validated_data):
    #     return OrderProcessor(validated_data)


data_responses = []
errors_response = []


class ProcessOrdersForm(forms.Form):
    tsv_data = forms.CharField(widget=forms.Textarea, required=True)


class OrderProcessor:
    def __init__(self, validated_data):
        self.data = {}
        self.errors = []
        self.base_url = "https://www.foo.com"
        # date_filter used to ignore rows that contains date lesser than 31/07/2016
        self.date_filter = datetime.datetime.strptime("07/31/2016", "%m/%d/%Y")
        rows = self.get_rows(validated_data['tsv_data'])
        self.process_rows(rows)

    @staticmethod
    def get_rows(tsv_data):
        # Strips the tab space and returns list of items per row.
        tsv_file = StringIO(tsv_data)
        rows = list(csv.reader(tsv_file, delimiter='\t'))
        return rows

    def process_rows(self, rows):
        header = rows[0]
        # Check if first row is header or order_history row
        if ['Row ID', 'Order ID', 'Order Date', 'Ship Date', 'Ship Mode', 'Customer ID', 'Customer Name', 'Segment',
            'Country', 'City', 'State', 'Postal Code', 'Region', 'Product ID', 'Category', 'Sub-Category',
            'Product Name', 'Sales', 'Quantity', 'Discount', 'Profit'] == header:
            rows = rows[1:]
        # Operation skipped for the first row if they match the header format

        for row in rows:
            try:
                row_id, order_id, order_date, _, _, _, customer_name, _, _, _, _, _, _, product_id, category, sub_category, _, sales, _, _, _ = row
                try:
                    # Checks if date in the format of mm/dd/YYYY
                    order_date = datetime.datetime.strptime(order_date, "%m/%d/%Y")
                except ValueError:
                    try:
                        # Checks if date in the format of mm/dd/YY
                        order_date = datetime.datetime.strptime(order_date, "%m/%d/%y")
                    except ValueError:
                        self.errors.append(f"Row {row_id}, column 3 has an unexpected value. Invalid Order Date format")
                        continue
                if order_date > self.date_filter:
                    # product_url = f"{self.base_url}{category}/{sub_category}/{product_id}"
                    revenue = None
                    try:
                        revenue = float(sales)
                    except ValueError:
                        self.errors.append(f"Row {row_id}, column {header.index(sales)} has an unexpected value."
                                           f"{sales} not of type float. Using null by default")

                    product_url = "{}/{}/{}/{}".format(self.base_url, quote(category), quote(sub_category),
                                                       quote(product_id))
                    item = {"product_url": product_url, "revenue": revenue}
                    if customer_name in self.data:
                        existing_order = None
                        for order in self.data[customer_name]['orders']:
                            if order['order_id'] == order_id:
                                existing_order = order
                                break

                        if existing_order:
                            existing_order["line_items"].append(item)
                        else:
                            order_date = order_date.isoformat()
                            order_items = {"order_id": order_id, "order_date": order_date, "line_items": [item]}
                            self.data[customer_name]['orders'].append(order_items)
                    else:
                        order_date = order_date.isoformat()
                        order_items = {"order_id": order_id, "order_date": order_date, "line_items": [item]}
                        self.data[customer_name] = {"orders": [order_items]}
            except ValueError as e:
                self.errors.append(f"Error in row {row}. {e}")
        data_responses.append(self.data)
        errors_response.append(self.errors)


def json_formatter(data):
    # Convert the Python object into a JSON string
    json_string = json.dumps(data)

    # Parse the JSON string and convert it into a Python object
    parsed_json = json.loads(json_string)

    # Use json.dumps() method with indent parameter to format the JSON
    formatted_json = json.dumps(parsed_json, indent=4)

    return formatted_json


class OrderViewSet(viewsets.ViewSet):

    @action(methods=['get'], detail=True)
    def get_orders(self, request, pk=None):
        """
        Checks if request from browser or API test tool
        Checks if ID given or valid or no response generated so far -> returns empty response with 'Key not present in error'
        If Key present, returns value as JSON response.
        """
        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
        if 'windows' in user_agent or 'macintosh' in user_agent or 'linux' in user_agent:
            if len(data_responses) == 0 or not pk or pk > len(data_responses):
                return render(request, 'get_orders.html', {'id': pk, 'data': None, 'errors': "Key not found"})
            formatted_json = json_formatter(data_responses[pk - 1])
            formatted_errors = json_formatter(errors_response[pk - 1])
            return render(request, 'get_orders.html', {'id': pk, 'data': formatted_json, 'errors': formatted_errors})
        else:
            if not pk:
                return Response(data_responses)
            try:
                index = int(pk) - 1
                return Response(
                    {'id': len(data_responses), 'data': data_responses[index], 'errors': errors_response[index]})
            except IndexError:
                return Response({'data': [], 'errors': "Invalid ID " + str(index)},
                                status=status.HTTP_404_NOT_FOUND)

    @action(methods=['get', 'post'], detail=False)
    def process_orders(self, request, pk=None):
        """
        If get request, returns form for user to enter TSV_Data
        if post request, validates input, generates JSON message, adds any error during transformation.
        Returns the last added response, error to user
        """
        if request.method == 'GET':
            form = ProcessOrdersForm()
            return render(request, 'process_orders.html', {'form': form})

        elif request.method == 'POST':
            serializer = OrderSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            order_processor = OrderProcessor(serializer.validated_data)
            data = order_processor.data
            errors = order_processor.errors

            # Check if request from a browser or API Test tool
            user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
            if 'windows' in user_agent or 'macintosh' in user_agent or 'linux' in user_agent:
                if data_responses:
                    formatted_json = json_formatter(data_responses[-1])
                    formatted_errors = json_formatter(errors_response[-1])
                    return render(request, 'get_orders.html',
                                  {'id': len(data_responses), 'data': formatted_json, 'errors': formatted_errors})
            else:
                return Response({'id': len(data_responses), 'data': data, 'errors': errors})
