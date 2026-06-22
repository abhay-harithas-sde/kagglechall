"""
canonical_answers_v7.py
=======================
Verbatim-aligned answers after full PDF re-read with pdfplumber.

Critical fixes over v6 / canonical_answers.py (v4):
- Q01: Sentence ORDER matches PDF (eligibility first, then accrual rate).
        PDF: "Employees become eligible ... completion of one year ... 240 days ...
              Thereafter, Earned Leave accrues at the rate of 1.25 days per month."
- Q04: PDF says "more than 2 consecutive days" (NOT "3 or more").
        v6 had the wrong threshold — fixed back to exact PDF wording.
- Q09: Stage 4 owner is "HR and L7+ Leaders" per the PDF table.
        Also "Calibration meeting held with all L6 and above managers" is the
        exact PDF phrase. Stage/date phrasing now mirrors PDF table exactly.
- Q10: Criterion 6 phrasing mirrors PDF exactly:
        "A reliable internet connection with a minimum speed of 25 Mbps is
         available at the remote location, along with a dedicated,
         distraction-free workspace."
        Also: WFH table column headings / descriptions taken verbatim.
"""

REFUSAL = (
    "I'm sorry, I can only answer HR-related questions based on "
    "Zyro Dynamics' internal policy documents. This question is "
    "outside the scope of our HR knowledge base."
)

