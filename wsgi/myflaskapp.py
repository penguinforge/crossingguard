from flask import Flask 
from flask import render_template
from flask import request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/CVE/", methods=['GET', 'POST']) 
def CVE_Report():
    if request.method == 'POST':
        return render_template('cve_report.html', cve=request.form['CVE'])

    return '''
            <form action="" method="post">
               <p>CVE:<input type=text name=CVE> <input type=submit value="Get Report">
            </form>
           '''

if __name__ == "__main__":
    app.run()
