from fastapi import FastAPI
from fastapi.responses import HTMLResponse #Output HTML instead of default JSON
from fastapi.templating import Jinja2Templates
from fastapi import Request #Needed for Jinja2 templates
from fastapi import Depends
from fastapi import form
from database.session import Base, engine
from database.session import get_db
from database import models
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse



templates = Jinja2Templates(directory="templates") #Refers to template folder to connect HTML files

app = FastAPI()

#To create tables inside network.db if they don't already exist
Base.metadata.create_all(bind=engine)

# " / " sets home page URL, "get" for user page visits
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# "/add" sets add contact page. Returns add.html template
@app.get("/add", response_class=HTMLResponse)
async def add_contact(request: Request):
    return templates.TemplateResponse("add.html", {"request": request})

#post route sends data 
@app.post("/add", response_class=HTMLResponse)
async def add_contact(
    name: str = Form(...), #FastAPI looks for HTML form data with these items
    date_met: str = Form(...), #Form(...) from FastAPI enforces requirement
    event: str = Form(...),
    interests: str = Form(...),
    db: Session = Depends(get_db) 
): 
    #declaring variable as Contact from the models py file 
    new_contact = models.Contact(
        name=name,
        date_met=date_met,
        event=event,
        interests=interests
    )
    db.add(new_contact) #Prepare a new row in Contact table
    db.commit() #Saves the new row
    return RedirectResponse(url="/contacts", status_code=303) #Redirect from POST to GET