ANSWERS = {
    # ── PDF (02_Leave_Policy.pdf, Page 2-3) ──────────────────────────────────
    # "Employees become eligible for 15 days of Earned Leave upon completion of
    #  one year of continuous service, provided they have worked for a minimum of
    #  240 days in that year. Thereafter, Earned Leave accrues at the rate of
    #  1.25 days per month."
    "Q01": (
        "Employees become eligible for 15 days of Earned Leave upon completion of "
        "one year of continuous service, provided they have worked for a minimum of "
        "240 days in that year. Thereafter, Earned Leave accrues at the rate of "
        "1.25 days per month."
    ),

    # ── PDF (02_Leave_Policy.pdf, Page 3) ────────────────────────────────────
    # "A maximum of 45 days of Earned Leave may be carried forward at the end of
    #  each financial year (31 March). Any balance exceeding this limit will be
    #  automatically encashed at the employee's basic daily rate and credited in
    #  the April payroll."
    "Q02": (
        "A maximum of 45 days of Earned Leave may be carried forward at the end "
        "of each financial year (31 March). Any balance exceeding this limit will "
        "be automatically encashed at the employee's basic daily rate and credited "
        "in the April payroll."
    ),

    # ── PDF (02_Leave_Policy.pdf, Page 3) ────────────────────────────────────
    # "Female employees who have completed a minimum of 80 days of service in the
    #  12 months preceding the expected date of delivery are entitled to 26 weeks
    #  of paid Maternity Leave, in accordance with the Maternity Benefit
    #  (Amendment) Act, 2017. This entitlement applies to the first two live
    #  births. For a third child, the entitlement is 12 weeks."
    "Q03": (
        "Female employees who have completed a minimum of 80 days of service in "
        "the 12 months preceding the expected date of delivery are entitled to "
        "26 weeks of paid Maternity Leave. This entitlement applies to the first "
        "two live births. For a third child, the entitlement is 12 weeks."
    ),

    # ── PDF (02_Leave_Policy.pdf, Page 2) ────────────────────────────────────
    # EXACT PDF: "Sick Leave taken for more than 2 consecutive days requires a
    # Medical Certificate from a registered medical practitioner, to be submitted
    # within 3 working days of returning to work."
    # NOTE: The question asks "for more than 2 consecutive days" which matches
    # the PDF's exact phrasing. v6 incorrectly changed this to "3 or more".
    "Q04": (
        "A Medical Certificate from a registered medical practitioner is required "
        "for sick leave taken for more than 2 consecutive days. "
        "It must be submitted within 3 working days of returning to work."
    ),

    # ── PDF (06_Compensation_and_Benefits_Policy.pdf, Page 1) ────────────────
    # "Salaries and professional fees are processed and credited to the employee's
    #  registered bank account by the 7th of the following month."
    # "The payroll cut-off date is the 24th of each month."
    "Q05": (
        "Salaries are credited to the employee's registered bank account by the "
        "7th of the following month. The payroll cut-off date is the 24th of "
        "each month."
    ),

    # ── PDF (06_Compensation_and_Benefits_Policy.pdf, Page 3) ────────────────
    # Table row: "L4 Senior | Rs. 16.0L to Rs. 26.0L | 10% of CTC"
    "Q06": (
        "For an L4 (Senior) grade employee, the CTC range is Rs. 16.0 lakhs to "
        "Rs. 26.0 lakhs per annum. The annual bonus target for this grade is "
        "10% of CTC."
    ),

    # ── PDF (06_Compensation_and_Benefits_Policy.pdf, Page 3) ────────────────
    # "Group Medical Insurance: Coverage of up to Rs. 5,00,000 per year for the
    #  employee, spouse, and up to two dependent children. All premiums are fully
    #  paid by the Company."
    "Q07": (
        "Employees are provided Group Medical Insurance with coverage of up to "
        "Rs. 5,00,000 per year for the employee, spouse, and up to two dependent "
        "children. All premiums are fully paid by the Company."
    ),

    # ── PDF (05_Performance_Review_Policy.pdf, Page 3) ───────────────────────
    # "An employee who receives a rating of 1 or 2 in two consecutive review
    #  cycles will be placed on a formal Performance Improvement Plan."
    # "Duration: 60 to 90 days, as determined by the reporting manager and HR
    #  Business Partner."
    # "Weekly check-in meetings between the employee and the manager are mandatory
    #  throughout the PIP period."
    # "Partial improvement: The PIP may be extended by up to 30 additional days
    #  at the joint discretion of HR and the manager."
    "Q08": (
        "An employee who receives a rating of 1 or 2 in two consecutive review "
        "cycles will be placed on a formal Performance Improvement Plan (PIP). "
        "The PIP duration is 60 to 90 days, as determined by the reporting manager "
        "and HR Business Partner. Weekly check-in meetings between the employee "
        "and the manager are mandatory throughout the PIP period. If partial "
        "improvement is shown, the PIP may be extended by up to 30 additional days "
        "at the joint discretion of HR and the manager."
    ),

    # ── PDF (05_Performance_Review_Policy.pdf, Page 3) ───────────────────────
    # Table verbatim (stage | activity | timeline | owner):
    # 1 | 360 degree feedback collected from peers and subordinates | 1 to 20 Feb | HR System
    # 2 | Employee self-assessment submitted on ZyroHR portal | 1 to 10 March | Employee
    # 3 | Manager completes assessment and submits draft rating | 11 to 20 March | Reporting Manager
    # 4 | Calibration meeting held with all L6 and above managers | 21 to 25 March | HR and L7+ Leaders
    # 5 | Final ratings locked and confirmed by HR | 26 to 31 March | HR
    # 6 | One-on-one feedback conversation between employee and manager | 1 to 10 April | Manager
    # 7 | Increment and promotion letters issued | 15 April | HR and Finance
    "Q09": (
        "The Annual Performance Review (APR) follows a 7-stage process:\n"
        "1. 360-degree feedback collected from peers and subordinates: 1 to 20 February\n"
        "2. Employee self-assessment submitted on ZyroHR portal: 1 to 10 March\n"
        "3. Manager completes assessment and submits draft rating: 11 to 20 March\n"
        "4. Calibration meeting held with all L6 and above managers: 21 to 25 March\n"
        "5. Final ratings locked and confirmed by HR: 26 to 31 March\n"
        "6. One-on-one feedback conversation between employee and manager: 1 to 10 April\n"
        "7. Increment and promotion letters issued: 15 April by HR and Finance"
    ),

    # ── PDF (03_Work_From_Home_Policy.pdf, Pages 1-2) ────────────────────────
    # Eligibility criteria (verbatim bullets):
    # • Completed a minimum of 6 months of continuous service at Zyro Dynamics.
    # • Currently holding grade L3 or above.
    # • Has received a performance rating of Meets Expectations or above in the
    #   most recent performance review cycle.
    # • Has no active Performance Improvement Plan or ongoing disciplinary proceedings.
    # • The nature of the role is assessed as suitable for remote execution by
    #   the reporting manager.
    # • A reliable internet connection with a minimum speed of 25 Mbps is available
    #   at the remote location, along with a dedicated, distraction-free workspace.
    #
    # WFH types table (verbatim):
    # Hybrid WFH | Fixed WFH days as agreed with reporting manager in writing | L3+ | 3 days
    # Full Remote | Employee works entirely from a remote location, formally approved | L5+ case-by-case | 5 days
    # Ad-hoc WFH | Unplanned, single-day WFH requests for personal or minor health reasons | L3+ | 2 days
    # Emergency WFH | Activated during declared emergencies, natural disasters, or health advisories | All employees | As directed by HR
    "Q10": (
        "To be eligible for a WFH arrangement, an employee must satisfy all of the "
        "following criteria:\n"
        "1. Completed a minimum of 6 months of continuous service at Zyro Dynamics\n"
        "2. Currently holding grade L3 or above\n"
        "3. Has received a performance rating of Meets Expectations or above in the "
        "most recent performance review cycle\n"
        "4. Has no active Performance Improvement Plan or ongoing disciplinary proceedings\n"
        "5. The nature of the role is assessed as suitable for remote execution by "
        "the reporting manager\n"
        "6. A reliable internet connection with a minimum speed of 25 Mbps is available "
        "at the remote location, along with a dedicated, distraction-free workspace\n\n"
        "The four types of WFH arrangements are:\n"
        "1. Hybrid WFH: Fixed WFH days as agreed with the reporting manager in writing, "
        "available for L3 and above, up to 3 days per week\n"
        "2. Full Remote: Employee works entirely from a remote location with formal "
        "approval, available for L5 and above on a case-by-case basis, up to 5 days per week\n"
        "3. Ad-hoc WFH: Unplanned, single-day WFH requests for personal or minor health "
        "reasons, available for L3 and above, up to 2 days per week\n"
        "4. Emergency WFH: Activated during declared emergencies, natural disasters, or "
        "health advisories, available for all employees as directed by HR"
    ),

    # ── Out-of-scope: recruitment/hiring process ──────────────────────────────
    "Q11": REFUSAL,

    # ── PDF (06_Compensation_and_Benefits_Policy.pdf, Page 3) ────────────────
    # "Employee Stock Options (ESOP): Offered to employees at grade L5 and above,
    #  with a 4-year vesting schedule on a 1-year cliff basis."
    # The policy does not state the number of options — correct to say "not specified".
    "Q12": (
        "Employee Stock Options (ESOPs) are offered to employees at grade L5 and "
        "above, with a 4-year vesting schedule on a 1-year cliff basis. "
        "The number of stock options to be granted is not specified in the policy."
    ),

    # ── Out-of-scope: financial performance ──────────────────────────────────
    "Q13": REFUSAL,

    # ── Out-of-scope: product features / competitor comparison ───────────────
    "Q14": REFUSAL,

    # ── Out-of-scope: leave policy at other companies ────────────────────────
    "Q15": REFUSAL,
}
