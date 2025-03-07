
# SunSafe Sentinel Project Goals

## **Primary Goal: Fraud Detection**

## ***Client data***

| Column Name   | Column Description                          |
|--------------|-------------------------------------------|
| client_id    | Unique id for client                     |
| district     | District where the client is            |
| client_catg  | Category client belongs to              |
| region       | Area where the client is                |
| creation_date | Date client joined                     |
| target       | Fraud: 1, Not fraud: 0                  |

## Invoice data

| Column Name            | Column Description |
|------------------------|-------------------|
| client_id             | Unique id for the client |
| invoice_date         | Date of the invoice |
| tarif_type           | Type of tax |
| counter_number       |  |
| counter_statue       | Takes up to 5 values such as working fine, not working, on hold status, etc. |
| counter_code         |  |
| reading_remarque     | Notes that the STEG agent takes during his visit to the client (e.g: If the counter shows something wrong, the agent gives a bad score) |
| counter_coefficient  | An additional coefficient to be added when standard consumption is exceeded |
| consommation_level_1 | Consumption Level 1 |
| consommation_level_2 | Consumption Level 2 |
| consommation_level_3 | Consumption Level 3 |
| consommation_level_4 | Consumption Level 4 |
| old_index            | Old index |
| new_index            | New index |
| months_number        | Month number |
| counter_type         | Type of counter |



### Objective:
Develop a system that identifies fraudulent electricity and gas consumption patterns using advanced data analysis and machine learning techniques.

### Key Tasks:
- Collect and preprocess historical consumption data, smart meter readings, and billing records.
- Implement an initial **XGBoost-based anomaly detection model**.
- Detect irregular consumption patterns indicative of meter tampering, incorrect billing, or energy theft.
- Evaluate the model with real-world data to ensure high recall and precision.

---
## **Stretch Goal: Output Refinement & Human Verification Bins**
### Objective:
Improve fraud detection accuracy by refining flagged cases and categorizing them into risk-based verification bins.

### Key Tasks:
- Introduce a **second-stage Decision tree** to reduce false positives.
- Develop a **binning system** that categorizes flagged cases into risk levels (e.g., *Low, Medium, High*) for human review.
- Provide a **customization option** for companies to choose which level of flagged cases they want to verify manually.
- Build a **dashboard** for intuitive visualization and management of flagged cases.
## Set up your Environment



### **`macOS`** type the following commands : 

- For installing the virtual environment you can either use the [Makefile](Makefile) and run `make setup` or install it manually with the following commands:

     ```BASH
    make setup
    ```
    After that active your environment by following commands:
    ```BASH
    source .venv/bin/activate
    ```
Or ....
- Install the virtual environment and the required packages by following commands:

    ```BASH
    pyenv local 3.11.3
    python -m venv .venv
    source .venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    ```
    
### **`WindowsOS`** type the following commands :

- Install the virtual environment and the required packages by following commands.

   For `PowerShell` CLI :

    ```PowerShell
    pyenv local 3.11.3
    python -m venv .venv
    .venv\Scripts\Activate.ps1
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    ```

    For `Git-bash` CLI :
  
    ```BASH
    pyenv local 3.11.3
    python -m venv .venv
    source .venv/Scripts/activate
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    ```

    **`Note:`**
    If you encounter an error when trying to run `pip install --upgrade pip`, try using the following command:
    ```Bash
    python.exe -m pip install --upgrade pip
    ```


   
## Usage

In order to train the model and store test data in the data folder and the model in models run:

**`Note`**: Make sure your environment is activated.

```bash
python example_files/train.py  
```

In order to test that predict works on a test set you created run:

```bash
python example_files/predict.py models/linear_regression_model.sav data/X_test.csv data/y_test.csv
```

## Limitations

Development libraries are part of the production environment, normally these would be separate as the production code should be as slim as possible.


