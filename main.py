from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="src/template")
app.mount("/static", StaticFiles(directory="src/static"), name="static")

@app.get('/')
def get_base(request:Request):
    return templates.TemplateResponse('registration.html', {'request':request})






