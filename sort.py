import sys
import os
import re
import csv
import pandas as pd
from ftplib import FTP
import socket



#Premier FTP Support email: datateam@premierwd.com

#GLOBAL_VARIABLES
PROSTREET_IN = "prostreet.csv"
PREMIERWD_IN = "Rigid_data.csv" 
PROSTREET_OUT = "UPLOAD.csv" 

#GLOBAL VARIABLES FOR LOGIN
FTP_ADDRESS = "ftp://website"
LOGIN_USER = "USER"
LOGIN_USER_PASS = "PASSWORD"

#PROSTREET_IN = Export from prostreet
#PREMIERWD = Data export from Premierwd
#PROSTREET_OUT = Final output with updated pricing, ready for upload to Prostreet

def grab_file_from_ftp():

        #define FTP and login credentials
        ftp = FTP(FTP_ADDRESS)
        ftp.login(user= LOGIN_USER, passwd=LOGIN_USER_PASS)

        #Info and status of transfer to console
        print(ftp.retrlines('LIST'))
        
        #filename = 'Bilstein.zip'
        localfile = open(PREMIERWD_IN, 'wb')
        ftp.retrbinary('RETR ' + PREMIERWD_IN, localfile.write, 1024)
        ftp.quit()
        localfile.close()




def proccess_line(export_line, FILEOUT, header_export):
        #Proccess each line of the file exported from the website

        #Variable declaration for Prostreet Export
        #test (PLS DELETE LINE)
        export_sku_index = header_export.index('Variant SKU')
        export_price_index = header_export.index('Variant Price')
        export_policy_index = header_export.index('Variant Inventory Policy')
        export_qty_index = header_export.index('Variant Inventory Qty')
        export_weight_index = header_export.index('Variant Grams')
        export_policy = export_line[export_policy_index]
        export_sku = export_line[export_sku_index]
        export_price = export_line[export_price_index]
        export_qty = export_line[export_qty_index]
        export_weight = export_line[export_weight_index]

        
        #open the supplier file (Wont loop every line elsewise)
        read_in_one = open(PREMIERWD_IN, 'r', encoding="utf8")
        supplier_file = csv.reader(read_in_one)
        header_supplier = next(supplier_file, None)

        #define the sku and the price of the suppliers info
        supplier_price_index = header_supplier.index('MAP')
        supplier_sku_index = header_supplier.index('Mfg Part Number')
        supplier_stocking_index = header_supplier.index('Inventory Status')


        #Create a copy of the current row of export
        row = []
        row = export_line

        #Check each line in PROSTREET_IN and compare with every line in the PREMIERWD file 
        # - Updates price
        # - Sets Policy to deny so items with 0 QTY show as "Sold out" / "Special order"
        # - Sets all Products not stocked by premier to QTY 0 
        print("Before for loop ")
        for supplier_line in supplier_file:
                
                #print(supplier_line)
                if (export_sku == supplier_line[supplier_sku_index]):
                        
                        print("setting price ")
                        #Set Price
                        row[export_price_index] = float(supplier_line[supplier_price_index].strip('$'))
                        print("setting policy ")
                        #Set Policy
                        row[export_policy_index] = 'deny'
                        print("setting stock ")
                        #Set Stocking Check
                        if(supplier_line[supplier_stocking_index] == 'Non Stocking'):
                                row[export_qty_index] = 0
                        print("writing ")
                        #Write row to file
                        FILEOUT.writerow(row)

                else:
                        pass
                
        
        read_in_one.close()
        

def main():

        #Grab ftp
        grab_file_from_ftp()
        
        
        # Open file: website export, supplier export and create writable file
        f_out = open(PROSTREET_IN, 'r', encoding="utf8")
        new_file = open(PROSTREET_OUT, 'w', newline='', encoding="utf8")
        reader2 = csv.reader(f_out)
        writer = csv.writer(new_file)

        #Read Header and store it
        header_supplier = next(reader2, None)

        #Prepare final file
        writer.writerow(header_supplier)
        
        # loop through both files at the same time, stops once shorter list completes
        for line in reader2:
                proccess_line(line, writer, header_supplier)

        print("FINISHED", end='')

        #Close the files 
        f_out.close()
        new_file.close()
        

if __name__ == "__main__":
    main()