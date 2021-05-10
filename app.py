import os
from flask import (Flask, render_template, jsonify,
                    request, redirect, url_for
                   )
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'nbnjdf'
app.config['MYSQL_DB'] = 'flask_db'

mysql = MySQL(app)
columnDict = dict()
tablesCreated = False

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


def getKey(item):
    #return column ID for sorting
    return item[4]

def getColumns(tablename):
    cursor = mysql.connection.cursor()
    sql = "SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '" + tablename + "'"
    cursor.execute(sql)

    cols = cursor.fetchall()
    cols = sorted(cols, key=getKey)
    print("sorted cols: ")
    print(cols)
    ret = []

    for col in cols:
        dic = {}
        dic["name"] = col[3]
        dic["type"] = col[7]
        dic["max"] = col[8]
        if dic["name"] != "sid" and dic["name"] != "cell":
            ret.append(dic)

    cursor.close()
    return ret

def getAll(fieldname):
    cursor = mysql.connection.cursor()
    sql = "SELECT * FROM " + fieldname
    cursor.execute(sql)

    clients = cursor.fetchall()
    cursor.close()

    return clients


@app.route("/create-tables")
def createTableIfNotExists():
    global tablesCreated
    if not tablesCreated:
        sqlClientTable = "CREATE TABLE IF NOT EXISTS `client` (`client_id` int(11) NOT NULL AUTO_INCREMENT, `client_address` varchar(255) DEFAULT NULL, `client_type` varchar(255) DEFAULT NULL, `client_name` varchar(255) DEFAULT NULL, PRIMARY KEY(`client_id`) ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4";
        sqlInsuranceTable = "CREATE TABLE IF NOT EXISTS `insurance` (`health_insurance_id` int(11) NOT NULL AUTO_INCREMENT, `health_insurance_provider` varchar(255) NOT NULL, `health_insurance_group` varchar(255) NOT NULL, `health_insurance_phone_number` varchar(255) NOT NULL, PRIMARY KEY(`health_insurance_id`) ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4";
        sqlStudentTable = "CREATE TABLE IF NOT EXISTS `student` ( `student_id` int(11) NOT NULL AUTO_INCREMENT, `client_id` int, FOREIGN KEY (`client_id`) REFERENCES client(`client_id`), `student_first_name` varchar(64) NOT NULL, `student_last_name` varchar(64) NOT NULL, `date_of_birth` date DEFAULT NULL, `primary_poc` varchar(64) DEFAULT NULL, `health_insurance_id` int, FOREIGN KEY (`health_insurance_id`) REFERENCES insurance(`health_insurance_id`), `phone_number` varchar(64) DEFAULT NULL, `email` varchar(64) NOT NULL, `address` varchar(255) NOT NULL, PRIMARY KEY(`student_id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4";
        sqlManufacTable = "CREATE TABLE IF NOT EXISTS `vaccine_manufacturer` (`vaccine_manufacturer_id` int(11) NOT NULL AUTO_INCREMENT, `vaccine_manufacturer_name` varchar(255) NOT NULL, `vaccine_manufacturer_address` varchar(255) NOT NULL, `vaccine_manufacturer_phone_number` varchar(64) NOT NULL, `vaccine_manufacturer_email` varchar(255) NOT NULL, `vaccine_type` varchar(255) NOT NULL, PRIMARY KEY(`vaccine_manufacturer_id`) ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4";
        sqlProviderTable = "CREATE TABLE IF NOT EXISTS `provider` ( `vaccine_provider_id` int(11) NOT NULL AUTO_INCREMENT, `vaccine_provider_name` varchar(255) NOT NULL, `vaccine_provider_address` varchar(255) DEFAULT NULL, `vaccine_provider_phone_number` varchar(255) NOT NULL, PRIMARY KEY(`vaccine_provider_id`) ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4";
        sqlActivityTable = "CREATE TABLE IF NOT EXISTS `activity` (`id` int(11) NOT NULL AUTO_INCREMENT, `previous_exposure` tinyint(1) NOT NULL, `last_travel` date DEFAULT NULL, `notes` varchar(255) NOT NULL, `antibody` tinyint(1) NOT NULL, `strain` varchar(255) DEFAULT NULL, PRIMARY KEY(`id`) ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4";
        sqlVaccinationTable = "CREATE TABLE IF NOT EXISTS `vaccination` (`vaccination_id` int(11) NOT NULL AUTO_INCREMENT, PRIMARY KEY (`vaccination_id`),`vaccine_manufacturer_id` int, FOREIGN KEY (`vaccine_manufacturer_id`) REFERENCES vaccine_manufacturer(`vaccine_manufacturer_id`), `student_id` int, FOREIGN KEY (`student_id`) REFERENCES student(`student_id`), `vaccine_provider_id` int, FOREIGN KEY (`vaccine_provider_id`) REFERENCES provider(`vaccine_provider_id`) ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4";


        cursor = mysql.connection.cursor()
        cursor.execute(sqlClientTable)
        cursor.execute(sqlInsuranceTable)
        cursor.execute(sqlStudentTable)
        cursor.execute(sqlManufacTable)
        cursor.execute(sqlProviderTable)
        cursor.execute(sqlActivityTable)
        cursor.execute(sqlVaccinationTable)

        mysql.connection.commit()

        cursor.close()

        data = {'success': True}
        tablesCreated = True
        return jsonify(data), 200
    else:
        data = {'success': True}
        return jsonify(data), 200

@app.route('/getFields/', methods=['GET'])
def getFields():
    if request.method == 'GET':
        # If not already in dict, fetch and add to dict
        if (request.args["search-type"] not in columnDict.keys()):
            cols = getColumns(request.args["search-type"])
            columnDict[request.args["search-type"]] = cols
        else:
            cols = columnDict[request.args["search-type"]]
        return jsonify(cols), 200


@app.route('/')
def homepage():
    return render_template("main.html", page="home")

@app.route('/addStudent')
def addStudent():
    clients = getAll('client')
    insurances = getAll('insurance')
    return render_template("main.html", insurances=insurances, clients = clients, page="student_form")

@app.route('/addClient')
def addClient():
    return render_template("main.html",  page="client_form")

@app.route('/addVacManufacturer')
def addVacManufacturer():
    return render_template("main.html", page="vaccine_manufacturer_form")

@app.route('/addProvider')
def addProvider():
    return render_template("main.html",  page="provider_form")

@app.route('/addActivity')
def addActivity():
    return render_template("main.html", page="activity_form")

@app.route('/addInsurance')
def addInsurance():
    return render_template("main.html",  page="insurance_form")

@app.route('/addVaccination')
def addVaccination():
    students = getAll('student')
    vaccine_manufacturers = getAll('vaccine_manufacturer')
    providers = getAll('provider')
    print(providers)
    return render_template("main.html", students = students, vaccine_manufacturers=vaccine_manufacturers, providers=providers, page="vaccination_form")

@app.route('/showSearch')
def showSearch():
    return render_template("main.html",  page="search")



@app.route('/add-data/<tablename>', methods=["post"])
def addData(tablename):
    form_data = request.form
    sql = generageSqlQuery(tablename, form_data)
    print(sql)
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
    data = cursor.fetchall()

    cursor.close()
    cols = []
    if len(data) > 0:
        cols = getColumns(tablename)
        
    return jsonify({"data": data, "cols": cols}), 200
    

if __name__ == '__main__':
    tablesCreated = False
    app.run()
