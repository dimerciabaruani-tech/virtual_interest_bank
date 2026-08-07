#formulas
#fixed values
INITIATION_FEE = 1207.50 #maximum amount aaded to loan capital upfront, accrues interest
MONTHLY_SERVICE_FEE = 69 #added to the monthly repayments, not part of the interest calculation

#savings/fixed deposits/notice accounts all use this formula:
#FV = P x (1 + nominal rate / compound years) ^ (compound years x t) 

def future_value(principal, rate, compound_years, period):
    fv = principal * (1 + rate / compound_years) ** (compound_years * period)
    return fv

def cal_effective_rate(rate, compound_years):
    effective_rate = (1 + rate / compound_years) ** compound_years - 1
    return effective_rate

def interest_earned(principal, fv):
    ie = fv - principal
    return ie

#loan repayments all use this formula:
#M = P x [monthly_rate x (1 + monthly_rate) ^ n] / [(1 + monthly_rate) ^ n - 1]

def monthly_rate(rate):
    m_rate = rate / 12
    return m_rate

def monthly_installment(principal, m_rate, months):
    p_financed = principal + INITIATION_FEE
    m_installment = p_financed * (m_rate * (1 + m_rate) ** months) / \
    ((1 + m_rate) ** months - 1)
    return m_installment

def total_repaid(m_installment, months):
    t_repaid = m_installment * months
    return t_repaid

def credit_life_monthly(principal, m_rate, m_installment, months):
    balance = principal + INITIATION_FEE
    credit_life_installments = [] #this list will hold all our creditLife installments
    for payment in range(months):
        interest_payable = balance * m_rate
        principal_payment = m_installment - interest_payable
        credit_life_charge = (balance / 1000) * 4.50
        credit_life_installments.append(credit_life_charge)
        balance -= principal_payment
    credit_life_insurance = sum(credit_life_installments)
    number_of_payments = len(credit_life_installments)
    return credit_life_insurance, number_of_payments, credit_life_installments

def true_month_cost(m_installment, credit_life_insurance):
    true_m_cost = m_installment + MONTHLY_SERVICE_FEE + credit_life_insurance
    return true_m_cost