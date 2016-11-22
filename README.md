#Inventory management application

Inventory management application has the following commands:
 1. item add <item_details> - Adds an item to the inventory.
 2. item remove <item_id> - Removes an item from the inventory.
 3.  item list - Lists all the items available in the inventory with their status (checked out or checked in).
 4. item list --export <file_name> - This command exports the entire inventory as a CSV file with all the fields listed above.
 5.  item checkout <item_id> - Checkout an item from the warehouse/store.
 6. item checkin <item_id> - Checkin an item that was previously checked out.
 7. item view <id> - View all the item details for item with id <id>. In addition to that, this command shows a log of all the times this item was checked out and checked in.
8.  item search <search_query> - Return a list of all the items that match the search_query.
 9. compute assetvalue - Calculate total assets value. The sum of the cost of each item.
10. An inventory item should have the following properties - id, name, description, total amount available, cost per item, date added, status (Can be one of true or false denoting items that have either been checked out or not respectively).
