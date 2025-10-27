import os
from typing import Any, Dict
from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

import psycopg
from psycopg.rows import dict_row
from settings import settings

router = APIRouter()

templates = Jinja2Templates(directory=os.path.join("AEYE_langchain/interface/v1"))

def fetch_db_status() -> Dict[str, Any]:
    dsn = settings.PG_CON
    
    data: Dict[str, Any] = {}

    with psycopg.connect(dsn, row_factory=dict_row) as conn:
        with conn.cursor() as cur:

            cur.execute("SHOW server_version;")
            data["server_version"] = cur.fetchone()["server_version"]

            cur.execute("SELECT current_user AS user, current_database() AS database;")
            data["session"] = cur.fetchone()

            # 데이터베이스 목록 + 사이즈
            cur.execute("""
                SELECT datname AS name,
                       pg_size_pretty(pg_database_size(datname)) AS size
                FROM pg_database
                WHERE datistemplate = false
                ORDER BY datname;
            """)
            data["databases"] = cur.fetchall()

            # 역할(롤) 목록
            cur.execute("""
                SELECT rolname,
                       rolsuper,
                       rolcreatedb,
                       rolcanlogin
                FROM pg_roles
                ORDER BY rolname;
            """)
            data["roles"] = cur.fetchall()

            # 현재 DB의 확장 목록
            cur.execute("""
                SELECT e.extname, e.extversion, n.nspname AS schema
                FROM pg_extension e
                JOIN pg_namespace n ON e.extnamespace = n.oid
                ORDER BY e.extname;
            """)
            data["extensions"] = cur.fetchall()

            # public 스키마 테이블
            cur.execute("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                  AND table_type = 'BASE TABLE'
                ORDER BY table_name;
            """)
            data["tables"] = [r["table_name"] for r in cur.fetchall()]

            # 현재 DB의 활성 세션
            cur.execute("""
                SELECT pid, usename, datname, state, client_addr,
                       backend_start, query_start,
                       LEFT(query, 120) AS query
                FROM pg_stat_activity
                WHERE datname = current_database()
                ORDER BY query_start DESC NULLS LAST
                LIMIT 20;
            """)
            data["activity"] = cur.fetchall()

    return data


@router.get("/db", response_class=HTMLResponse)
async def db_dashboard(request: Request):
    try:
        status = fetch_db_status()
        return templates.TemplateResponse("db.html", {"request": request, "status": status, "error": None})
    except Exception as e:
        return templates.TemplateResponse("db.html", {"request": request, "status": {}, "error": str(e)})

@router.get("/db.json")
async def db_json():
    try:
        status = fetch_db_status()
        return JSONResponse(status)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
