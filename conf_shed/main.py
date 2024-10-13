from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from conf_shed.config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS
from models import Presentation, Shedule, Room


app = FastAPI()


SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autoflush=False, bind=engine)
db = SessionLocal()


templates = Jinja2Templates(directory="templates")


@app.get('/', response_class=HTMLResponse)
@app.get('/index', response_class=HTMLResponse)
def index(request: Request):
    number = '1'
    return templates.TemplateResponse(request=request, name="index.html", context={"number": number})


@app.get('/reg', response_class=HTMLResponse)
def reg(request: Request):
    return templates.TemplateResponse(request=request, name="reg.html")


@app.post('/regsuc', response_class=HTMLResponse)
def regsuc(request: Request, name=Form(), pr_id=Form()):
    pres = db.query(Shedule).filter(Shedule.pr_id == int(pr_id)).first()
    if pres.listeners == None:
        pres.listeners = f"{name}"
    else:
        pres.listeners = f"{pres.listeners}\r\n{name}"
    db.commit()
    return templates.TemplateResponse(request=request, name="regsuc.html", context={'name':name, 'pr_id':pr_id})


@app.get('/pr-reg', response_class=HTMLResponse)
def reg(request: Request):
    return templates.TemplateResponse(request=request, name="pr-reg.html")


@app.post('/api/pr-edit/{prid}', response_class=HTMLResponse) #crUd
def pr_view(prid, name=Form(), presenter=Form(), time=Form(), room_num=Form()):
    pres = db.query(Presentation).filter(Presentation.id == int(prid)).first()
    shed_pr = db.query(Shedule).filter(Shedule.pr_id == int(prid)).first()
    block = db.query(Shedule).filter(Shedule.time == str(time), Shedule.room_id == int(room_num)).first()
    if block == None:
        pres.name = name
        pres.presenter = presenter
        pres.time = time
        shed_pr.pr_name = name
        shed_pr.presenter = presenter
        shed_pr.room_id = int(room_num)
        shed_pr.time = time
        db.commit()
    else:
        return "Время или аудитория уже занято!!"

    return "Изменения внесены!"


@app.post('/presentors-pr-list/{prs_name}') #cRud
def presentors_pr_list(prs_name):
    pres_list = db.query(Shedule).filter(Shedule.presenter == str(prs_name)).all()
    return pres_list


@app.post('/pr-delete/{prid}') #cruD
def pr_delete(prid):
    pres_shed = db.query(Shedule).filter(Shedule.pr_id == int(prid)).first()
    pres_pr = db.query(Presentation).filter(Presentation.id == int(prid)).first()
    if pres_pr == None:
        return {"message": "Отсутствует презентация с таким номером!"}
    else:
        db.delete(pres_shed)
        db.delete(pres_pr)
        db.commit()
        return {"message": "Запись успешно удалена!"}


@app.get('/pr-view', response_class=HTMLResponse)
def pr_view(request: Request):
    return templates.TemplateResponse(request=request, name="pr-view.html")


@app.post('/api/pr-view/{prid}') #просмотр презентации для слушателей
def reg(prid):
    pres = db.query(Presentation).filter(Presentation.id == int(prid)).first()
    return pres


@app.post('/pr-regsuc', response_class=HTMLResponse) #Crud
def pr_regsuc(request: Request, pr_name=Form(), presenter=Form(), time=Form(), room_num=Form()):
    block = db.query(Shedule).filter(Shedule.time == str(time), Shedule.room_id == int(room_num)).first()
    if block == None:
        new_pr = Presentation(name=pr_name, presenter=presenter, time=time)
        db.add(new_pr)
        db.commit()
        new_shed = Shedule(pr_id=new_pr.id, pr_name=pr_name, presenter=presenter, room_id=int(room_num), time=time)
        db.add(new_shed)
        db.commit()
    else:
        return "Выберите другое время или аудиторию"
    return templates.TemplateResponse(request=request, name="pr-regsuc.html", context={'shed':new_shed.id, 'time':time, 'room':room_num})


@app.get('/confshed', response_class=HTMLResponse)
def confshed(request: Request):
    return templates.TemplateResponse(request=request, name="confshed.html")


@app.get('/api/confshed/{num}')
def api_confshed1(num):
    try:
        confs = db.query(Shedule).filter(Shedule.room_id == int(num)).all()
        #REST api
        return {
            "status": "success",
            "data": confs,
            "details": None
        }
    except:
        return {
            "status": "error",
            "data": None,
            "details": "Ошибка базы данных."
        }

