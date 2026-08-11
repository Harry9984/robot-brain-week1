1. Root Cause:
The original script used basic string concatenation (`+ "," +`). This broke the CSV structure because the item name "Shirt, Red (Large)" contained a comma itself, which caused the CSV parser to split that row into three columns instead of two.

2. Fix:
I replaced the manual string building with Python's built-in `csv` module (`csv.writer`). This module automatically wraps any text containing commas in double quotes, preserving the integrity of the columns.

3. Verification:
I ran a standard CSV reader script to verify the output. Every single row now strictly returns a length of 2 columns, confirming the fix is successful.
