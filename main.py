from typing import Annotated
from fastapi import FastAPI, File, UploadFile
import os
from starlette.middleware.cors import CORSMiddleware
from uuid import uuid4
from b64uuid import B64UUID
from datetime import datetime

app = FastAPI()
origins = [
    "*", # 추후 프론트엔드 주소/포트로 변경
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

categories = ['board']

@app.post("/upload/{category}")
async def upload(category:str, file: Annotated[UploadFile, File(description="업로드할 파일")]):
    if category not in categories:
        return { "error" : "허용되지 않은 카테고리"}
    content = await file.read()
    file_name = str(B64UUID(uuid4())).upper() + os.path.splitext(file.filename)[-1]
    year = datetime.now().strftime("%Y")
    month = datetime.now().strftime("%m")
    day = datetime.now().strftime("%d")
    path = f"data/{category}/{year}/{month}/{day}"
    svfile = path + f"/{file_name}"
    if not os.path.exists(path):
        os.makedirs(path)
    with open(svfile, "wb") as f:
        f.write(content)
    f.close()
    return { "filename" : svfile.replace("data/","")}



#서버 이전시에는 ./data/user 에 있는 파일들의 소유권을 이 코드실행 소유자(예:woori2)로 변경해 줘야 함
@app.post("/portraitupload/{userid}")
async def portrait_upload(userid:str, file: Annotated[UploadFile, File(description="업로드할 파일")]):
    content = await file.read()
    file_name = str(userid).upper() + os.path.splitext(file.filename)[-1]

    svfile = "data/user" + f"/{file_name}"
    with open(svfile, "wb") as f:
        f.write(content)
    f.close()
    return { "filename" : svfile.replace("data/", "")}