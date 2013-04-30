from flask import Flask, render_template, request, url_for

app = Flask(__name__, static_url_path='/static/')

# Additional Logging for OpenShift
app.config['PROPAGATE_EXCEPTIONS'] = True

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/CVE/", methods=['GET', 'POST']) 
def CVE_Report():
    if request.method == 'POST':
        return render_template('cve_report.html', cve=request.form['CVE'])

    return '''
            <form action="" method="post">
               <p>CVE: <input type=text name=CVE> <input type=submit value="Get Report">
            </form>
           '''


@app.route("/IAVM/", methods=['GET', 'POST']) 
@app.route("/IAVM/<iavm>") 
def IAVM_Report(iavm=None):
    if request.method == 'POST' or iavm:
        if iavm:
            return render_template('iavm_report.html', iava=iavm)
        else:
            return render_template('iavm_report.html', iava=request.form['IAVM'])
    return '''
            <form action="" method="post">
               <p>IAVM: <input type=text name=IAVM> <input type=submit value="Get Report">
            </form>
           '''


if __name__ == "__main__":
    app.run()
