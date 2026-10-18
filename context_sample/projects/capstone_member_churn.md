# Capstone Project: Member Churn Early-Warning

Status as of 2026-09-28: modeling phase

## One-line summary

Predict which credit union members are likely to close their primary checking account within the next 90 days, so the Member Experience team can reach out before they leave.

## Key facts

- Course: Applied AI Systems certificate, capstone track.
- Advisor: Dr. Priya Raman (faculty advisor; weekly check-ins on Wednesdays at 12:15 by video).
- Business sponsor: Teresa Alvarez, my manager at Lakeshore Community Credit Union. She reviews whether the output is useful to branch staff.
- Code review partner: Sam Chen, my studio classmate. We review each other's pull requests every Sunday.
- Final presentation and report deadline: 2026-12-11.
- Midpoint review: 2026-10-30.

## Data

All data is synthetic. I generate it with a Python script (generate_members.py) that simulates 50,000 members with realistic distributions for tenure, product holdings, direct-deposit status, digital-banking logins, branch visits, and fee events. I decided not to use real member data, even de-identified, because of privacy policy and because I want the repository to be public. Churn rate in the synthetic data is about 6.5 percent, so the classes are imbalanced.

## Approach

1. Baseline: logistic regression with class weights.
2. Main model: XGBoost with a time-based train/validation/test split (train on months 1 to 18, validate on 19 to 21, test on 22 to 24).
3. Explanations: SHAP values for the top features so that branch staff understand why a member was flagged.
4. Output: a weekly ranked list of the top 200 at-risk members per region, written to a PostgreSQL table.

## Current results

- Logistic regression baseline: ROC AUC 0.66.
- XGBoost first pass: ROC AUC 0.71, precision at top 200 of 0.18.
- Most important features so far: loss of direct deposit in the last 60 days, decline in digital logins, and number of fee events.

## Open problems

- Calibration is poor; predicted probabilities are too high for low-tenure members.
- I have not chosen the alert threshold. Teresa wants a list short enough that each branch can call every flagged member within a week.
- I still need a simple dashboard for the final presentation.

## Next steps

- Try isotonic calibration on the validation set.
- Write the data generation assumptions section of the report.
- Ask Dr. Raman whether a survival-analysis framing is worth the extra complexity before the midpoint review.
