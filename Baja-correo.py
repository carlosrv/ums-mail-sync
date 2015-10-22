#!/usr/bin/python

import MySQLdb
import pymssql
import smtplib

# User and password for mail

def sendmail(solapin_baja):
    user = "ums@cnic.edu.cu"
    user_pwd = "123456"
    TO = 'carlos.vergel@cnic.edu.cu'
    SUBJECT = "Usuarios Bajas de UMS"
    TEXT = 'El usuario %s fue dado de baja por Economia y de los Servicios de Red' %solapin_baja
    server = smtplib.SMTP('correo.cnic.edu.cu')
    server.ehlo()
    server.starttls()
    server.login(user, user_pwd)
    BODY = '\r\n'.join(['To: %s' % TO,
       'From: %s' % user,
       'Subject: %s' % SUBJECT,
       '', TEXT])
    server.sendmail(user, [TO], BODY)
    print ('email sent')

# Connect to Mysql - UMS Accounts
ums_accounts_conn = MySQLdb.connect(host="10.37.1.31",  # your host, usually localhost
                                    user="ums",  # your username
                                    passwd="umscn1c",  # your password
                                    db="ums")  # name of the data base


#  Assets de RECURSOS HUMANOS
econ_accounts_conn = pymssql.connect(host='10.36.34.247',
                                     user='user_assetsp',
                                     password='super2015*',
                                     database='RH_Assets')


# UMS cursors
cur_ums_accounts = ums_accounts_conn.cursor()
cur_ums_accounts.execute("SELECT * FROM accounts_account")


# for row_eko in cur_eko_accounts:
#     print row_eko[1]

def is_baja(solapin_ums):
    cur_eko_accounts = econ_accounts_conn.cursor()
    cur_eko_accounts.execute("SELECT * FROM Empleados_Gral WHERE Id_Empleado = %d", solapin_ums)
    for row_eko in cur_eko_accounts:
        solapin_eko = row_eko[1]
        if row_eko[21] == 1:
            return 1
    return 0

    cur_eko_accounts.close()


usuarios_a_dar_baja = []

for row_ums in cur_ums_accounts:
    if row_ums[10] and row_ums[1] == 1:
        solapin_ums = row_ums[10]
        # print 'solapin ums: ', solapin_ums
        if is_baja(solapin_ums) == 1:
            usuarios_a_dar_baja.append(solapin_ums.strip())

# Cerrar la conexion con la db
cur_ums_accounts.close()



# recorrr la lista de los usuarios a dar baja en UMS y enviar correo
# Dar baja de UMS ponerlo inactivo
def ums_baja(solapin_baja):
    cur_ums_accounts = ums_accounts_conn.cursor()
    cur_ums_accounts.execute("UPDATE accounts_account SET active=0 WHERE entity_ID ='%s'" % (solapin_baja))
    cur_ums_accounts.close()
    sendmail(solapin_baja)
    return 1


for suspend_service in usuarios_a_dar_baja:
    solapin_baja = suspend_service
    if ums_baja(solapin_baja) == 1:
        print suspend_service


print usuarios_a_dar_baja
