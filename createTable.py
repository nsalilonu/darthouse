from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String


DATABASE_NAME = "postgresql://gkxpqzrwjotsih:9b075c957964638c446f351394517675e40f7ae30ee2997a6b72bc5ec0280114@ec2-3-211-221-185.compute-1.amazonaws.com:5432/dbpk5mu96m82v"
engine = create_engine(DATABASE_NAME, echo = True)
meta = MetaData()

reviews = Table(
   'reviews', meta, 
   Column('request_id', String, primary_key = True), 
   Column('address', String, nullable=False), 
   Column('start_date', String, nullable=False),
   Column('end_date', String, nullable=False),
   Column('cleanliness', String),
   Column('cleanliness_comments', String),
   Column('noise', String),
   Column('noise_comments', String),
   Column('responsive', String),
   Column('responsive_comments', String),
   Column('landlord', String),
   Column('landlord_comments', String),
   Column('pest', String),
   Column('pest_comments', String),
   Column('safety', String),
   Column('safety_comments', String),
   Column('appliance', String),
   Column('appliance_comments', String),
   Column('transportBool', Integer),
   Column('transport', String),
   Column('transport_comments', String),
   Column('furnishedBool', Integer),
   Column('furnished', String),
   Column('furnished_comments', String),
   Column('utility', Integer),
   Column('final_thoughts', String)
)
meta.create_all(engine)
