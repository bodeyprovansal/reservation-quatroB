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
prev_reservation_SQL = "SELECT order_id FROM orders WHERE order_date = %s AND order_time = %s"
get_new_customer_id_SQL = "SELECT customer_id FROM customers ORDER BY customer_id DESC LIMIT 1"
get_new_order_id_SQL = "SELECT order_id FROM orders ORDER BY order_id DESC LIMIT 1"
get_customer_id_SQL = "SELECT customer_id FROM customers WHERE first_name = %s AND last_name = %s AND phone_number = %s AND email_address = %s;"
get_order_id_SQL = "SELECT order_id FROM orders WHERE customer_id = %s ORDER BY"

#DELETE order must be Reservations -> Orders -> Customers

drop_reservation_SQL = "DELETE FROM reservations WHERE reservation_key = %s"


              
print("Content-Type: text/html")    # HTML is following
print()                             # blank line required, end of headers
print("<html><body>")


# connect to database
cnx = mysql.connector.connect(user='root',
                                password='',
                                database='cr',
                                host='127.0.0.1')
      


      
def newReservation():
    
  cust_id = getCustID()
  cat_id = repair_category
  if cust_id == None:
    if not previousReservation():
      print("Sorry, that time is not available. ")
    else:
      createCustomer()
      new_cust_id = getNewCustID()
      
      new_res_key = createKey()
      createOrder(new_cust_id, cat_id)
      new_ord_id = getNewOrderID()
      createNewReservation(new_cust_id, new_ord_id, new_res_key)    
      print("Thank You! Your reservation has been set.")
      print(" Your reservation will be at: " + str(repair_time) + " on: " + str(repair_date))
      print(" If you need to cancel or confirm your reservation, your reservation key is: " + new_res_key)
  else:    
    if previousReservation():
      print("Sorry, that time is not available. ")
    else:
      createOrder(cust_id[0], cat_id)
      ord_id = getNewOrderID()
      res_key = createKey()
      createReservation(cust_id, ord_id, res_key, repair_date, repair_time)
      #print("Nice to see you again. Customer iD: " + str(cust_id[0]) + " New Order #: " + str(ord_id[0]) + " New Reservation Key: " + str(res_key))
   
  
#buffered = True - ignores values/rows retrieved from previous cursors
def getCustID():
  cursor = cnx.cursor(buffered = True)
  cursor.execute(get_customer_id_SQL, (first_name, last_name, phone_number, email_address))
  cust_id = cursor.fetchone()
  cursor.close()
  return cust_id
  
def getOrderID(cust_id):
  cursor = cnx.cursor(buffered = True)
  cursor.execute(get_order_id_SQL, (cust_id[0],))
  ord_id = cursor.fetchone()
  return ord_id
#finds the most recently created customer id  
def getNewCustID():
  cursor = cnx.cursor(buffered = True)
  cursor.execute(get_new_customer_id_SQL)
  cust = cursor.fetchone()
  cust_id = cust[0]
  cursor.close()
  return cust_id
#finds the most recently created order id
def getNewOrderID():
  cursor = cnx.cursor(buffered = True)
  cursor.execute(get_new_order_id_SQL)
  #
  ord_id = cursor.fetchone()
  cursor.close()
  return ord_id

def createCustomer():
  cursor = cnx.cursor(buffered = True)
  cursor.execute(new_customer_SQL, (first_name, last_name, phone_number, email_address))
  cnx.commit()
  cursor.close()
  
def createOrder(cust_id, cat_id):
  cursor = cnx.cursor(buffered = True)
  cursor.execute(new_order_SQL, (cust_id, int(cat_id), description, repair_date, repair_time))
  cnx.commit()
  cursor.close()
#creates a new reservation for existing customers  
def createReservation(cust_id, ord_id, res_key, date, time):
  cursor_prev = cnx.cursor(buffered = True)
  cursor_prev.execute(prev_reservation_SQL, (date, time))
  prev_res = cursor_prev.fetchone()
  print(prev_res)
  cursor_prev.close()
  if prev_res == None:
    print(" No previous reservation. ")
    cursor_res = cnx.cursor(buffered = True)
    cursor_res.execute(new_reservation_SQL, (cust_id[0], ord_id[0], res_key))
    cnx.commit()
    cursor_res.close()
    print(" Nice to see you again. Customer iD: " + str(cust_id[0]) + " New Order #: " + str(ord_id[0]) + " New Reservation Key: " + str(res_key))
  else:
    print(" Previous Reservation Found. Did not set New Reservation. ")   


#creates reservation for new customers only
def createNewReservation(cust_id, ord_id, res_key):
  cursor_res = cnx.cursor(buffered = True)
  cursor_res.execute(new_reservation_SQL, (cust_id, ord_id[0], res_key))
  cnx.commit()
  cursor_res.close()
  
#checks to see if the time requested has already been reserved
def previousReservation():
  cursor_prev = cnx.cursor(buffered = True)
  cursor_prev.execute(prev_reservation_SQL, (repair_date, repair_time))
  prev_res = cursor_prev.fetchall()
  print(prev_res)
  cursor_prev.close()
  if prev_res != []:
    print(prev_res)
    #print("prev_ res != None, returning False")
    return False
  else:
    #print("prev_res = None, returning True")
    return True

#creates a random aaa-1111 reservation key
def createKey():
  lower_case = "".join(choice(string.ascii_lowercase) for x in range(3))
  dig = "".join(choice(string.digits) for x in range(4))
  key = lower_case + "-" + dig
  return key

#removes reservation when correct reservation key is provided
def deleteReservation(res_key_input):
  print("Reservation Cancelled. ")
  
  cursor_res = cnx.cursor()
  cursor_res.execute(drop_reservation_SQL, (res_key_input,))
  cursor_res.close()
  cnx.commit()
  
#Flags if the "Make Reservation" button was pressed  
if "make_reservation" in form:
  new_reservation=True
  newReservation()  
#Flags if the "Cancel Reservation" button was pressed  
if "cancel_reservation" in form:
  cancel_reservation=True
  res_key_input = form["reservation_key"].value
  deleteReservation(res_key_input)


print("</body></html>") 

cnx.close()  # close the connection
