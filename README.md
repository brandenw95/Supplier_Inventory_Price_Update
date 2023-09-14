# Prostreet Motorsports Supplier Inventory Update Script
## Description

This script automates the process of grabbing product data from a supplier and then updates the pricing and other attributes of products in Prostreet. Specifically, the script pulls the product data file from an FTP server and then processes each line of this file, updating the pricing and other attributes as needed based on the supplier data.

## Features

- **FTP File Fetching**: Automatically retrieves the supplier data file (`all_s.csv`) from a specified FTP server.
- **Pricing Update**: Updates the product pricing in Prostreet based on the MAP pricing from the supplier.
- **Stock Management**: Updates product availability based on inventory status from the supplier.
- **Inventory Policy Management**: Sets policy for items with 0 QTY to show as "Sold Out" or "Special Order".

## Prerequisites

- Python environment (preferably Python 3.x).
- Required Python packages:
  - `pandas`
  - `csv`

## Setup

1. Make sure you've installed the required Python packages.

   ```
   pip install pandas
   ```

2. Set up the global variables in the script:

   - `PROSTREET_IN`, `PREMIERWD_IN`, and `PROSTREET_OUT` for input and output CSV filenames.
   - FTP credentials: `FTP_ADDRESS`, `LOGIN_USER`, and `LOGIN_USER_PASS`.

## Usage

1. Run the script:

   ```
   python sort.py
   ```

2. If the FTP fetching is enabled (`grab_file_from_ftp()` in `main()`), the script will first download the `all_s.csv` file from the FTP server.

3. The script will process each line of the Prostreet exported data (`products.csv`), updating pricing and other attributes based on the supplier data.

4. A new file (`UPLOAD.csv`) will be created, containing the updated product data ready for upload to Prostreet.

## Notes

1. FTP login credentials have been hardcoded for demonstration purposes. In a production environment, consider using environment variables or secure vaults to store sensitive information.
2. The script currently processes the files based on predefined headers in the CSV files. Ensure the structure of the input CSV files matches the expected headers.

## Contributing

Please report any issues or contribute to improvements by creating pull requests.

## License

Please ensure appropriate licensing for your project, especially if you are distributing or using it in a commercial environment.
