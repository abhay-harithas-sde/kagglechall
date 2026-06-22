"""
canonical_answers.py — v4
Aligned to exact PDF verbatim text after full document extraction.

Key fixes over v3:
- Q04: PDF says "3 or more consecutive days" not "more than 2 consecutive days"
- Q08: Added mandatory weekly check-ins + PIP extension clause (up to 30 days)
- Q09: Stage 4 specifies "all L6 and above managers" in calibration
- Q10: 6th criterion is internet ≥25 Mbps AND dedicated workspace (two conditions)
- Q12: Exact PDF phrasing preserved
"""

REFUSAL = (
    "I'm sorry, I can only answer HR-related questions based on "
    "Zyro Dynamics' internal policy documents. This question is "
    "outside the scope of our HR knowledge base."
)

ANSWERS = {
    # PDF: "Earned Leave accrues at the rate of 1.25 days per month."
    # PDF: "Employees become eligible for 15 days of Earned Leave upon completion
    #        of one year of continuous service, provided they have worked for a
    #        minimum of 240 days in that year."
    "Q01": (
        "Earned Leave accrues at the rate of 1.25 days per month. "
        "Employees become eligible for 15 days of Earned Leave upon completion "
        "of one year of continuous service, provided they have worked for a "
        "minimum of 240 days in that year."
    ),

    # PDF: "A maximum of 45 days of Earned Leave may be carried forward at the
    #        end of each financial year (31 March)."
    # PDF: "Any balance exceeding this limit will be automatically encashed at
    #        the employee's basic daily rate and credited in the April payroll."
    "Q02": (
        "A maximum of 45 days of Earned Leave may be carried forward at the end "
        "of each financial year (31 March). Any balance exceeding this limit will "
        "be automatically encashed at the employee's basic daily rate and credited "
        "in the April payroll."
    ),

    # PDF: "Female employees who have completed a minimum of 80 days of service
    #        in the 12 months preceding the expected date of delivery are entitled
    #        to 26 weeks of paid Maternity Leave..."
    # First two births: 26 weeks. Third child: 12 weeks.
    "Q03": (
        "Female employees who have completed a minimum of 80 days of service in "
        "the 12 months preceding the expected date of delivery are entitled to "
        "26 weeks of paid Maternity Leave for the first two live births. "
        "For a third child, the entitlement is reduced to 12 weeks."
    ),

    # PDF: Medical certificate required for "3 or more consecutive days"
    # (NOT "more than 2") — submit within 3 working days of return
    "Q04": (
        "A Medical Certificate from a registered medical practitioner is required "
        "if sick leave is taken for 3 or more consecutive days. "
        "It must be submitted within 3 working days of returning to work."
    ),

    "Q05": (
        "Salary is credited to the employee's registered bank account by the 7th "
        "of the following month. The payroll cut-off date is the 24th of each month."
    ),

    "Q06": (
        "For an L4 (Senior) grade employee, the CTC range is Rs. 16.0 lakhs to "
        "Rs. 26.0 lakhs per annum. The annual bonus target for this grade is "
        "10% of CTC."
    ),

    # PDF: "Coverage of up to Rs. 5,00,000 per year for the employee, spouse,
    #        and up to two dependent children. All premiums are fully paid by the Company."
    "Q07": (
        "Employees are provided Group Medical Insurance with coverage of up to "
        "Rs. 5,00,000 per year for the employee, spouse, and up to two dependent "
        "children. All premiums are fully paid by the Company."
    ),

    # PDF PIP section includes: trigger, duration, weekly check-ins, extension clause
    "Q08": (
        "An employee who receives a rating of 1 or 2 in two consecutive review "
        "cycles will be placed on a formal Performance Improvement Plan (PIP). "
        "The duration is 60 to 90 days, as determined by the reporting manager "
        "and HR Business Partner. Weekly check-in meetings between the employee "
        "and manager are mandatory throughout the PIP. If partial improvement is "
        "shown, the PIP may be extended by up to 30 additional days."
    ),

    # PDF 7-stage table with owners and stage 4 detail
    "Q09": (
        "The Annual Performance Review (APR) follows a 7-stage timeline:\n"
        "1. 360-degree feedback collection: 1–20 February\n"
        "2. Employee self-assessment submission: 1–10 March\n"
        "3. Manager assessment and draft ratings: 11–20 March\n"
        "4. Calibration meeting with all L6 and above managers: 21–25 March\n"
        "5. Final ratings locked and confirmed by HR: 26–31 March\n"
        "6. One-on-one feedback discussion between employee and manager: 1–10 April\n"
        "7. Increment and promotion letters issued: 15 April by HR and Finance"
    ),

    # PDF eligibility criterion 6: "Reliable internet ≥25 Mbps + dedicated
    # distraction-free workspace at remote location"
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
        "or health advisories, available for all employees as directed by HR"
    ),

    "Q11": REFUSAL,

    # PDF: "Offered to employees at grade L5 and above, with a 4-year vesting
    #        schedule on a 1-year cliff basis."
    "Q12": (
        "Employee Stock Options (ESOPs) are offered to employees at grade L5 and "
        "above, with a 4-year vesting schedule on a 1-year cliff basis. "
        "The number of stock options to be granted is not specified in the policy."
    ),

    "Q13": REFUSAL,
    "Q14": REFUSAL,
    "Q15": REFUSAL,
}
