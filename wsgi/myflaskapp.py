import urllib2
from BeautifulSoup import BeautifulSoup
import re
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
            iava = iavm 
        else:
            iava = request.form['IAVM']

        base_uri = 'http://iase.disa.mil/stigs/downloads/xml/iavm-to-cve(u).xml'
        xml = urllib2.urlopen(base_uri)
        xmlsoup = BeautifulSoup(xml.read())
        xmlsoup.originalEncoding

        cves = []
        iavms = xmlsoup.findAll('iavm')
        for i in iavms:
            if iava == re.findall(r'\"(.+?)\"', "{0}".format(i.s).split()[7])[0]:
                #print iavm
                #iava = i.s['iavm']
                # If you want to see how an IAVA as xml is structured. print i
                severity = i.s['severity']
                iavm_cves = i.s.findAll('cvenumber')
                for cve in iavm_cves:
                    cves.append(cve.contents[0])
                #if rhel_check and simple:
                #    for cve in cves:
                #    base_uri = 'https://access.redhat.com/security/cve/'
                #    try:
                #        uri = base_uri + cve
                #        html = urllib2.urlopen(uri)
                #        if html.geturl() == uri:

        return render_template('iavm_report.html', iava=iava, severity=severity, cves=cves)
    else:
        return '''
            <form action="" method="post">
               <p>IAVM: <input type=text name=IAVM> <input type=submit value="Get Report">
            </form>
           '''


if __name__ == "__main__":
    app.run()
