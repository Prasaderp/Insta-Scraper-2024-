from fastapi import FastAPI, HTTPException, BackgroundTasks, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from scraper import scrape_profile, scrape_hashtag_posts, initialize_driver, quit_driver
from database import profile_col, hashtag_posts_col
from starlette.requests import Request
import logging

app = FastAPI()
templates = Jinja2Templates(directory="templates")


# Setup logging
logging.basicConfig(level=logging.INFO)

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/profile", response_class=HTMLResponse)
def get_profile(request: Request, background_tasks: BackgroundTasks, username: str = Form(...), is_private: bool = Form(False)):
    driver = initialize_driver()
    background_tasks.add_task(quit_driver, driver)
    try:
        profile_data = scrape_profile(username, is_private, driver)
        return templates.TemplateResponse("profile.html", {"request": request, "profile_data": profile_data})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/hashtag", response_class=HTMLResponse)
def get_hashtag_posts(request: Request, background_tasks: BackgroundTasks, hashtag: str = Form(...)):
    driver = initialize_driver()
    background_tasks.add_task(quit_driver, driver)
    try:
        post_data = scrape_hashtag_posts(hashtag, driver)
        return templates.TemplateResponse("hashtag.html", {"request": request, "post_data": post_data})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Serve static files (CSS, JS, images)
app.mount("/static", StaticFiles(directory="static"), name="static")
