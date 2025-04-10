import json
import uuid
from fastapi import APIRouter, Request, BackgroundTasks
from fastapi import File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from app.core import ai_analyze
from app.api.deps import buffer
from AtlantSDK.utils.clear_md import clean_text

router = APIRouter()
tasks = {}


@router.post("/upload_pdf")
async def upload_pdf(r: Request, file: UploadFile = File(...)):
    # Проверка типа файла
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400, 
            detail="Invalid file type. Only PDF files are allowed."
        )

    try:
        # Чтение содержимого файла
        contents = await file.read()
        filename = file.filename.replace(" ", "_")
        with open(f"uploads/{filename}", "wb") as f:
            f.write(contents)
        
        return JSONResponse(
            status_code=200,
            content={
                "filename": filename,
                "size": len(contents),
                "content_type": file.content_type
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"message": f"Error processing file: {str(e)}"}
        )
    finally:
        await file.close()


@router.get('/analyze_pdf')
async def analyze_pdf_file(r: Request, name: str, bg_tasks: BackgroundTasks = BackgroundTasks()):
    task_id = str(uuid.uuid4())
    bg_tasks.add_task(ai_analyze.dp.proccess_update, {"command": "START", "args": f"uploads/{name} {task_id}"}, "CORE")
    
    tasks[task_id] = {
        "status": "processing",
        "progress": 0,
        "result": None
    }
    return {"task_id": task_id}


@router.get("/check_status")
async def check_status(task_id: str):
    task = buffer.get(task_id)

    if not task:
        return {
            "status": "progress",
            "progress": 50,
            "result": None
        } 

    return  {
        "status": "completed",
        "progress": 100,
        "result": json.loads(clean_text(task.replace("json", "")))
    } 


@router.get("/get_chapter")
async def get_chapter(task_id: str, chapter: int):
    task = buffer.get(task_id)
    chapters_content = json.loads(clean_text(task.replace("json", ""))).get("chapters_content")
    res = chapters_content[chapter].replace("\n", "<br>").replace('"', "")
    return res