#Inventory management application
This is a command line application(Inventory management application) 

##Run App

Clone the directory: git clone https://github.com/manuellah/bc-12-inventory_app.git

Go to the app directory cd bc-12-inventory_app

Ensure you are running virtual enviroment:
if on mac or linux

```console
. venv/bin/activate 
```
if on windows
```console
venv\scripts\activate 
```
install requirements
```console
Install requirements: pip install -r requirements.txt
```
start app
```console
Run the app: python main.py
```

##application's Commands

1. add item : add <item_name> <quantity> <cost_per_item> or add
2. remove item: remove <item_id> or remove
3. view database: list_all --export <filename> or list_all
4. check out item : checkout <number> or checkout
5. check in item : checkin <number> or checkin
6. full item details :view_item <item_id> or view_item
7. computes total worth of our inventory : asset_value
8. Search item :search <search_query> or search
9. configure you prompt: config <prompt string>
10. exit the application : exit or quit
11. clear window/shell: clear


##application descriptions

Inventory management application has the following commands:

1. item add <item_details> - Adds an item to the inventory.

2. item remove <item_id> - Removes an item from the inventory.

3. item list - Lists all the items available in the inventory with their status (checked out or checked in).

item list --export <file_name> - This command exports the entire inventory as a CSV file with all the fields listed above.
4. item checkout <item_id> - Checkout an item from the warehouse/store.

5. item checkin <item_id> - Checkin an item that was previously checked out.

6. item view <id> - View all the item details for item with id <id>. In addition to that, this command shows a log of all the times this item was checked out and checked in.

7. item search <search_query> - Return a list of all the items that match the search_query.

8. compute assetvalue - Calculate total assets value. The sum of the cost of each item.

An inventory item should have the following properties - id, name, description, total amount available, cost per item, date added, status (Can be one of true or false denoting items that have either been checked out or not respectively).


