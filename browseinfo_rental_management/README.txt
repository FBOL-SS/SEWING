Date: 21-9-2018

Improvement Point in version 12.0.0.1:

1) If Invoice is created from Rental Order then in invoice - Rental start date and rental end date displayed otherwise hide rental start date and end date.

Improvement Point in version 12.0.0.2:

added tax and calculated total amount in rental order and invoice.

Improvement Point in version 12.0.0.3:

Index improved.

Improvement Point in version 12.0.0.4:

Update report.
Index improved.


Improvement Point in version 12.0.0.5:

--> Update Cron Method
--> Update Report Layout & report data
--> Solve record does not exits error.

Date : 5-4-2019

--> Solve error while replace product(Create incoming shipment)


Date : 11-4-2019 

--> Added new warning for same product with same serial no is getting replace .
--> Fixed issue user replace null  values .

Date 11-12-2019
version : 12.0.0.9
1.)added boolean field in res setting
2.) invoice not generate while cron run
3.) 1st invoice only generate with saleable product
4.) when added saleable product and rental product in rental order , after confirming rental order its generate two picking , one of rental products picking and another for saleable products picking


Date 11-12-2019
version : 12.0.1.0
issues solve:-
remove singletone errors
unused object added comment it

version : 12.0.1.1
replace product serial in picking functionality improved

version : 12.0.1.2
change src location in picking of saleable product

12.0.1.3

1) Add hourly and weekly selection for bill frequency.
2) Add constraint for start date and end date.
3) Add constraint for hourly initial and bill frequency terms.
4) add invoice counter for hourly invoice configuration.
5) Update invoice cron to hourly bases. and Update
renew date conditions based on bill frequency.
6) Solve issue of singleton error while order confirm.
7) Update security.

Version 12.0.1.4 : (29/04/20)
		- Change string 'Monthly rent' to 'Rent' in rental line.
		- Remove required true from py for start & end date.
		- Add condition not to create picking of service product (in saleable products) 

Version 12.0.1.5 : (30/07/20)
		- Solve issue of create picking of saleable products with non admin user.

Version 12.0.1.6: (08/12/20)
	- Fixed traceback generated on replacing a product from wizard. 	

Version 12.0.1.7: (16/12/20)
	- Fixed issue of total amount not getting changed in sale order after changing saleable products. 		
