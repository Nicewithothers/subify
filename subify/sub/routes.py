"""Imports"""
from json import dumps
from flask import Blueprint, request, flash, redirect, url_for, render_template
from flask_login import login_required, current_user
from plotly import graph_objects as go, utils as ut
from sqlalchemy import func
from subify.models import Sub
from subify.sub.forms import NewSubForm
from subify import database

sub = Blueprint('sub', __name__)


@sub.route('/addsub', methods=['GET', 'POST'])
@login_required
def add_sub():
    """New subb addition"""
    add_sub_form = NewSubForm(request.form)
    if add_sub_form.validate_on_submit() and request.method == 'POST':
        name = add_sub_form.name.data
        sub_type = add_sub_form.type.data
        occurance_type = add_sub_form.occurance_type.data
        price = add_sub_form.price.data
        is_paid = False

        existing_sub_onetime = Sub.query.filter(
            func.upper(Sub.name) == name.upper(),
            func.upper(Sub.user_id) == func.upper(current_user.name),
            func.upper(Sub.occurance_type != 'onetime')
        ).first()

        if existing_sub_onetime:
            flash("You already have this expense as renewable!")
            return redirect(url_for('sub.addsub'))

        database.session.add(Sub(
            name=name,
            type=sub_type,
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
    """Dashboard route"""
    subs = Sub.query.filter_by(user_id=current_user.name, is_paid=False).all()
    return render_template('dashboard.html', subs=subs)


@sub.route('/filtersubs')
@login_required
def filtersubs():
    """Filter subs"""
    type_filter = request.args.get('filter')
    if type_filter != "":
        match type_filter:
            case "Unpaid":
                subs = Sub.query.filter_by(user_id=current_user.name,
                                           is_paid=False).all()
                if len(subs) == 0:
                    subs = None
            case "Paid":
                subs = Sub.query.filter_by(user_id=current_user.name,
                                           is_paid=True).all()
                if len(subs) == 0:
                    subs = None
            case _:
                subs = Sub.query.filter_by(user_id=current_user.name).filter(
                    Sub.type.icontains(type_filter)).all()
                if len(subs) == 0:
                    subs = None
    else:
        subs = Sub.query.filter_by(user_id=current_user.name).all()
        if len(subs) == 0:
            subs = None

    return render_template('dashboard-filtered.html', subs=subs)


@sub.route('/deletesub/<sub_id>', methods=['POST'])
@login_required
def deletesub(sub_id):
    """Sub delete route"""
    targeted_sub = Sub.query.get(sub_id)

    if targeted_sub is not None:
        database.session.delete(targeted_sub)
        database.session.commit()
    else:
        flash("Sub not found.", category="error")
        return redirect(url_for('sub.dashboard'))

    flash("Successfully deleted!", category="success")
    return redirect(url_for('sub.dashboard'))


@sub.route('/paysub/<sub_id>', methods=['POST'])
@login_required
def paysub(sub_id):
    """Sub pay route"""
    targeted_sub = Sub.query.get(sub_id)
    print(targeted_sub)
    if targeted_sub is not None:
        targeted_sub.is_paid = True
        database.session.commit()
        flash("Successfully paid!", category="success")
        return redirect(url_for('sub.dashboard'))


@sub.route('/stat', methods=['GET', 'POST'])
@login_required
def stat():
    """Stat route with data"""
    paid_subs = Sub.query.filter_by(user_id=current_user.name,
                                    is_paid=True).count()
    unpaid_subs = Sub.query.filter_by(user_id=current_user.name,
                                      is_paid=False).count()

    first_fig_base = go.Pie(labels=["Paid subs", "Unpaid subs"],
                            values=[paid_subs, unpaid_subs])
    first_fig = dumps(
        go.Figure(data=[first_fig_base])
        .update_layout(paper_bgcolor='rgba(0,0,0,0)',
                       plot_bgcolor='rgba(0,0,0,0)')
        .update_traces(showlegend=False),
        cls=ut.PlotlyJSONEncoder)

    paid_subs_money = (database.session.query(func.sum(Sub.price))
                       .filter_by(user_id=current_user.name, is_paid=True)
                       .scalar())
    unpaid_subs_money = (database.session.query(func.sum(Sub.price))
                         .filter_by(user_id=current_user.name, is_paid=False)
                         .scalar())

    second_fig_base = go.Pie(labels=["Paid subs sum", "Unpaid subs sum"],
                             values=[paid_subs_money, unpaid_subs_money])
    second_fig = dumps(
        go.Figure(data=[second_fig_base])
        .update_layout(paper_bgcolor='rgba(0,0,0,0)',
                       plot_bgcolor='rgba(0,0,0,0)')
        .update_traces(showlegend=False),
        cls=ut.PlotlyJSONEncoder
    )

    subs_by_type = (database.session.query(Sub.type, func.count(Sub.type))
                    .filter_by(user_id=current_user.name).group_by(Sub.type)
                    .all())

    subs_by_type_first = [row[0] for row in subs_by_type]
    subs_by_type_second = [row[1] for row in subs_by_type]

    third_fig_base = go.Bar(x=subs_by_type_first, y=subs_by_type_second)
    third_fig = dumps(
        go.Figure(data=[third_fig_base])
        .update_layout(paper_bgcolor='rgba(0,0,0,0)',
                       plot_bgcolor='rgba(0,0,0,0)')
        .update_traces(showlegend=False),
        cls=ut.PlotlyJSONEncoder
    )

    subs_by_occurance = (database.session
                         .query(Sub.occurance_type,
                                func.count(Sub.occurance_type))
                         .filter_by(user_id=current_user.name)
                         .group_by(Sub.type).all())

    subs_by_occurance_first = [row[0] for row in subs_by_occurance]
    subs_by_occurance_second = [row[1] for row in subs_by_occurance]

    fourth_fig_base = go.Bar(x=subs_by_occurance_first,
                             y=subs_by_occurance_second)
    fourth_fig = dumps(
        go.Figure(data=[fourth_fig_base])
        .update_layout(paper_bgcolor='rgba(0,0,0,0)',
                       plot_bgcolor='rgba(0,0,0,0)')
        .update_traces(showlegend=False),
        cls=ut.PlotlyJSONEncoder)

    return render_template("stat.html",
                           first_fig=first_fig,
                           second_fig=second_fig,
                           third_fig=third_fig,
                           fourth_fig=fourth_fig)
