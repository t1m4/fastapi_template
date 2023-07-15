import sqlalchemy
from fastapi import APIRouter

from app import db
from app.types import StrDict

router = APIRouter()


@router.get(path='/health')
def health() -> StrDict:
    # check database with exception
    with db.connect() as conn:

        conn.execute(sqlalchemy.text('SELECT 1 = 1;'))

    return {'status': 'alive'}
