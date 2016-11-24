from models import  Asset, Log, Session
from datetime import datetime
import click, csv

class Inventory(object):
    def __init__(self, inventory = "my_inventory"):
        self.inventory = inventory
        self.session = Session()
        
    def item_add(self, item_name, item_description, item_quantity,
                 cost_per_item):
        
        date_added = datetime.now().strftime('%Y-%m-%d %H:%M')
        item_status = True
        
        self.session.add(Asset(item_name, item_description, item_quantity, 
                    cost_per_item, date_added,  item_status))
        self.session.commit()
        
        click.secho("\n\t\t\tSuccessfully Added", fg = 'green', bold = True) 
        
    def item_remove(self, item_id):
        display = "\n\tEnter The Quantity To Remove or D to Delete The Entire Row : "
        action = raw_input(click.style(display , fg = 'yellow'))

        if action.upper() == 'D':
            pass
        elif action.isdigit():
            pass
        else:
            print action.upper()
            click.secho("\n\t\t\t Invalid Quantity Value (Either D or Number)", fg = 'red', bold = True)
            return
                
        query = (self.session.query(Asset)
                  .filter(Asset.assetId==item_id)).first()
        self.session.commit()
        
        if query is None:
            click.secho("\n\t\t\t No Such Item", fg = 'red', bold = True) 
            
        elif action.upper() == 'D':
            self.session.query(Asset.assetId).filter(Asset.assetId ==   item_id).delete()
            self.session.commit()
            click.secho("\n\t\t\tSuccessfully Removed", fg = 'green', bold = True) 
            
        elif isinstance(float(action), float):
            deduct = float(action)
            current_quantity = query.item_amount_available
            if deduct <= 0 :
                click.secho("\n\t\t\tCan Not Update negative or Zero Quantity", fg = 'red', bold = True)
            elif deduct > current_quantity:
                click.secho("\n\t\t\tQuantity Entered Is Greater Than Available Quantity", fg = 'red', bold = True)
            else:
                query1 = (self.session.query(Asset)
                  .filter(Asset.assetId==item_id))
                new_bal = current_quantity - deduct
                format_str = "\n\t\t\tSuccessfully Update. New Balance   {}".format(new_bal)
                query1.update({'item_amount_available': new_bal})
                click.secho(format_str, fg = 'green', bold = True)

    def item_list(self):
        mydata = []
        rs = self.session.query(Asset).all()
        self.session.commit()
        for item in rs:
            mydata.append([item.assetId, item.item_name,
             item.item_amount_available, item.cost_per_item, item.date_added,
             item.item_status])
            
        return mydata
 
    def item_check_out(self, item_id):
        query = (self.session.query(Asset)
                  .filter(Asset.assetId==item_id)).first()
        if query is None:
            click.secho("\n\t\t\t No Such Item", fg = 'green', bold = True) 
        elif query.item_status:
            the_date = datetime.now().strftime('%Y-%m-%d %H:%M')
            self.session.add(Log(the_date, None, item_id))

            my_item = (self.session.query(Asset)
            .filter(Asset.assetId==item_id)
            .update({'item_status': False}))
            self.session.commit()

            click.secho("\n\t\t\t Checked Out Successfully", fg = 'green', bold = True) 
        else:
            click.secho("\n\t\t\t The Item Is Currently Checked Out", fg = 'green', bold = True) 
    def item_check_in(self, item_id):
        query = (self.session.query(Asset)
                  .filter(Asset.assetId==item_id)).first()
        if query is None:
            click.secho("\n\t\t\t No Such Item", fg = 'green', bold = True) 
        elif not query.item_status:
            my_item = (self.session.query(Log)
            .filter(Log.assetId==item_id)
            .update({'check_in_date': datetime.now().strftime('%Y-%m-%d %H:%M')}))

            (self.session.query(Asset)
            .filter(Asset.assetId==item_id)
            .update({'item_status': True}))
            self.session.commit()

            click.secho("\n\t\t\t Checked In Successfully", fg = 'green', bold = True) 
            
        else:
            click.secho("\n\t\t\t The Item Is Not Checked Out", fg = 'green', bold = True) 
    def item_view(self, item_id):
        rs = (self.session.query(Asset)
        .filter(Asset.assetId==item_id).first())
        self.session.commit()
        
        if rs is None:
            return
        
        logs = []
        for log in rs.logs:
            logs.append((log.logId ,log.check_out_date, log.check_in_date)) 
            
        return [rs.assetId, rs.item_name, rs.item_description,
                rs.item_amount_available, rs.cost_per_item, 
                rs.date_added, rs.item_status, logs]
        
    def assetvalue(self):
        total_value = 0
        rs = self.session.query(Asset.cost_per_item, Asset.item_amount_available).all()
        for item in rs:
            total_value= item.cost_per_item * item.item_amount_available + total_value
        return total_value
    
    def item_search(self, search_data):
        result_list = []
        search_pattern = '%{}%'.format(search_data)
        rs = (self.session.query(Asset)
              .filter(Asset.item_description.like(search_pattern)).all())
        for data in rs:
            result_list.append([data.assetId, data.item_name,
            data.item_amount_available, data.cost_per_item, 
            data.date_added, data.item_status])
            
        return result_list
    
    def db_state(self, filename = 'database'):
        '''
        Exports the current state of the database
        '''
        mydata = []
        rs = self.session.query(Asset).all()
        self.session.commit()
        for item in rs:
            mydata.append([item.assetId, item.item_name, item.item_description, item.item_amount_available,
            item.cost_per_item, item.date_added,
            item.item_status])
            
        
        with open(filename + '.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'item-name','description', 'amount_available', 'price', 'date_added', 'status'])
            writer.writerows(mydata)
        
        format_string = '\n\t\t\t{}  Successfully Created\n'.format(filename + '.csv')
        click.secho(format_string, fg = 'green', bold = True, underline = True)
   