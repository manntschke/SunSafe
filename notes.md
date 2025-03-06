# SunSafe Sentinel Project Goals

## **Primary Goal: Fraud Detection**

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

