from models import  Asset, log, Session
from datetime import datetime
import click

class inventory(object):
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
        self.session.query(Asset.AssetId).filter(Asset.AssetId == item_id).delete()
        self.session.commit()
        
        click.secho("\n\t\t\tSuccessfully Removed", fg = 'green', bold = True) 
        
    def item_list(self):
        mydata = []
        rs = self.session.query(Asset).all()
        self.session.commit()
        for item in rs:
            mydata.append([item.AssetId, item.Item_name,
             item.Item_amount_available, item.Cost_per_item, item.Date_added,
             item.Item_status])
            
        return mydata
 
    def item_check_out(self, item_id):
        the_date = datetime.now().strftime('%Y-%m-%d %H:%M')
        self.session.add(log(the_date, None, item_id))
        self.session.commit()
        
        click.secho("\n\t\t\t Checked Out Successfully", fg = 'green', bold = True) 
        
    def item_check_in(self, item_id):
        my_item = (self.session.query(log)
        .filter(log.AssetId==item_id)
        .update({'Check_in_date': datetime.now().strftime('%Y-%m-%d %H:%M')}))
        self.session.commit()
        
        click.secho("\n\t\t\t Checked In Successfully", fg = 'green', bold = True) 
    
    def item_view(self, item_id):
        rs = (self.session.query(Asset)
        .filter(Asset.AssetId==item_id).one())
        self.session.commit()
        logs = []
        for log in rs.logs:
            logs.append((log.LogId ,log.Check_out_date, log.Check_in_date)) 
            
        return [rs.AssetId, rs.Item_name, rs.Item_description,
                rs.Item_amount_available, rs.Cost_per_item, 
                rs.Date_added, rs.Item_status, logs]
        
    def assetvalue(self):
        total_value = 0
        rs = self.session.query(Asset.Cost_per_item, Asset.Item_amount_available).all()
        for item in rs:
            total_value= item.Cost_per_item * item.Item_amount_available + total_value
        return total_value
    
    def item_search(self):
        result_list = []
        search_data = raw_input(click.style("\n\t\tEnter Your search request : ", fg = 'yellow'))
        search_pattern = '%{}%'.format(search_data)
        rs = (self.session.query(Asset)
              .filter(Asset.Item_description.like(search_pattern)).all())
        for data in rs:
            result_list.append([data.AssetId, data.Item_name,
            data.Item_amount_available, data.Cost_per_item, 
            data.Date_added, data.Item_status])
            
        return result_list
    
    