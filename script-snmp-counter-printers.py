#!/usr/bin/env python3

# -------------------------------------------------------------------------
# script-snmp-counter-printers.py - Script para elitura dos contadores das
#                                    impressoras via protocolo SNMP
# HW: Intel
# OS: Linux
# Compiler: Python 3.10.8
# PKG: pysnmp 4.4.12
# Criado em: 31/10/2022
# Revisao: 00
# Copyright (c) 2022 by Alan Lopes
# -------------------------------------------------------------------------
# Codigo-fonte adaptado de Simple SNMP Queries with Python (Brian Yaklin)
#  https://www.yaklin.ca/2021/08/25/snmp-queries-with-python.html

import sys
from pysnmp.entity.rfc3413.oneliner import cmdgen
import csv
from datetime import datetime

# identificação dos Objetos (OID)
isoLocation = "iso.3.6.1.2.1.1.6.0"
isoTotalPageCount = "iso.3.6.1.2.1.43.10.2.1.4.1.1"
isoShortName = "iso.3.6.1.2.1.1.1.0"
isoSerialNumber = "iso.3.6.1.2.1.43.5.1.1.17.1"

# tupla dos OID para consulta
oids = (isoSerialNumber, isoShortName, isoLocation, isoTotalPageCount)

# criar arquivos com os dados
#filenamedst = "dst/" + datetime.now().strftime("%Y%m%d%H%M") + "_contadores_impressoras.txt"
filenamedst = "dst/contadores_impressoras.txt"
out = csv.writer(open(filenamedst,"w",encoding="UTF8"), delimiter=',',quoting=csv.QUOTE_ALL)
out.writerow(["DataHora, SerialNumber, Modelo, Localizacao , TotalPageCount"])

# ler arquivos de impressora
filelistprinters = "src/list_printers.txt"

with open(filelistprinters, "r") as filecsv:
	readerfile = csv.DictReader(filecsv)

	for row  in readerfile:
        # leitura dos dados da impressora
		host = row["host"]
		snmp_ro_comm = row["snmp_ro_comm"]

		# Define a PySNMP CommunityData object named auth, by providing the SNMP community string
		auth = cmdgen.CommunityData(snmp_ro_comm)

		# Define the CommandGenerator, which will be used to send SNMP queries
		cmdGen = cmdgen.CommandGenerator()

		# Query a network device using the getCmd() function, providing the auth object, a UDP transport
		# our OID for SYSNAME, and don't lookup the OID in PySNMP's MIB's
		errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
			auth,
			cmdgen.UdpTransportTarget((host, 161)),
			*[cmdgen.MibVariable(oid) for oid in oids],
			lookupMib=False,
		)

		# Check if there was an error querying the device
		if errorIndication:
			sys.exit()

        # carga dos dados no arquivo de destino
		data = [datetime.now()]
		data += ["%s" % val.prettyPrint() for oid, val in varBinds]
		out.writerow(data)