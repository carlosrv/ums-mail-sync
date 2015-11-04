#!/usr/bin/python

import MySQLdb
import pymssql
import smtplib
import time

from config import *


def testmail():
    user = email_user
    user_pwd = email_pass
    TO = email_to
    SUBJECT = "Ejecucion del Script de actulizacion de planillas"
    TEXT = "El script de actualizacion de planillas fue ejecutado el %s " % (time.strftime("%c"))
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
    print TEXT
#
# Connect to Mysql - Planillas Accounts
planillas_accounts_conn = MySQLdb.connect(host=ums_host,  # your host, usually localhost
                                          user=planillas_user,  # your username
                                          passwd=planillas_pass,  # your password
                                          db=planillas_db)  # name of the data base
#  Assets de RECURSOS HUMANOS
econ_accounts_conn = pymssql.connect(host=eco_host,
                                     user=eco_user,
                                     password=eco_pass,
                                     database=eco_db)

cur_planillas_accounts = planillas_accounts_conn.cursor()
cur_planillas_accounts.execute("TRUNCATE TABLE template_generator_app_employee")

user_planillas = []

cur_planillas_accounts.close()

cur_planillas_accounts = planillas_accounts_conn.cursor()
#
# variable = '2119867'
#
# print direcciones[variable[1:3]]

cur_eko_accounts = econ_accounts_conn.cursor()
cur_eko_accounts.execute("SELECT * FROM Vista_Yamile WHERE Baja = 0")

for row_eko in cur_eko_accounts:
    solapin = str(row_eko[0])
    name = str(row_eko[1].encode('utf-8'))
    lastname1 = str(row_eko[2].encode('utf-8'))
    lastname2 = str(row_eko[3].encode('utf-8'))
    personal_id = str(row_eko[4])
    area_id = row_eko[5]
    user_info = [solapin.strip(), name.strip(), lastname1.strip(), lastname2.strip(), personal_id.strip(),
                 direcciones[area_id[1:3]].strip()]

    user_planillas.append(user_info)
cur_planillas_accounts.close()
cur_eko_accounts.close()

# print user_planillas
planillas_accounts_conn = MySQLdb.connect(host=ums_host,  # your host, usually localhost
                                          user=planillas_user,  # your username
                                          passwd=planillas_pass,  # your password
                                          db=planillas_db)  # name of the data base
cur_planillas_accounts = planillas_accounts_conn.cursor()

count = 1
for planillas_data in user_planillas:
    id_planillas = count
    user_id = planillas_data[0]
    name_planilla = planillas_data[1].decode('utf-8')
    last1_planilla = planillas_data[2].decode('utf-8')
    last2_planilla = planillas_data[3].decode('utf-8')
    id_personal = planillas_data[4]
    area_name = planillas_data[5].decode('utf-8')
    dirrec_name = planillas_data[5]
    cur_planillas_accounts.execute("INSERT INTO planillas.template_generator_app_employee (solapin,name,lastname,ci,area,departament)  VALUES (%s,%s,%s,%s,%s,%s)",(user_id, name_planilla, last1_planilla + " " +last2_planilla, id_personal, area_name, area_name))

    count = count + 1
    print  user_id, name_planilla, last1_planilla, id_personal, dirrec_name
planillas_accounts_conn.commit()
cur_planillas_accounts.close()
print count
testmail()