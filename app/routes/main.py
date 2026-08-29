from flask import Blueprint, render_template, request

from app.models import CATEGORIES, Event
from app.utils import get_weather

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
@main_bp.route("/events")
def index():
    category = request.args.get("category", "").strip()
    sort = request.args.get("sort", "newest")

    query = Event.query
    if category and category in CATEGORIES:
        query = query.filter_by(category=category)

    if sort == "oldest":
        query = query.order_by(Event.created_at.asc())
    elif sort == "date_asc":
        query = query.order_by(Event.date.asc())
    elif sort == "date_desc":
        query = query.order_by(Event.date.desc())
    else:  # "newest" — default, by posting date
        query = query.order_by(Event.created_at.desc())

    page = request.args.get("page", 1, type=int)
    pagination = query.paginate(page=page, per_page=9, error_out=False)

    return render_template(
        "index.html",
        events=pagination.items,
        pagination=pagination,
        categories=CATEGORIES,
        current_category=category,
        current_sort=sort,
    )


@main_bp.route("/about")
def about():
    return render_template("about.html")


@main_bp.route("/event/<int:event_id>")
def event_detail(event_id):
    event = Event.query.get_or_404(event_id)
    weather = get_weather(event.location)
    return render_template("event_detail.html", event=event, weather=weather)
