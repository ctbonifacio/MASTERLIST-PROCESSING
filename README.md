# MASTERLIST-PROCESSING
TO PROCESS MASTERLIST

## Header Formatting Automation

A new script is available to normalize a masterlist file so the output header row is:

- `ACC NUMBER`
- `DEBTOR NAME`

Supported input types:

- CSV (`.csv`)
- Excel workbook (`.xlsx`, `.xlsm`)

### Usage

```bash
python format_masterlist_headers.py input.csv output.csv
python format_masterlist_headers.py input.xlsx formatted_masterlist.xlsx
```

If `output` is omitted, the script writes:

- `formatted_masterlist.csv` for CSV input
- `formatted_masterlist.xlsx` for Excel input

## Web App Bank Formatting

The app now runs with Streamlit and formats a bank upload file from the web UI.

### Run the app

```bash
streamlit run app.py
```

### How it works

- Select the bank and upload the workbook.
- Download a formatted Excel file named:
  - `(bank)_(date processed)_(last month and year).xlsx`

For `HSBC UAE`, the output maps:

- `ACC NUMBER` ← column B
- `DEBTOR NAME` ← column D
- `STATUS CODE` = `PAYMENT FILE`
- `CLAIM PAID AMOUNT` ← column F
- `CLAIM PAID DATE` ← column E converted to `yyyy-mm-dd`
- `DATE IMPORT` = current import date

For `ENBD`, `EIB`, and `DIB`, the app currently creates the header-only workbook until extraction rules are added.

### DIB Masterlist Processor

A new tab is available in the Streamlit app to merge DIB masterlist details from a workbook containing the following sheets:

- `ALLOC`
- `CUSTOMER_INFO`
- `LAST PAYMENT`
- `CORP DETAILS`
- `AUTO`

The integration logic is:

1. `ALLOC` is the main source.
   - Extract `CIF` from `ALLOC` column A.
   - Extract `SHADOW_ACNO` from `ALLOC` column F.
2. Lookup `CUSTOMER_INFO` by `CIF` and extract:
   - `NAME`, `NATIONALITY`, `SHADOW_ACNO`, `CS_PRODUCT`, `PROD_TYPE`, `LGL_CRM`, `GROSS_OS`, `DPD`, `EMAIL`
3. Lookup `LAST PAYMENT` by `SHADOW_ACNO` and extract:
   - `CP_AMT_PAY`, `CP_PAY_DATE`
4. Lookup `CORP DETAILS` by `CIF` and extract:
   - `V_PASSPORT_NO`, `D_DOB`, `V_PERMANENT_NATIONAL_ID`, `V_EMAIL_ID`, `V_EMIRATE`, `V_MOBILE_NO`, `V_EMPLOYER_NAME`
5. Lookup `AUTO` by `CIF` and extract:
   - `N_YEAR_MODEL`, `V_MODEL_NAME`, `V_COLOR`, `V_REGISTRATION_NAME`, `V_REGISTRATION_NO`, `V_ENGINE_NO`, `V_CHASSIS_NO`, `V_VENDOR_NAME`

The generated output contains the combined DIB record fields for each CIF and is available for download as an Excel workbook.

