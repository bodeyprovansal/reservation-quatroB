#!/usr/bin/env python3

import cgitb, cgi
import mysql.connector

import string
from random import *

cgitb.enable()
# Enabling keep_blank_values to allow empty fields
form = cgi.FieldStorage(keep_blank_values=1)
fields = {
  'repair_time': form['repair_time'].value,
  'repair_date': form['repair_date'].value,
  'repair_category_id': form['repair_category_id'].value,
  'repair_description': form['repair_description'].value,
  'first_name': form['first_name'].value,
  'last_name': form['last_name'].value,
  'phone_number': form['phone_number'].value,
  'email_address': form['email_address'].value,
  'reservation_key': form['reservation_key'].value,
  'new_reservation': 'make_reservation' in form,
  'cancel_reservation': 'cancel_reservation' in form
}

# Database connection
cnx = mysql.connector.connect(user='root', password='', database='cr', host='127.0.0.1')

def dbInteraction(query, parameters, needsCommit=False):
  cursor = cnx.cursor(buffered = True)
  cursor.execute(query, parameters)
  if needsCommit:
    cnx.commit()
  else:
    return cursor.fetchone()

def getLastInsertId():
  return dbInteraction('SELECT LAST_INSERT_ID()', {})[0]

def createCustomer(first_name, last_name, phone_number, email_address):
  query = 'INSERT INTO customers (first_name, last_name, phone_number, email_address) VALUES (%s, %s, %s, %s)'
  dbInteraction(query, (first_name, last_name, phone_number, email_address), True)
  return getLastInsertId()

def fetchCustomerId(first_name, last_name, phone_number, email_address):
  query = 'SELECT customer_id FROM customers WHERE first_name = %s AND last_name = %s AND phone_number = %s AND email_address = %s'
  row = dbInteraction(query, (first_name, last_name, phone_number, email_address))
  if row:
    return row[0]

def createOrder(customer_id, category_id, detailed_description, order_date, order_time):
  query = 'INSERT INTO orders (customer_id, category_id, detailed_description, order_date, order_time) VALUES (%s, %s, %s, %s, %s)'
  dbInteraction(query, (customer_id, category_id, detailed_description, order_date, order_time), True)
  return getLastInsertId()

def createReservation(customer_id, order_id, reservation_key):
  query = 'INSERT INTO reservations (customer_id, order_id, reservation_key) VALUES (%s, %s, %s)'
  dbInteraction(query, (customer_id, order_id, reservation_key), True)
  return getLastInsertId()

def removeReservation(reservation_key):
  query = 'DELETE FROM reservations WHERE reservation_key = %s'
  dbInteraction(query, (reservation_key,), True)

def fetchExistingReservation(order_date, order_time):
  query = 'SELECT order_id FROM orders WHERE order_date = %s AND order_time = %s'
  return dbInteraction(query, (order_date, order_time))

def generateReservationKey():
  lower_case = ''.join(choice(string.ascii_lowercase) for x in range(3))
  dig = ''.join(choice(string.digits) for x in range(4))
  key = lower_case + '-' + dig
  return key

# Route Handlers
def handleNewReservation():
  if fetchExistingReservation(fields['repair_date'], fields['repair_time']):
    return print('Sorry, that time is not available.')

  customerId = fetchCustomerId(fields['first_name'], fields['last_name'], fields['phone_number'], fields['email_address'])
  if not customerId:
    customerId = createCustomer(fields['first_name'], fields['last_name'], fields['phone_number'], fields['email_address'])

  orderId = createOrder(customerId, fields['repair_category_id'], fields['repair_description'], fields['repair_date'], fields['repair_time'])
  reservationKey = generateReservationKey()
  createReservation(customerId, orderId, reservationKey)
  print('Thank You! Your reservation has been set.<br/>')
  print(' Your Customer ID is ' + str(customerId) + ' and your Order ID is ' + str(orderId) + '<br/>')
  print(' Your reservation will be at: ' + str(fields['repair_time']) + ' on: ' + str(fields['repair_date']) + '<br/>')
  print(' If you need to cancel or confirm your reservation, your reservation key is: ' + reservationKey)

def handleRemovingReservation():
  print('Reservation Cancelled.')
  removeReservation(fields['reservation_key'])

# HTTP Route
print('Content-Type: text/html')
print()
print('<html><body>')

if fields['new_reservation']:
  handleNewReservation()
elif fields['cancel_reservation']:
  handleRemovingReservation()

print('</body></html>')
cnx.close()
