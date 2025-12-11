from sqlalchemy import Column, Integer, String
from .session import Base

class Contact(Base): #Creates the db table through  Base inheritance
    __tablename__ = "contacts" #Sets the SQL table name as contacts

    #Sets table columns with Column()
    id = Column(Integer, primary_key=True, index=True) #Primary_key=True to uniquely identify each row 
    name = Column(String(100), nullable=False)
    date_met = Column(String(50))
    event = Column(String(100))
    interests = Column(String(200))
    
    #Label for printed contact objects
    def __repr__(self):
        return f"<Contact {self.name}>"
