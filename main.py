import click
from tabulate import tabulate
from pyfiglet import figlet_format
from cmd import Cmd
from inventory_app import inventory

app_name = click.style(figlet_format('Inventory', font='big'),fg='red',bold=True)
inventory = inventory()

class Main(Cmd):
    intro = click.style('\t============ WELCOME =============\n', fg = 'red', bold = True)
    doc_header = click.style('', fg = 'green', bold = True)
    misc_header = 'Main Commands'
    undoc_header = 'Other Commands'
    ruler = click.style('-', fg = 'yellow')
    
    prompt = click.style("\n  Inventory Prompt >>> ", fg = 'cyan', bold = True)

    
    def do_add(self, args):
        click.secho("\n\t\t\tEnter The Item's Specifications", fg = 'yellow', underline = True, bold = True) 
        
        item_name = raw_input(click.style("\n\t\tName : ", fg = 'yellow'))
        item_description = raw_input(click.style('\n\t\tDescription : ', fg = 'yellow'))
        item_quantity = raw_input(click.style('\n\t\tQuantity : ', fg = 'yellow'))
        cost_per_item = raw_input(click.style("\n\t\tCost Per Item : ", fg = 'yellow'))
                                  
        inventory.item_add(item_name, item_description, item_quantity, cost_per_item)
    
    def do_remove(self, args):
        item_id = raw_input(click.style("\n\t\tEnter Item Id : ", fg = 'yellow'))
        inventory.item_remove(item_id)
        
        
    def do_list_all(self, args):
        all_data = inventory.item_list() 
        click.secho('\n\t\t\t  List Of All The Assets\n', fg = 'yellow', bold = True, underline = True)
        headers = ['Id', 'Name', 'Quantity', 'Cost Per Item', 'Date added', 'Ckecked Status']
        click.secho(tabulate(all_data, tablefmt='fancy_grid', headers = headers), fg = 'yellow')
        
    def do_checkout(self, args):
        item_id = raw_input(click.style("\n\t\tEnter Item Id : ", fg = 'yellow'))
        inventory.item_check_out(item_id)
        
    def do_checkin(self, args):
        item_id = raw_input(click.style("\n\t\tEnter Item Id : ", fg = 'yellow'))
        inventory.item_check_in(item_id)
        
    def do_view_item(self, args):
        item_id = raw_input(click.style("\n\t\tEnter Item Id : ", fg = 'yellow'))
        item_data_cons = inventory.item_view(item_id)
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
        tot_assets_value = inventory.assetvalue()
        format_str = '\n\t\t The Total Assets Value\n'
        val = '\t\t\t  {}\n'.format(tot_assets_value)
        eq = '=' * 50
        click.secho('\n\n\t' + eq + '\n', fg = 'cyan', bold = True)
        click.secho(format_str, fg = 'yellow', bold = True)
        click.secho(val, fg = 'yellow', bold = True)
        click.secho('\n\t' + eq + '\n', fg = 'cyan', bold = True)
        
    def do_search(self, args):
        results = inventory.item_search()
        headers = ['Id', 'Name', 'Quantity', 'Cost Per Item', 'Date added', 'Ckecked Status']
        click.secho(tabulate(results, tablefmt='fancy_grid', headers = headers), fg = 'yellow')
    def do_quit(self, args):
        return True
    
    def do_clear(selff, args):
        click.clear()
        
    def emptyline(self):
        pass 
    
    def default(self, args):
        click.secho("Invalid Command", fg = 'red')
        
    def do_config(self, args):
        Main.prompt = click.style(args+' >>> ', fg = 'yellow', bold = True)
        
        
if __name__ == '__main__':
    print app_name
    Main().cmdloop()