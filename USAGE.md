# Tej App Usage Guide

The **Tej** app for ERPNext allows you to manage Tunisian "Retenue à la Source" (RS) Certificates and generate the required XML declarations for the Tej platform.

## 1. Prerequisites

Ensure your Suppliers are correctly set up in ERPNext. The workflow primarily revolves to recording RS Certificates against Suppliers.

## 2. Managing RS Certificates

An **RS Certificate** represents a withholding tax certificate issued to a supplier. You can create these manually or they may be generated from payments/invoices (depending on your specific automation setup).

### Creating a New Certificate manually

1.  Go to **Tej > Tej RS Certificate**.
2.  Click **New Tej RS Certificate**.
3.  **Supplier**: Select the supplier.
4.  **Posting Date**: Set the date of the certificate (defaults to today).
5.  **RS Information**:
    *   **RS Code**: Select the appropriate code (1-9) corresponding to the nature of the service/item (e.g., Honoraires, Loyers, etc.).
    *   **RS Rate (%)**: Enter the withholding rate.
6.  **Amounts**:
    *   **Gross Amount**: Enter the base amount (Montant Brut).
    *   **RS Amount**: Automatically calculated based on Gross Amount * Rate.
    *   **Net Amount**: Automatically calculated.
7.  **Save** and **Submit** the document.

> **Note**: Only *Submitted* certificates are pulled into Declarations.

## 3. Generating a Monthly Declaration

The **Tej RS Declaration** aggregates all RS Certificates for a specific month and generates the XML file required by tax authorities.

### Creating a Declaration

1.  Go to **Tej > Tej RS Declaration**.
2.  Click **New Tej RS Declaration**.
3.  **Company**: Select your company.
4.  **Period**:
    *   Select the **Month** (e.g., 01 for January).
    *   Enter the **Year** (e.g., 2026).
5.  **Declaration Type**: Choose "Monthly" (default) or "Occasional".
6.  Click **Save**.

### Fetching Data & Generating File

1.  After saving, click the **Get Certificates** button.
    *   The system will search for all *submitted* `Tej RS Certificate` documents for that specific month and year that haven't been declared yet.
    *   They will populate the "Certificates" table.
2.  Verify the total amounts and the list of certificates.
3.  Click the **Generate XML** button.
    *   The system will check for errors and generate the XML file.
    *   The status will change to "Generated".
4.  The XML file will be attached to the document in the "XML File" field.
5.  **Download** the XML file and upload it to the Tej platform.

## 4. Updates & Cancellations

*   If you need to change a certificate that is part of a Draft declaration, remove it from the declaration table first or delete the declaration.
*   If a declaration is already submitted/generated, you may need to file an amended declaration (check local regulations for specific procedures on amending XMLs).
