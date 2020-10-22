from fastapi import FastAPI, HTTPException
from zipfile import ZipFile
from user_info import UserInfo

user_info = UserInfo()

tags_metadata = [
    {
        "name": "user",
        "description": "Get information about a particular user"
    }
]

app = FastAPI(title="Take Home",
              description="testing",
              version="0.0.1",
              openapi_tags=tags_metadata)


@app.on_event("startup")
async def startup_event():
    file_name = "Input.zip"

    # opening the zip file in READ mode
    with ZipFile(file_name, 'r') as zip:
        for info in zip.infolist():
            if info.filename.endswith('.csv'):
                zip.extract(info.filename)
                user_info.load_data(info.filename)


@app.get('/')
async def index():
    return {
        "name": "take home",
        "description": "testing api",
        "api": [{
            "uri": "/",
            "methods": ["GET"],
            "description": "Describes the service"
        },
            {
                "uri": "user/{user_id}",
                "methods": ["GET"],
                "description": "Get user information."
            }
        ]
    }


@app.get('/user/{user_id}', status_code=200, tags=["user"])
async def get_user_info(user_id: str):
    if user_id is None:
        raise HTTPException(502, 'Error getting user information')
    return user_info.get_user_info(user_id)

