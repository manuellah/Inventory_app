from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

eng = create_engine('sqlite:///inventory.db')
Base = declarative_base()
Session = sessionmaker(bind=eng)
ses = Session()   
 
class Asset(Base):
    __tablename__ = "Assets"
 
    AssetId = Column(Integer, primary_key=True)
    Item_name = Column(String) 
    Item_description = Column(String)
    Item_total = Column(Integer)
    Item_available_ammount = Column(Integer)
    Item_cost_per_item = Column(Float)
    Item_date_added = Column(DateTime)
    Item_status = Column(Boolean)

    logs = relationship("log")

    def __init__(self, Item_name, Item_description, Item_total, Item_available_ammount,
    			Item_cost_per_item, Item_date_added, Item_status):
        
        self.Item_name = Item_name
        self.Item_description = Item_description
        self.Item_total = Item_total
        self.Item_available_ammount = Item_available_ammount
        self.Item_cost_per_item = Item_cost_per_item
        self.Item_date_added = Item_date_added
        self.Item_status = Item_status

class log(Base):
    __tablename__ = "logs"
 
    LogId = Column(Integer, primary_key=True)
    Check_out_date = Column(DateTime)   
    Check_in_date = Column(DateTime)    
    AssetId = Column(Integer, ForeignKey("Assets.AssetId"))    
                           
    Assets = relationship("Asset")   

    def __init__(self, Check_out_date, Check_in_date, AssetId):
    	 self.Check_out_date =  Check_out_date     
    	 self.Check_in_date =   Check_in_date  
    	 self.AssetId = AssetId           
         
Base.metadata.bind = eng        
Base.metadata.create_all() 

#ads=Asset('Manu','Bootcamp process', 400, 500,100, datetime.utcnow(), True)
ads = log(datetime.utcnow(), datetime.utcnow(), 1)
ses.add(ads)
ses.commit()   
