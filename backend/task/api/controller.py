from celery.result import AsyncResult
from fastapi import APIRouter

from backend.task.worker import celery, get_ip_details

from ..models import UserIpDetail
from ..schemas import UserIp

router = APIRouter()


@router.post(
    "/task",
    tags=["create task"],
    description="Create task using the IP address",
)
async def create_task(ip: UserIp):
    task = get_ip_details.delay(ip.address)
    result = task.get()
    ip_detail_obj = UserIpDetail(ip=ip.address, details=result)
    ip_detail_obj.save()

    return {"task_id": task.id}


@router.get(
    "/status/{id}",
    tags=["get task by id"],
    description="Get task status by celery task id",
)
async def check_task_status(id: str):
    result = AsyncResult(id, app=celery)
    return {"status": result.state}
