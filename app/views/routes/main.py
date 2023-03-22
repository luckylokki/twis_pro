from flask import render_template, redirect, url_for, flash, request, abort, Blueprint
from flask_login import login_required, current_user
from sqlalchemy import desc
from app import db
from app.forms import TwisForm
from app.models import get_current_timestamp, TwisModel

main = Blueprint('main', __name__)


@main.route("/")
def twis_list():
    """List all messages route"""
    if current_user.is_authenticated:
        object_list = TwisModel.query.order_by(desc(TwisModel.date)).all()
    else:
        return redirect(url_for("users.signin"))

    return render_template("twis_list.html", object_list=object_list)


@main.route("/my_twises/", methods=["GET", "POST"])
@login_required
def twis_my_list():
    """List all current user messages route"""
    if current_user.is_authenticated:
        object_list = current_user.twises
    else:
        return redirect(url_for("users.signin"))

    return render_template("twis_list.html", object_list=object_list)


@main.route("/create/", methods=["GET", "POST"])
@login_required
def twis_create():
    """Create new message route"""
    form = TwisForm()
    if request.method == "POST":
        db.session.add(
            TwisModel(
                value=form.twis_text.data,
                date=get_current_timestamp().replace(microsecond=0).isoformat(' '),
                user_name=current_user.username,
                user_id=current_user.id
            )
        )
        db.session.commit()
        flash("New message added", "success")
        return redirect(url_for("main.twis_list"))

    return render_template("twis_form.html", form=form)


@main.route("/update/<int:pk>", methods=["GET", "POST"])
@login_required
def twis_update(pk: int):
    """Update message route"""
    twis: TwisModel = TwisModel.query.get_or_404(pk)
    form = TwisForm(obj=twis)
    if request.method == "POST":
        twis.value = form.twis_text.data
        twis.date_update = get_current_timestamp().replace(microsecond=0).isoformat(' ')
        db.session.add(twis)
        db.session.commit()
        flash("Time report has been updated", "success")

        return redirect(url_for("main.twis_list"))

    return render_template("twis_form.html", form=form)


@main.route("/delete/<int:pk>", methods=["GET", "POST"])
@login_required
def twis_delete(pk: int):
    """Delete message route"""
    twis: TwisModel = TwisModel.query.get_or_404(pk)

    if twis.user_id != current_user.id:
        abort(403)

    if request.method == "POST":
        db.session.delete(twis)
        db.session.commit()
        flash("Twis has been deleted", "success")

        return redirect(url_for("main.twis_list"))

    return render_template("twis_delete.html", object=twis)
