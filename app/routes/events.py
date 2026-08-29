from flask import Blueprint, abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from app.extensions import db
from app.forms import EventForm
from app.models import Event
from app.utils import logger

events_bp = Blueprint("events", __name__)


def _populate_event_from_form(event, form):
    event.title = form.title.data.strip()
    event.short_description = form.short_description.data.strip()
    event.full_description = form.full_description.data.strip()
    event.location = form.location.data.strip()
    event.date = form.date.data
    event.ticket_price = form.ticket_price.data or 0
    event.organizer = form.organizer.data.strip()
    event.category = form.category.data


@events_bp.route("/event/add", methods=["GET", "POST"])
@login_required
def add_event():
    form = EventForm()
    if form.validate_on_submit():
        event = Event(author_id=current_user.id)
        _populate_event_from_form(event, form)
        db.session.add(event)
        db.session.commit()
        logger.info("Event created: id=%s title=%r by %s", event.id, event.title, current_user.email)
        flash("ღონისძიება წარმატებით დაემატა!", "success")
        return redirect(url_for("main.event_detail", event_id=event.id))

    return render_template("add_event.html", form=form)


@events_bp.route("/event/<int:event_id>/edit", methods=["GET", "POST"])
@login_required
def edit_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.author_id != current_user.id:
        logger.warning(
            "Blocked unauthorized edit attempt: event id=%s by %s", event_id, current_user.email
        )
        abort(403)

    form = EventForm(obj=event)
    if form.validate_on_submit():
        _populate_event_from_form(event, form)
        db.session.commit()
        logger.info("Event updated: id=%s by %s", event.id, current_user.email)
        flash("ღონისძიება წარმატებით განახლდა.", "success")
        return redirect(url_for("main.event_detail", event_id=event.id))

    return render_template("edit_event.html", form=form, event=event)


@events_bp.route("/event/<int:event_id>/delete", methods=["POST"])
@login_required
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.author_id != current_user.id:
        logger.warning(
            "Blocked unauthorized delete attempt: event id=%s by %s", event_id, current_user.email
        )
        abort(403)

    logger.info("Event deleted: id=%s title=%r by %s", event.id, event.title, current_user.email)
    db.session.delete(event)
    db.session.commit()
    flash("ღონისძიება წაიშალა.", "info")
    return redirect(url_for("main.index"))
