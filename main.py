from fastapi import FastAPI
from fastapi.responses import HTMLResponse #Output HTML instead of default JSON
from fastapi.templating import Jinja2Templates
from fastapi import Request #Needed for Jinja2 templates
from fastapi import Depends
from fastapi import Form
from database.session import Base, engine
from database.session import get_db
from database import models
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

templates = Jinja2Templates(directory="templates") #Refers to templates folder to connect HTML files

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name = "static")

#To create tables inside network.db if they don't already exist
Base.metadata.create_all(bind=engine)

# " / " sets home page URL, "get" for user page visits
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request}) #index is industry standard for home page

# "/add" sets add contact page. Returns add.html template
@app.get("/add", response_class=HTMLResponse)
async def add_contact(request: Request):
    return templates.TemplateResponse("add.html", {"request": request})

#post route recieves data from the HTML post action  
@app.post("/add", response_class=HTMLResponse)
async def add_contact(
    name: str = Form(...), #FastAPI looks for HTML form data with these items
    date_met: str = Form(...), #Form(...) from FastAPI enforces requirement
    event: str = Form(...),
    interests: str = Form(...),
    email: str = Form(None),
    db: Session = Depends(get_db)  #parameter to call get_db() so db = sessionlocal can be used
): 
    #Contact from the models py file 
    new_contact = models.Contact(name=name, date_met=date_met, event=event, interests=interests, email=email)

    db.add(new_contact) #Prepare a new row in Contact table w/ the Contact class stored as new_contact
    db.commit() #Saves the new row
    return RedirectResponse(url="/contacts", status_code=303) #Redirect from POST to GET

@app.get("/contacts", response_class=HTMLResponse)
async def view_contacts(request:Request, db: Session = Depends(get_db)):
    connections = db.query(models.Contact).all() #SQL language to select * from the contacts table

    #passes the SQL querey ^^ into the template "contacts.html" for display
    return templates.TemplateResponse("contacts.html", {"request": request, "connections":connections}) #"connections" is for the html to recognize, :connections provides the info from the querey 

@app.post("/delete", response_class=HTMLResponse) #adding a post route to delete contacts 
async def delete_contact(contact_id: int = Form(...), db: Session = Depends(get_db)):
    connection = db.query(models.Contact).filter(models.Contact.id==contact_id).first()
    if connection:
        db.delete(connection) #deletes whats queried from the stored variable 
        db.commit()
    return RedirectResponse(url="/contacts", status_code=303)
    