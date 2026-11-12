

\# PES1UG24AM240 – Software Engineering Lab 7



\## Fuzz Testing for Input Validation Bugs



\### Objective

To identify and fix input validation bugs using property-based fuzz testing with Python Hypothesis.



\### Technologies Used

\- Python 3.12.6

\- Hypothesis 6.170.15

\- Pytest 8.3.4



\### Functions Tested

1\. `sanitize\_license\_plate()`

2\. `parse\_trip\_mileage()`

3\. `format\_rental\_invoice()`



\### Files

\- `processor.py` – Fixed application implementation.

\- `test\_processor.py` – Hypothesis-based fuzz testing.

\- `PES1UG24AM240\_LAB-7\_REPORT(SCREENSHOTS INCLD.).pdf` – Complete lab report with screenshots.



\### Installation



```bash

python -m pip install hypothesis pytest

```



\### Execution



Run the application:



```bash

python processor.py

```



Run the tests:



```bash

python -m pytest test\_processor.py

```



\### Results

Initial fuzz testing identified input-validation failures in all three functions.



After implementing defensive validation, all three Hypothesis tests passed.



\*\*Final Result: 3 passed.\*\*



