FROM tiangolo/uwsgi-nginx-flask:python3.6
RUN pip3 install --upgrade Click dnspython Flask Flask-MySQLdb itsdangerous Jinja2 MarkupSafe mysql-connector-python mysqlclient six Werkzeug
ADD /azure-trooper /app
