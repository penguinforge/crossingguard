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


@app.route("/IAVM/", methods=['POST']) 
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
        referances = []
        severity = "Not Found."
        title = ""
        date = ""
 
        iavms = xmlsoup.findAll('iavm')
        for i in iavms:
            if iava == re.findall(r'\"(.+?)\"', "{0}".format(i.s).split()[7])[0]:
                # If you want to see how an IAVA as xml is structured.
                # print i
                severity = i.s['severity']
                title = i.s['title']
                date = i.s['releasedate']
                links = i.s.findAll('reference')
                for link in links:
                    referances.append({link['refname']: link['url']})

                iavm_cves = i.s.findAll('cvenumber')
                for cve in iavm_cves:
                    base_uri = 'https://access.redhat.com/security/cve/'
                    try:  # Check to see if Red Hat has this as a record. 
                        uri = base_uri + cve.contents[0]
                        html = urllib2.urlopen(uri)

                        if html.geturl() == uri:
                            cves.append({cve.contents[0]: True})
                        else:
                            cves.append({cve.contents[0]: False})
                    except urllib2.HTTPError, e:
                        print e.code
                    except urllib2.URLError, e:
                        print e.code
        return render_template('iavm_report.html', iava=iava, severity=severity, 
                cves=cves, iavm_title=title, release_date=date, 
                iavm_referances=referances)


@app.route("/IAVM/list") 
@app.route("/IAVM/LIST") 
def IAVM_List():
     base_uri = 'http://iase.disa.mil/stigs/downloads/xml/iavm-to-cve(u).xml'
     xml = urllib2.urlopen(base_uri)
     xmlsoup = BeautifulSoup(xml.read())
     xmlsoup.originalEncoding

     iavms = xmlsoup.findAll('iavm')
     iavm_list = []
     for iava in iavms:
         iavm = iava.s['iavm']
         severity = iava.s['severity']
         title = iava.s['title']
         iavm_list.append((iavm, severity, title))

     print iavm_list[0][0]

     return render_template('iavm_list.html', iavms=iavm_list)


if __name__ == "__main__":
    app.run()
