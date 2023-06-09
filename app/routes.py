from app import app
from flask import render_template, redirect, url_for, request
from report_of_monaco_2018_racing_bydujiy import main as rr


drive_data, start_data, end_data = rr.read_logs('app/static/data_files')
drivers_list = rr.get_drivers(drive_data)
race_report = rr.get_report(drive_data, start_data, end_data)


@app.route("/")
def default_route():
    return redirect(url_for("print_report"))


@app.route('/report/', methods=["GET"])
def print_report():
    order = request.args.get('order')
    report = rr.sort_result(race_report, order)
    return render_template('report/report.html', report=report)


@app.route('/report/drivers/', methods=["GET", "POST"])
def print_drivers():
    order = request.args.get('order')
    drivers = rr.sort_result(drivers_list, order)
    return render_template('report/drivers.html', drivers=drivers)


@app.route('/print_driver')
def print_driver():
    driver_id = request.args.get('driver_id')
    return redirect(url_for('driver', driver_id=driver_id))


@app.route('/report/driver/<string:driver_id>')
def driver(driver_id):
    driver_report = rr.search_by_abbr(race_report, driver_id)
    return render_template('report/driver.html', driver_report=driver_report)
