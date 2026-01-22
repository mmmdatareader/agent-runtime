from fastapi import FastAPI, UploadFile, BackgroundTasks
import uuid
import time

app = FastAPI()

# In-memory job store
JOBS = {}

@app.post("/run")
async def run_job(file: UploadFile, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())

    JOBS[job_id] = {
        "status": "running",
        "current_agent": "queued",
        "trace": {}
    }

    background_tasks.add_task(process_job, job_id)
    return {"job_id": job_id}


def process_job(job_id: str):
    agents = ["load_file", "structure_analyzer", "plan_generator", "verifier"]

    for agent in agents:
        JOBS[job_id]["current_agent"] = agent
        JOBS[job_id]["trace"][agent] = {
            "status": "running",
            "start_time": time.time()
        }

        time.sleep(3)

        JOBS[job_id]["trace"][agent].update({
            "status": "completed",
            "end_time": time.time(),
            "output": f"{agent} output"
        })

    JOBS[job_id]["status"] = "completed"


@app.get("/status/{job_id}")
def get_status(job_id: str):
    return JOBS.get(job_id, {"error": "job not found"})
