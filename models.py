from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.orm import sessionmaker, relationship


eng = create_engine('sqlite:///inventory.db')
Base = declarative_base()
Base.metadata.bind = eng 
Session = sessionmaker(bind=eng)


class Asset(Base):
    __tablename__ = "Assets"
 
    AssetId = Column(Integer, primary_key=True)
    Item_name = Column(String) 
    Item_description = Column(String)
    Item_amount_available = Column(Integer)
    Cost_per_item = Column(Float)
    Date_added = Column(String)
    Item_status = Column(Boolean)

    logs = relationship("log")

    def __init__(self, Item_name, Item_description, Item_amount_available,
                 Cost_per_item, Item_date_added, Item_status):
        
        self.Item_name = Item_name
        self.Item_description = Item_description
        self.Item_amount_available = Item_amount_available
        self.Cost_per_item = Cost_per_item
        self.Date_added = Item_date_added
        self.Item_status = Item_status

class log(Base):
    __tablename__ = "logs"
 
    LogId = Column(Integer, primary_key=True)
    Check_out_date = Column(String)   
    Check_in_date = Column(String)    
    AssetId = Column(Integer, ForeignKey("Assets.AssetId"))    
                           
    Assets = relationship("Asset")   

    def __init__(self, Check_out_date, Check_in_date, AssetId):
        self.Check_out_date =  Check_out_date 
        self.AssetId = AssetId 
        self.Check_in_date =   Check_in_date
            
Base.metadata.create_all() 

#ads=Asset('Manu','Bootcamp process', 400, 500,100, datetime.utcnow(), True)
#ads = log(datetime.utcnow(), datetime.utcnow(), 1)
#ses.add(ads)

#ses= Session()
#print ses.query(Asset.Item_name, Asset.Item_description).all()
