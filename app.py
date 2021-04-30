import os
from flask import (Flask, render_template, jsonify,
                    request, redirect
                   )
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'nbnjdf'
app.config['MYSQL_DB'] = 'flask_db'

mysql = MySQL(app)

def generageSqlQuery(tablename, formdata):
    sql = "INSERT INTO `" + tablename + "`"
    sql += " VALUES ("
    sqlKeys = ""
    sqlValues = ""
    index = 0
    for item in formdata:
        index = index + 1
        key = item
        value = formdata[key]
        sqlKeys += "`" + key + "`"
        sqlValues += "'" + value + "'"

        if index < len(formdata):
            sqlKeys += ","
            sqlValues += ","
    sql = "INSERT INTO `" + tablename + "` (" + sqlKeys + ") VALUES (" + sqlValues + ")"
    return sql

def generateSearchQuery(tablename, formdata):

    sql = "SELECT * from " + tablename
    if (len(formdata) == 0):
        return sql + ";"
    else: 
        keys = list(formdata.keys())
        for i in range(len(keys)):
            if i == 0:
                sql += " WHERE " + keys[i] 
                sql += " = '" + str(formdata[keys[i]]) + "'"
            else:
                sql += " AND " + keys[i] + " = '" + formdata[keys[i]] + "'"
    sql += ";"
    return sql


def getColumns(tablename):
    cursor = mysql.connection.cursor()
    sql = "SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '" + tablename + "'"
    cursor.execute(sql)

    cols = cursor.fetchall()
    ret = []
    for col in cols:
        dic = {}
        dic["name"] = col[3]
        dic["type"] = col[7]
        dic["max"] = col[8]
        ret.append(dic)

    cursor.close()
    return ret


@app.route("/create-tables")
def createTableIfNotExists():
    sqlStudentTable = "CREATE TABLE IF NOT EXISTS `student` ( `student_id` int(11) NOT NULL AUTO_INCREMENT, `student_first_name` varchar(64) NOT NULL, `student_last_name` varchar(64) NOT NULL, `date_of_birth` date DEFAULT NULL, `primary_poc` varchar(64) DEFAULT NULL, `phone_number` varchar(64) DEFAULT NULL, `email` varchar(64) NOT NULL, `address` varchar(255) NOT NULL, `date_vaccinated` date DEFAULT NULL, PRIMARY KEY(`student_id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4";
    sqlClientTable = "CREATE TABLE IF NOT EXISTS `client` (`client_uid` int(11) NOT NULL AUTO_INCREMENT, `client_address` varchar(255) DEFAULT NULL, `client_type` varchar(255) DEFAULT NULL, `client_name` varchar(255) DEFAULT NULL, PRIMARY KEY(`client_uid`) ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4";
    sqlManufacTable = "CREATE TABLE IF NOT EXISTS `vaccine_manufacturer` (`vaccine_manufacturer_uid` int(11) NOT NULL AUTO_INCREMENT, `vaccine_manufacturer_name` varchar(255) NOT NULL, `vaccine_manufacturer_address` varchar(255) NOT NULL, `vaccine_manufacturer_phone_number` varchar(64) NOT NULL, `vaccine_manufacturer_email` varchar(255) NOT NULL, `vaccine_type` varchar(255) NOT NULL, PRIMARY KEY(`vaccine_manufacturer_uid`) ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4";
    sqlProviderTable = "CREATE TABLE IF NOT EXISTS `provider` ( `vaccine_id` int(11) NOT NULL AUTO_INCREMENT, `vaccine_provider_name` varchar(255) NOT NULL, `vaccine_provider_address` varchar(255) DEFAULT NULL, `vaccine_provider_phone_number` varchar(255) NOT NULL, PRIMARY KEY(`vaccine_id`) ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4";
    sqlActivityTable = "CREATE TABLE IF NOT EXISTS `activity` (`id` int(11) NOT NULL AUTO_INCREMENT, `previous_exposure` tinyint(1) NOT NULL, `last_travel` date DEFAULT NULL, `notes` varchar(255) NOT NULL, `antibody` tinyint(1) NOT NULL, `strain` varchar(255) DEFAULT NULL, PRIMARY KEY(`id`) ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4";
    sqlInsuranceTable = "CREATE TABLE IF NOT EXISTS `insurance` (`health_insurance_id` int(11) NOT NULL AUTO_INCREMENT, `health_insurance_provider` varchar(255) NOT NULL, `health_insurance_group` varchar(255) NOT NULL, `health_insurance_phone_number` varchar(255) NOT NULL, PRIMARY KEY(`health_insurance_id`) ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4";

    cursor = mysql.connection.cursor()

    cursor.execute(sqlStudentTable)
    cursor.execute(sqlClientTable)
    cursor.execute(sqlManufacTable)
    cursor.execute(sqlProviderTable)
    cursor.execute(sqlActivityTable)
    cursor.execute(sqlInsuranceTable)

    mysql.connection.commit()

    cursor.close()

    data = {'success': True}
    return jsonify(data), 200

@app.route('/getFields/', methods=['GET'])
def getFields():
    if request.method == 'GET':
        cols = getColumns(request.args["search-type"])
        return jsonify(cols), 200


@app.route('/')
def homepage():
    return render_template("main.html",form_data=None)

@app.route('/add-data/<tablename>', methods=["post"])
def addActivity(tablename):
    form_data = request.form
    sql = generageSqlQuery(tablename, form_data)

    cursor = mysql.connection.cursor()
    cursor.execute(sql)
    mysql.connection.commit()
    cursor.close()

    data = {'success': True}
    return jsonify(data), 200

@app.route('/search/<tablename>', methods=["GET"])
def search(tablename):
    form_data = request.args.to_dict()
    sql = generateSearchQuery(tablename, form_data)

    cursor = mysql.connection.cursor()
    cursor.execute(sql)
    cursor.close()

    data = {'success': True}
    return jsonify(data), 200

if __name__ == '__main__':
    app.run()
