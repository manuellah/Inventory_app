import click, csv
from tabulate import tabulate
from pyfiglet import figlet_format
from cmd import Cmd
from inventory_app import Inventory

app_name = click.style(figlet_format('Inventory', font='big'),fg='red',bold=True)
inventory = Inventory()

class Main(Cmd):
    intro = click.style('\t============ WELCOME =============\n', fg = 'red', bold = True)
    doc_header = click.style('\tMain Commands', fg = 'green', bold = True)
    misc_header = click.style('\tMain Commands', fg = 'green', bold = True)
    undoc_header = click.style('\tOther Commands', fg = 'green', bold = True)
    ruler = click.style('-', fg = 'yellow')
    
    prompt = click.style("\n  Inventory Prompt >>> ", fg = 'cyan', bold = True)

    
    def do_add(self, args):
        '''
        Adds items to the database
        Syntax :  add <item_name> <quantity> <cost_per_item> or add
        '''
        if not args:
            click.secho("\n\t\t\tEnter The Item's Specifications",
                        fg = 'yellow', underline = True, bold = True) 

            item_name = raw_input(click.style("\n\t\tName : ", fg = 'yellow'))
            item_description = raw_input(click.style('\n\t\tDescription : ', fg = 'yellow'))
            item_quantity = raw_input(click.style('\n\t\tQuantity : ', fg = 'yellow'))
            cost_per_item = raw_input(click.style("\n\t\tCost Per Item : ", fg = 'yellow'))
            
            inventory.item_add(item_name, item_description, item_quantity, cost_per_item)
            return
        args = args.split()
        if len(args) != 3:
            fmt_str = "\n\t\tcorrect_syntax: add <item_name> <quantity> <cost_per_item>\n"
            click.secho(fmt_str, fg = 'yellow', bold = True, underline = True)
            return
        
        else:
            item_description = raw_input(click.style('\n\t\tDescription : ', fg = 'yellow'))
            inventory.item_add(args[0], item_description, args[1], args[2])
    
    
    def do_remove(self, args):
        '''
        Removes an item from the database or updates the quantity available
        correct_syntax: remove <item_id> or remove
        '''
        item_id =''
        if not args:
            item_id = raw_input(click.style("\n\tEnter Item Id : ", fg = 'yellow'))
        
        else:
            args = args.split()
            item_id = args[0]
            if not item_id.isdigit():
                click.secho('\n\t\tInvalid Input: Item Id is suppossed to be an integer', 
                            fg = 'yellow', bold = True, underline = True)
                
                return
            elif len(args) != 1:
                fmt_str = "\n\t\tcorrect_syntax: remove <item_id>\n"
                click.secho(fmt_str, fg = 'yellow', bold = True, underline = True)
                return
            else:
                item_id = args[0]

        inventory.item_remove(item_id)
        
    def do_list_all(self, args):
        '''
        Displays all the data in the database in a table.
        correct_syntax: list_all
        If argument --export supplied, it export the database to a csv file
        correct_syntax: list_all --export <filename>
        '''
        if not args:
            all_data = inventory.item_list() 
            click.secho('\n\t\t\t  List Of All The Assets\n', fg = 'yellow', bold = True, underline = True)
            headers = ['Id', 'Name', 'Quantity', 'Cost Per Item', 'Date added', 'Checked Status']
            click.secho(tabulate(all_data, tablefmt='fancy_grid', headers = headers), fg = 'yellow')
            
            return
        
        args = args.split()
        if args[0] == '--export':
            all_data = inventory.item_list() 
            click.secho('\n\t\t\t  List Of All The Assets\n', fg = 'yellow', bold = True, underline = True)
            headers = ['Id', 'Name', 'Quantity', 'Cost Per Item', 'Date added', 'Checked Status']
            click.secho(tabulate(all_data, tablefmt='fancy_grid', headers = headers), fg = 'yellow')
            
            inventory.db_state(args[1] ) 
            
        else:
            click.secho("\n\t\tIncorrect Syntax \n\n\tCorrect syntax : list_all --export <filename> ", fg = 'yellow')


    def do_checkout(self, args):
        '''
        Checks out an item from our warehouse. 
        Correct syntax : checkout <number> or checkout
        '''
        
        item_id = ''
        if not args:
            item_id = raw_input(click.style("\n\t\tEnter Item Id : ", fg = 'yellow'))
        else:
            item_id = args
        
        if item_id.isdigit():
            inventory.item_check_out(item_id)
            
        else:
            click.secho("\n\t\tIncorrect Syntax \n\n\tCorrect syntax : checkout <number> ", fg = 'yellow')
        
    def do_checkin(self, args):
        '''
        Checks in a previously checked out item from our warehouse. 
        Correct syntax : checkin <number> or checkin
        '''
        item_id = ''
        if not args:
            item_id = raw_input(click.style("\n\t\tEnter Item Id : ", fg = 'yellow'))
        else:
            item_id = args
        
        if item_id.isdigit():
            inventory.item_check_in(item_id)
            
        else:
            click.secho("\n\t\tIncorrect Syntax \n\n\tCorrect syntax : checkin <number> ", fg = 'yellow')
        
    def do_view_item(self, args):
        '''
        Displays full information of an item and also shows a log of
        all the times this item was checked out and checked in.
        Correct syntax :view_item <item_id> or view_item

        '''
        item_id = ''
        if not args:
            item_id = raw_input(click.style("\n\t\tEnter Item Id : ", fg = 'yellow'))
        
        else:
            item_id = args
        
        if not item_id.isdigit():
            click.secho("\n\t\tIncorrect Syntax \
                        \n\n\tCorrect syntax :view_item <item_id> or view_item", fg = 'yellow')
            return
            
        item_data_cons = inventory.item_view(item_id)
        if not item_data_cons:
            click.secho("\n\t\t\t No Such Item", fg = 'green', bold = True)
            return
        
        item_data = [click.style(str(item).ljust(30), fg = 'yellow') 
                     for item in item_data_cons]
        print '\n\tItem Id :'.ljust(31) + item_data[0]
        print '\tItem Name :'.ljust(30) + item_data[1]
        print '\tItem Description :'.ljust(30) + item_data[2]
        print '\tAvailable Quantity :'.ljust(30) + item_data[3]
        print '\tCost Per Item :'.ljust(30) + item_data[4]
        print '\tDate Bought :'.ljust(30) + item_data[5]
        print '\tChecked Status :'.ljust(30) + item_data[6]
        logs_data = item_data_cons[7]
        headers = ['Log Id','Check Out Date','Check In Date']
        format_str = '\n\t\t The check in/out log\n'
        click.secho(format_str, fg = 'yellow', bold = True)
        click.secho(tabulate(logs_data, tablefmt='fancy_grid', headers = headers), fg = 'yellow')
        
    def do_asset_value(self, args):
        '''
        Computes  total assets value. The sum of the cost of each item.
        Including the ones which have been checked out since they are still ours
        You online get ride of an item after you remove it(remove command)
        Correct syntax : asset_value 
        '''
        
        tot_assets_value = inventory.assetvalue()
        format_str = '\n\t\t The Total Assets Value\n'
        val = '\t\t\t  {}\n'.format(tot_assets_value)
        eq = '=' * 50
        click.secho('\n\n\t' + eq + '\n', fg = 'cyan', bold = True)
        click.secho(format_str, fg = 'yellow', bold = True)
        click.secho(val, fg = 'yellow', bold = True)
        click.secho('\n\t' + eq + '\n', fg = 'cyan', bold = True)
        
    def do_search(self, args):
        '''
        Returns a list of all the items that match the search_query. 
        Correct syntax :search <search_query> or search
        '''
        
        search_data = ''
        if not args:
            search_data = raw_input(click.style("\n\t\tEnter Your Search Request : ", fg = 'yellow'))
        
        else:
            search_data = args
   
        results = inventory.item_search(search_data)
        headers = ['Id', 'Name', 'Quantity', 'Cost Per Item', 'Date added', 'Checked Status']
        print '\n\n'
        click.secho(tabulate(results, tablefmt='fancy_grid', headers = headers), fg = 'yellow')
    def do_quit(self, args):
        '''
        To exit the application
        syntax : quit
        '''
        print '\n\n'
        return True
    
    def do_exit(self, args):
        '''
        To exit the application
        syntax : exit
        '''
        print '\n\n'
        return True
    
    def do_clear(selff, args):
        '''
        Clears the window/shell
        syntax : clear
        '''
        click.clear()
        
    def emptyline(self):
        '''
        Pressing ENTER in the prompt displays a blank prompt
        '''
        pass 
    
    def default(self, args):
        '''
        Inventory Application Commands
        
        '''
        click.secho("\n\t\tInventory Application's Command", fg = 'blue', bold = True, underline = True)
        commands = '''
        1. add item : add <item_name> <quantity> <cost_per_item> or add
        \n\t2. remove item: remove <item_id> or remove
        \n\t3. view database: list_all --export <filename> or list_all
        \n\t4. check out item : checkout <number> or checkout
        \n\t5. check in item : checkin <number> or checkin
        \n\t6. full item details :view_item <item_id> or view_item
        \n\t7. computes total worth of our inventory : asset_value
        \n\t8. Search item :search <search_query> or search
        \n\t9. configure you prompt: config <prompt string>
        \n\t10. exit the application : exit or quit
        \n\t11. clear window/shell: clear
        '''
        click.secho(commands, fg = 'yellow', bold = True)
        
    def do_config(self, args):
        '''
        Configure the prompt to suite your taste
        syntax : clear
        syntax: config <prompt string>
        '''
        Main.prompt = click.style(args+' >>> ', fg = 'cyan', bold = True)
        
        
if __name__ == '__main__':
    click.clear()
    print app_name
    Main().cmdloop()
