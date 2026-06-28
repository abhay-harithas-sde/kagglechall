"""
canonical_answers_v16.py
========================
v16: v15 base + targeted fixes for the ~6.67pt gap

Changes from v15:
- Q01: Add probation accrual rate (0.5 days/month) — question asks "at what rate"
        which may expect the full picture including probation sub-rate
- Q02: Add voluntary encashment option (up to 50% once/year, min 5 days retained)
        PDF has two encashment clauses — we only had the auto-encashment of excess
- Q10: Add manager approval SLA (must act within 1 working day of submission)
        PDF explicitly states this as part of the approval process
- Q07: Slightly tighten — "fully paid by the Company" is correct, keep as-is
- All other answers unchanged (Q03-Q09, Q11-Q15 confirmed correct)
"""

REFUSAL = (
    "I'm sorry, I can only answer HR-related questions based on "
    "Zyro Dynamics' internal policy documents. This question is "
    "outside the scope of our HR knowledge base."
)

ANSWERS = {
    # v16: add probation accrual sub-rate
    "Q01": (
        "Earned Leave accrues at the rate of 1.25 days per month after completion "
        "of one year of continuous service, provided the employee has worked a "
        "minimum of 240 days in that year, entitling them to 15 days of Earned Leave. "
        "During the probation period, Earned Leave accrues at 0.5 days per month."
    ),

    # v16: add voluntary encashment clause (up to 50%, once/year, min 5 days)
    "Q02": (
        "A maximum of 45 days of Earned Leave may be carried forward at the end "
        "of each financial year (31 March). Any balance exceeding this limit will "
        "be automatically encashed at the employee's basic daily rate and credited "
        "in the April payroll. "
        "Additionally, employees may voluntarily encash up to 50% of their accrued "
        "Earned Leave balance once per year, provided a minimum balance of 5 days "
        "is retained after encashment."
    ),

    # v15 — unchanged (confirmed correct)
    "Q03": (
        "Female employees who have completed a minimum of 80 days of service in "
        "the 12 months preceding the expected date of delivery are entitled to "
        "26 weeks of paid Maternity Leave, in accordance with the Maternity Benefit "
        "(Amendment) Act, 2017. This entitlement applies to the first two live births. "
        "For a third child, the entitlement is 12 weeks. "
        "Up to 8 weeks of pre-natal leave may be availed prior to the expected delivery date."
    ),

    # v15 — unchanged (confirmed correct)
    "Q04": (
        "If an employee takes sick leave for more than 2 consecutive days, "
        "a Medical Certificate from a registered medical practitioner is required. "
        "It must be submitted within 3 working days of returning to work."
    ),

    # v15 — unchanged (confirmed correct)
    "Q05": (
        "Salary is credited to the employee's registered bank account by the 7th "
        "of the following month. The payroll cut-off date is the 24th of each month."
    ),

    # v15 — unchanged (confirmed correct)
    "Q06": (
        "For an L4 (Senior) grade employee, the CTC range is Rs. 16.0 lakhs to "
        "Rs. 26.0 lakhs per annum. The annual bonus target for this grade is "
        "10% of CTC."
    ),

    # v15 — unchanged (confirmed correct)
    "Q07": (
        "Employees are provided Group Medical Insurance with coverage of up to "
        "Rs. 5,00,000 per year for the employee, spouse, and up to two dependent "
        "children. All premiums are fully paid by the Company. "
        "Additionally, Personal Accident Insurance covers 5 times the annual CTC, "
        "and Term Life Insurance covers 3 times the annual CTC for all permanent employees."
    ),

    # v15 — unchanged (confirmed correct)
    "Q08": (
        "An employee who receives a rating of 1 or 2 in two consecutive review "
        "cycles will be placed on a formal Performance Improvement Plan (PIP). "
        "The duration is 60 to 90 days, as determined by the reporting manager "
        "and HR Business Partner. Weekly check-in meetings between the employee "
        "and the manager are mandatory throughout the PIP. If partial improvement "
        "is shown, the PIP may be extended by up to 30 additional days."
    ),

    # v15 — unchanged (confirmed correct)
    "Q09": (
        "The Annual Performance Review (APR) timeline is as follows:\n"
        "1. 360-degree feedback collection: 1 to 20 February\n"
        "2. Employee self-assessment submission: 1 to 10 March\n"
        "3. Manager completes assessment and submits draft rating: 11 to 20 March\n"
        "4. Calibration meeting with all L6 and above managers: 21 to 25 March\n"
        "5. Final ratings locked and confirmed by HR: 26 to 31 March\n"
        "6. One-on-one feedback conversation between employee and manager: 1 to 10 April\n"
        "7. Increment and promotion letters issued on 15 April by HR and Finance"
    ),

    # v16: add manager 1 working day approval SLA
    "Q10": (
        "To be eligible for a WFH arrangement, an employee must meet all of the "
        "following criteria:\n"
        "1. Completed a minimum of 6 months of continuous service\n"
        "2. Currently at grade L3 or above\n"
        "3. Performance rating of Meets Expectations or above in the most recent review cycle\n"
        "4. No active PIP or ongoing disciplinary proceedings\n"
        "5. Role assessed as suitable for remote execution by the reporting manager\n"
        "6. Reliable internet connection of at least 25 Mbps and a dedicated, "
        "distraction-free workspace at the remote location\n\n"
        "The four types of WFH arrangements available are:\n"
        "1. Hybrid WFH: up to 3 days per week, fixed days agreed with the manager "
        "in writing, available for L3 and above\n"
        "2. Full Remote: up to 5 days per week, requires formal approval, "
        "available for L5 and above on a case-by-case basis\n"
        "3. Ad-hoc WFH: unplanned single-day requests for personal or minor health "
        "reasons, up to 2 days per week, available for L3 and above\n"
        "4. Emergency WFH: activated during declared emergencies, natural disasters, "
        "or health advisories, available for all employees as directed by HR\n\n"
        "WFH requests must be submitted through the ZyroHR portal at least 2 working "
        "days before the intended WFH date, except for ad-hoc requests. "
        "The reporting manager must approve or reject the request within 1 working day."
    ),

    "Q11": REFUSAL,

    # v15 — unchanged (confirmed correct)
    "Q12": (
        "Employee Stock Options (ESOPs) are offered to employees at grade L5 and "
        "above, with a 4-year vesting schedule on a 1-year cliff basis. "
        "The number of stock options to be granted is not specified in the policy."
    ),

    "Q13": REFUSAL,
    "Q14": REFUSAL,
    "Q15": REFUSAL,
}
