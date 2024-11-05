from fastapi import FastAPI
import uvicorn
from routers import task, user



app = FastAPI()



@app.get('/', tags=['Welcome'])
async def get_main_page():
    return {'message': 'Welcom to TaskManager'}

app.include_router(task.router)
app.include_router(user.router)



if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)