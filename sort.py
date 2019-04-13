import sys
import os
import re
import csv
#import pandas as pd

def proccess_line(export_line, FILEOUT, header_export):
        #Proccess each line of the file exported from the website

        # Variable declaration
        export_sku_index = header_export.index('Variant SKU')
        export_price_index = header_export.index('Variant Price')
        export_sku = export_line[export_sku_index]
        export_price = export_line[export_price_index] 
        
        #open the supplier file (Wont loop every line elsewise)
        read_in_one = open("supplier.csv", 'r')
        supplier_file = csv.reader(read_in_one)
        header_supplier = next(supplier_file, None)

        #define the sku and the price of the suppliers info
        supplier_price_index = header_supplier.index('Variant Price')
        supplier_sku_index = header_supplier.index('Variant SKU')
        

        #Test code // Delete after
        #print("Export line w/o prices = ", export_sku, export_price)
        #print("Supplier type = ", type(supplier_sku_index))
        #print("Export type = ", type(export_sku))
        #print("Supplier sku = ", supplier_sku_index, "Supplier price = ", supplier_price)
        #print(export_sku)

        #Create a copy of the current row of export
        row = []
        row = export_line
        

        for supplier_line in supplier_file:
                
                if (export_sku == supplier_line[supplier_sku_index]):

                        row[export_price_index] = supplier_line[supplier_price_index]
                        FILEOUT.writerow(row)
                else:
                        pass
        
        read_in_one.close()
        
def main():

        # Open file: website export, supplier export and create writable file
        f_out = open("export.csv", 'r')
        new_file = open("final.csv", 'w', newline='')
        reader2 = csv.reader(f_out)
        writer = csv.writer(new_file)

        #Read Header and store it
        header_supplier = next(reader2, None)

        #Prepare final file
        writer.writerow(header_supplier)
        
        # loop through both files at the same time, stops once shorter list completes
        for line in reader2:
                proccess_line(line, writer, header_supplier)

        f_out.close()
        new_file.close()
        

                

if __name__ == "__main__":
    main()