from flask import Blueprint, request, flash, redirect, url_for, render_template
from flask_login import login_required, current_user
from subify.sub.forms import NewSubForm
from subify import database
from subify.models import Sub
from sqlalchemy import func

sub = Blueprint('sub', __name__)


@sub.route('/addsub', methods=['GET', 'POST'])
@login_required
def add_sub():
    add_sub_form = NewSubForm(request.form)
    if add_sub_form.validate_on_submit() and request.method == 'POST':
        name = add_sub_form.name.data
        type = add_sub_form.type.data
        occurance_type = add_sub_form.occurance_type.data
        price = add_sub_form.price.data
        is_paid = False

        sub = Sub.query.filter(
            func.upper(Sub.name) == name.upper(),
            func.upper(Sub.user_id) == func.upper(current_user.name),
            func.upper(Sub.occurance_type != 'onetime')
        ).first()

        if sub:
            flash("You already have this expense as renewable!")
            return redirect(url_for('sub.addsub'))

        database.session.add(Sub(
            name=name,
            type=type,
            occurance_type=occurance_type,
            price=price,
            is_paid=is_paid,
            user_id=current_user.name
        ))

        database.session.commit()

        flash("Successfully added!", category="success")
        return redirect(url_for('sub.dashboard'))
    return render_template('addsub.html', form=add_sub_form)


@sub.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    subs = Sub.query.filter_by(user_id=current_user.name, is_paid=False).all()
    return render_template('dashboard.html', subs=subs)


@sub.route('/filtersubs')
@login_required
def filtersubs():
    filter = request.args.get('filter')
    if filter is not None:
        if filter == 'Paid':
            subs = Sub.query.filter_by(user_id=current_user.name, is_paid=True).all()
            if len(subs) == 0:
                subs = None
        else:
            subs = Sub.query.filter_by(user_id=current_user.name, is_paid=False).filter(
                Sub.type.icontains(filter)).all()
            if len(subs) == 0:
                subs = None
    else:
        subs = Sub.query.filter_by(user_id=current_user.name, is_paid=True).all()
        if len(subs) == 0:
            subs = None

    return render_template('dashboard-filtered.html', subs=subs)
