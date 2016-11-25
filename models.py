from sqlalchemy import create_engine, ForeignKey, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.orm import sessionmaker, relationship


or_
eng = create_engine('sqlite:///inventory.db')
Base = declarative_base()
Base.metadata.bind = eng 
Session = sessionmaker(bind=eng)


class Asset(Base):
    '''
    This class creates Assets table which holds data for our items.
    Has a one to many relationship with the Logs table
    '''
    
    __tablename__ = "Assets"
 
    assetId = Column(Integer, primary_key=True)
    item_name = Column(String) 
    item_description = Column(String)
    item_amount_available = Column(Integer)
    cost_per_item = Column(Float)
    date_added = Column(String)
    item_status = Column(Boolean)

    logs = relationship("Log")

    def __init__(self, item_name, item_description, item_amount_available,
                 cost_per_item, item_date_added, item_status):
        
        self.item_name = item_name
        self.item_description = item_description
        self.item_amount_available = item_amount_available
        self.cost_per_item = cost_per_item
        self.date_added = item_date_added
        self.item_status = item_status

class Log(Base):
    '''
    This class creates logss table which tracks the check in, check out of an item.
    
    '''
    __tablename__ = "Logs"
 
    logId = Column(Integer, primary_key=True)
    check_out_date = Column(String)   
    check_in_date = Column(String)    
    assetId = Column(Integer, ForeignKey("Assets.assetId"))    
                           
    Assets = relationship("Asset")   

    def __init__(self, check_out_date, check_in_date, assetId):
        self.check_out_date =  check_out_date 
        self.assetId = assetId 
        self.check_in_date =  check_in_date
            
Base.metadata.create_all() 
