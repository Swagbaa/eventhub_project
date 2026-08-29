from flask import Blueprint, current_app, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from app.extensions import db
from app.forms import ProfileForm
from app.models import Event, User
from app.utils import logger, save_profile_picture

profile_bp = Blueprint("profile", __name__)


@profile_bp.route("/profile")
@login_required
def profile():
    events = (
        Event.query.filter_by(author_id=current_user.id).order_by(Event.created_at.desc()).all()
    )
    return render_template("profile.html", user=current_user, events=events, is_own=True)


@profile_bp.route("/profile/edit", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = ProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.name = form.name.data.strip()
        current_user.email = form.email.data.lower().strip()

        if form.picture.data:
            filename = save_profile_picture(form.picture.data, current_app.config["UPLOAD_FOLDER"])
            current_user.profile_image = filename

        db.session.commit()
        logger.info("Profile updated: %s", current_user.email)
        flash("პროფილი განახლდა.", "success")
        return redirect(url_for("profile.profile"))

    return render_template("edit_profile.html", form=form)


@profile_bp.route("/user/<int:user_id>")
def public_profile(user_id):
    user = User.query.get_or_404(user_id)
    events = Event.query.filter_by(author_id=user.id).order_by(Event.created_at.desc()).all()
    is_own = current_user.is_authenticated and current_user.id == user.id
    return render_template("profile.html", user=user, events=events, is_own=is_own)
