from models import  Asset, log, Session
from datetime import datetime

class inventory(object):
    def __init__(self, inventory):
        self.inventory = inventory
        self.ses = Session()
        
    def item_add(self):
        print "\t\t\tItem Details"
        
        item_name = raw_input("\t\tName : ")
        item_description = raw_input('\t\tDescription : ')
        item_quantity = raw_input('\t\tQuantity : ')
        cost_per_item = raw_input("\t\tCost Per Item : ")
        date_added = datetime.utcnow()
        item_status = True
        
        self.ses.add(Asset(item_name, item_description, item_quantity, 
                    cost_per_item, date_added,  item_status))
        self.ses.commit()
        
        print "\t\t\tSuccessfully Added"
        
    def item_remove(self, item_id):
        self.ses.query(Asset.AssetId).filter(Asset.AssetId == item_id).delete()
        self.ses.commit()
        
        
    def item_list(self):
        mydata = []
        rs = self.ses.query(Asset).all()
        self.ses.commit()
        for item in rs:
            mydata.append([item.AssetId, item.Item_name, item.Item_description,
             item.Item_amount_available, item.Cost_per_item, item.Date_added,
             item.Item_status])
            
        return mydata
 
    def item_check_out(self, item_id):
        self.ses.add(log(datetime.utcnow(), None, item_id))
        self.ses.commit()
    def item_check_in(self, item_id):
        the_item = self.ses.query( log.Check_in_date).filter_by(log.AssetId==item_id).update()
        the_item.Check_in_date = datetime.utcnow()
        self.ses.commit()
    
    def item_view(self):
        pass
    
    def assetvalue(self):
        pass
    
    def item_search(self, item):
        pass
    
    def update_log(self, item_id):
        ads=Asset('Manu','Bootcamp process', 400, 500,100, datetime.utcnow(), True)
        ads = log(datetime.utcnow(), datetime.utcnow(), 1)
        
        self.ses.add(ads)
        self.ses.commit()   

        
asd = inventory('my inventory')
asd.item_check_in(1)

    
