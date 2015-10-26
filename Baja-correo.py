#!/usr/bin/python

import MySQLdb
import pymssql
import smtplib

# User and password for mail

def sendmail(solapin_baja):
    user = email_user
    user_pwd = email_pass
    TO = email_to
    SUBJECT = email_subject
    TEXT = email_body %solapin_baja
    server = smtplib.SMTP(email_host)
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
ums_accounts_conn = MySQLdb.connect(host=ums_host,  # your host, usually localhost
                                    user=ums_user,  # your username
                                    passwd=ums_pass,  # your password
                                    db=ums_db)  # name of the data base


#  Assets de RECURSOS HUMANOS
econ_accounts_conn = pymssql.connect(host=eco_host,
                                     user=eco_user,
                                     password=eco_pass,
                                     database=eco_db)

# UMS cursors
cur_ums_accounts = ums_accounts_conn.cursor()
cur_ums_accounts.execute("SELECT * FROM accounts_account")


# for row_eko in cur_eko_accounts:
#     print row_eko[1]

def is_baja(solapin_ums):
    cur_eko_accounts = econ_accounts_conn.cursor()
    cur_eko_accounts.execute("SELECT * FROM Empleados_Gral WHERE Id_Empleado = %d", solapin_ums)
    for row_eko in cur_eko_accounts:
        if row_eko[21] == 1:
            return 1
    return 0

    cur_eko_accounts.close()


usuarios_a_dar_baja = []
user_name = []

for row_ums in cur_ums_accounts:
    if row_ums[10] and row_ums[1] == 1:
        solapin_ums = row_ums[10]
        name_ums = row_ums[5]
        # print 'solapin ums: ', solapin_ums
        if is_baja(solapin_ums) == 1:
            usuarios_a_dar_baja.append(solapin_ums.strip())
            user_name.append(name_ums)

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
