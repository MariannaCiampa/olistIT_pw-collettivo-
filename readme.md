md = mark down

# TITOLO

## esempio
* pippo
**pippo**
~~**pippo**~~
_**pippo**_


## **customers**
* pk_customer VARCHAR
* region VARCHAR
* city VARCHAR
* cap VARCHAR (si potrebbe eliminare)


## **categories**
* pk_category SERIAL
* name VARCHAR (in inglese)


## **products**
* pk_product VARCHAR 
* fk_category INTEGER
* name_length INTEGER (errore ortografico)
* description length INTEGER 
* imgs_qty INTEGER


## **orders**
* pk_order VARCHAR
* fk_customer VARCHAR 
* status VARCHAR
* purchase_timestamp TIMESTAMP
* delivered_timestamp TIMESTAMP
* estimated_date DATE


(per il momento non abbiamo questa tabella)
## **sellers**
* pk_seller VARCHAR 
* region VARCHAR 


## **orders_products**
* pk_order_product SERIAL
* fk_order VARCHAR
* fk_product VARCHAR
* fk_seller VARCHAR
* price FLOAT
* freight FLOAT (=costo di trasporto)

(abbiamo escluso order_item)