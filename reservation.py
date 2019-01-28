import cgitb , cgi
import mysql.connector
import string
from random import *
cgitb.enable()
#"keep_blank_values = 1" parameter allows empty fields
form = cgi.FieldStorage(keep_blank_values=1)

#retrieve input values
repair_time = form["repair_time"].value
repair_date = form["repair_date"].value
repair_category = form["repair_category"].value
description = form["description"].value
first_name = form["first_name"].value
last_name = form["last_name"].value
phone_number = form["phone_number"].value
email_address = form["email_address"].value
new_reservation = False
cancel_reservation = False


new_customer_SQL = "INSERT INTO customers (first_name, last_name, phone_number, email_address) VALUES (%s, %s, %s, %s)"
new_order_SQL = "INSERT INTO orders (customer_id, category_id, detailed_description, order_date, order_time) VALUES (%s, %s, %s, %s, %s)"
new_reservation_SQL = "INSERT INTO reservations (customer_id, order_id, reservation_key) VALUES (%s, %s, %s)"
get_customer_id_SQL = "SELECT customer_id FROM customers ORDER BY customer_id DESC LIMIT 1"
get_order_id_SQL = "SELECT order_id FROM orders ORDER BY order_id DESC LIMIT 1"

              
print("Content-Type: text/html")    # HTML is following
print()                             # blank line required, end of headers
print("<html><body>")


# connect to database
cnx = mysql.connector.connect(user='root',
                                password='otterRHCP6486',
                                database='cr',
                                host='127.0.0.1')
      


def newReservation():
  createCustomer()
  new_cust_id = getCustID()
  new_cat_id = repair_category
  new_res_key = createKey()
  createOrder(new_cust_id, new_cat_id)
  new_ord_id = getOrderID()
  
  cursor = cnx.cursor()
  cursor.execute(new_reservation_SQL, (new_cust_id, new_ord_id, new_res_key))
  cnx.commit()
  print("Thank You! Your reservation has been set.")
  print("Your reservation will be at: " + str(repair_time) + "on: " + str(repair_date))
  print("If you need to cancel or confirm your reservation, your reservation key is: " + new_res_key)  
  
def getCustID():
  cursor = cnx.cursor()
  cursor.execute(get_customer_id_SQL)
  cust = cursor.fetchone()
  cust_id = cust[0]
  return cust_id

def getOrderID():
  cursor = cnx.cursor()
  cursor.execute(get_order_id_SQL)
  ord = cursor.fetchone()
  ord_id = ord[0]
  return ord_id

def createCustomer():
  cursor = cnx.cursor()
  cursor.execute(new_customer_SQL, (first_name, last_name, phone_number, email_address))
  cnx.commit()
  
def createOrder(cust_id, cat_id):
  cursor = cnx.cursor()
  cursor.execute(new_order_SQL, (cust_id, int(cat_id), description, repair_date, repair_time))
  cnx.commit()
  
def createKey():
  lower_case = "".join(choice(string.ascii_lowercase) for x in range(3))
  dig = "".join(choice(string.digits) for x in range(4))
  key = lower_case + "-" + dig
  return key
  
if "make_reservation" in form:
  new_reservation=True
  #testing
  #print("New Reservation: " + str(new_reservation) + " ")  
  newReservation()
  
  
if "cancel_reservation" in form:
  cancel_reservation=True
  reservation_key = form["reservation_key"].value
  #testing
  #print("Cancel Reservation: " + str(cancel_reservation) + " ")

#def checkForConflict():
  #before creating new reservation, check if time is already taken


#def cancelReservation():  
  #remove reservation from database



print("</body></html>") 

cnx.close()  # close the connection 