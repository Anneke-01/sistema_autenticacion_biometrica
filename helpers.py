import csv
import os
import urllib.request

from flask import redirect, render_template, request, session
from functools import wraps
from sqlalchemy import text, select
from flask_paginate import Pagination

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def pagination(db,count_query, data_query, per_page=6):
    page_num = request.args.get("page", 1, type=int)
    offset = (page_num - 1) * per_page

    total = db.execute(
        text(count_query)
    ).scalar()

    rows = db.execute(
        text(data_query),
        {
            "limit": per_page,
            "offset": offset
        }
    ).mappings().all()

    start_index = offset + 1 if total > 0 else 0
    end_index = min(offset + per_page, total)

    pager = Pagination(
        page=page_num,
        total=total,
        per_page=per_page,
        display_msg=(
            f"Mostrando registros {start_index} - {end_index} "
            f"de un total de <strong>({total})</strong>"
        )
    )

    return rows, pager