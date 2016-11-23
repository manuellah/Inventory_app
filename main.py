import click
from tabulate import tabulate
from pyfiglet import figlet_format
from cmd import Cmd
from inventory_app import inventory

app_name = click.style(figlet_format('Inventory', font='big'),fg='red',bold=True)
inventory = inventory()

class Main(Cmd):
    intro = click.style('\t============ WELCOME =============\n', fg = 'red', bold = True)
    doc_header = 'doc_header'
    misc_header = 'misc_header'
    undoc_header = 'undoc_header'
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