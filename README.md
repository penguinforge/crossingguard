Crossing Guard
=============

IAVM mapping tool to Red Hat products. 
=======

This is the code used to host http://crossingguard-penguinforge.rhcloud.com/ .

The code is designed to run on an OpenShift enviornment using the python 2.6 cartridge. 

You should be able to run the code localy by cloning it and running the following (Note this uses [python virtualenv](https://pypi.python.org/pypi/virtualenv)):

```
virtualenv cguard_py
cguard_py/bin/python crossingguard/setup.py install

export OPENSHIFT_APP_DNS=localhost
cguard_py/bin/python crossingguard/wsgi/myflaskapp.py
```

You can also deploy it to your own OpenShift online enviornment with the following: 
```
rhc app create APP_NAME python-2.6 --from-code https://github.com/penguinforge/crossingguard.git
```
OR
```
rhc app create APP_NAME pyton-2.6
cd APP_NAME
git remote add upstream https://github.com/penguinforge/crossingguard.git
git fetch upstream
git checkout master; git merge --strategy=recursive -X theirs upstream/master
git push
```

 Copyright (C) 2013  Eric Rich

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
