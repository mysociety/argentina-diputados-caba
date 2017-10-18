# coding=utf-8

import scraperwiki
import lxml.etree
import sqlite3

BASE_URL = 'https://parlamentaria.legislatura.gov.ar/webservices/Json.asmx/GetDiputadosActivosNuevo?id_bloque='

xml = scraperwiki.scrape(BASE_URL)

root = lxml.etree.fromstring(xml)

print root

parsedMembers = []

for member in root:

    memberData = {}

    memberData['id'] = member.find('{http://tempuri.org/}id_legislador').text

    memberData['first_name'] = member.find('{http://tempuri.org/}nombre').text

    memberData['last_name'] = member.find('{http://tempuri.org/}apellido').text

    memberData['name'] = u'{} {}'.format(memberData['first_name'], memberData['last_name'])

    memberData['party'] = member.find('{http://tempuri.org/}bloque').text

    memberData['image'] = member.find('{http://tempuri.org/}foto').text

    gender = member.find('{http://tempuri.org/}id_sexo').text

    if gender == '1':
        memberData['gender'] = 'male'
    elif gender == '2':
        memberData['gender'] = 'female'

    print memberData

    parsedMembers.append(memberData)

print 'Counted {} Members'.format(len(parsedMembers))

try:
    scraperwiki.sqlite.execute('DELETE FROM data')
except sqlite3.OperationalError:
    pass
scraperwiki.sqlite.save(
    unique_keys=['id'],
    data=parsedMembers)
