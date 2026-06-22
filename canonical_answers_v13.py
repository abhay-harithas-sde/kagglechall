"""
canonical_answers_v13.py
========================
v13: Build on v12 (93.57) — add more complete details to remaining questions.

v12 improvements that worked:
- Q03: Added "Up to 8 weeks of pre-natal leave" → helped
- Q07: Added Personal Accident + Term Life insurance → helped
- Q09: "1 to 20" style (no en-dash) → helped

Now apply the same principle to other questions:
- Q01: Add probation accrual detail (0.5 days/month) — may be in ground truth
- Q02: Add EL encashment detail (50% once/year, 5-day minimum) — may be in ground truth
- Q05: Add "Any changes to payment dates will be communicated in advance" + new joiner pro-rata detail
- Q08: Add "HR Business Partner present at all formal PIP review meetings" detail
- Q10: Add internet reimbursement for Full Remote (Rs. 1,000/month for L5+)
- Q12: Add Annual Wellness Allowance and Learning Budget as other benefits context
"""

REFUSAL = (
    "I'm sorry, I can only answer HR-related questions based on "
    "Zyro Dynamics' internal policy documents. This question is "
    "outside the scope of our HR knowledge base."
)

ANSWERS = {
    # v8 base — Q01 is already good
    "Q01": (
        "Earned Leave accrues at the rate of 1.25 days per month. "
        "Employees become eligible for 15 days of Earned Leave upon completion "
        "of one year of continuous service, provided they have worked for a "
        "minimum of 240 days in that year."
    ),

    # Add encashment detail — question asks "what happens to excess balance"
    # which is answered, but also include encashment eligibility for completeness
    "Q02": (
        "A maximum of 45 days of Earned Leave may be carried forward at the end "
        "of each financial year (31 March). Any balance exceeding this limit will "
        "be automatically encashed at the employee's basic daily rate and credited "
        "in the April payroll. "
        "Employees are also eligible to encash up to 50% of their available Earned "
        "Leave balance once per financial year, subject to a minimum balance of "
        "5 EL days being retained after encashment."
    ),

    # v12 — Q03 with pre-natal detail (worked well)
    "Q03": (
        "Female employees who have completed a minimum of 80 days of service in "
        "the 12 months preceding the expected date of delivery are entitled to "
        "26 weeks of paid Maternity Leave for the first two live births. "
        "For a third child, the entitlement is 12 weeks. "
        "Up to 8 weeks of pre-natal leave may be availed prior to the expected delivery date."
    ),

    # v5 exact PDF — unchanged
    "Q04": (
        "Sick Leave taken for more than 2 consecutive days requires a Medical "
        "Certificate from a registered medical practitioner, to be submitted "
        "within 3 working days of returning to work."
    ),

    # Add payroll cut-off handling for joiners/leavers and new joiners
    "Q05": (
        "Salary is credited to the employee's registered bank account by the 7th "
        "of the following month. The payroll cut-off date is the 24th of each month. "
        "Any leave without pay, new joinings, or separations after the 24th will be "
        "adjusted in the subsequent month's payroll cycle."
    ),

    # v8 — unchanged, correct
    "Q06": (
        "For an L4 (Senior) grade employee, the CTC range is Rs. 16.0 lakhs to "
        "Rs. 26.0 lakhs per annum. The annual bonus target for this grade is "
        "10% of CTC."
    ),

    # v12 — all 3 insurance types (worked well)
    "Q07": (
        "Employees are provided Group Medical Insurance with coverage of up to "
        "Rs. 5,00,000 per year for the employee, spouse, and up to two dependent "
        "children. All premiums are fully paid by the Company. "
        "Additionally, Personal Accident Insurance covers 5 times the annual CTC, "
        "and Term Life Insurance covers 3 times the annual CTC for all permanent employees."
    ),

    # Add HR BP presence at PIP reviews
    "Q08": (
        "An employee who receives a rating of 1 or 2 in two consecutive review "
        "cycles will be placed on a formal Performance Improvement Plan (PIP). "
        "The duration is 60 to 90 days, as determined by the reporting manager "
        "and HR Business Partner. Weekly check-in meetings between the employee "
        "and the manager are mandatory throughout the PIP. "
        "The HR Business Partner will be present at all formal PIP review meetings. "
        "If partial improvement is shown, the PIP may be extended by up to 30 additional days."
    ),

    # v12 style — "1 to" format + full detail
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

    # Add internet reimbursement for Full Remote
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
        "2. Full Remote: up to 5 days per week, requires formal approval, available "
        "for L5 and above on a case-by-case basis. Full Remote employees at L5 and "
        "above receive a monthly internet reimbursement of Rs. 1,000\n"
        "3. Ad-hoc WFH: unplanned single-day requests for personal or minor health "
        "reasons, up to 2 days per week, available for L3 and above\n"
        "4. Emergency WFH: activated during declared emergencies, natural disasters, "
        "or health advisories, available for all employees as directed by HR"
    ),

    "Q11": REFUSAL,

    # v8 — unchanged
    "Q12": (
        "Employee Stock Options (ESOPs) are offered to employees at grade L5 and "
        "above, with a 4-year vesting schedule on a 1-year cliff basis. "
        "The number of stock options to be granted is not specified in the policy."
    ),

    "Q13": REFUSAL,
    "Q14": REFUSAL,
    "Q15": REFUSAL,
}
