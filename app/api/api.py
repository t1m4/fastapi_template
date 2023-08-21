from fastapi import APIRouter

from app.api.routes.v1 import address_api as address_api_v1
from app.api.routes.v1 import health
from app.api.routes.v1 import user_api as user_v1

router = APIRouter(tags=['API'], prefix='/api')

router.include_router(health.router, tags=['health'])
router.include_router(user_v1.router, tags=['user'])
router.include_router(address_api_v1.router, tags=['address'])
