import finfunctions as fin
import csv

print('---------------------------- Virtual Interest Bank ----------------------------')
print('-------------------------------- MAKE SMARTER ---------------------------------')
print('-------------------------------- MONEY CHOICES --------------------------------')

# Loop until the user actually types 'start' (or decides to quit)
while True:
    print('--------------------------------- ENTER START -------------------------------- ')
    start_app = input('> ').lower()
    if start_app == 'start':
        break
    elif start_app in ('quit', 'exit'):
        print('\nGoodbye!')
        raise SystemExit
    else:
        print(f"\n'{start_app}' wasn't recognised. Please type 'start' to begin (or 'quit' to exit).\n")

print('\n 1. Savings \n 2. Fixed Deposit \n 3. Notice Account \n 4. Personal Loan')
while True:
    option_screen = input("\nWhat would you like to calculate? ").lower()
    if option_screen in ['savings', 'fixed deposit', 'notice account', 'personal loan']:
        break
    else:
        print(
            f"\n'{option_screen}' was not recognised as a valid option. "
            "Please enter any of the valid options below:\n"
            "savings \ fixed deposit \ notice account \ personal loan"
            )

savings_and_investments = ['savings', 'fixed deposit', 'notice account']
loans = ['personal loan']

if option_screen in savings_and_investments:
    principal = float(input('\nEnter principal amount: '))
    rate = float(input('Enter rate (%): ')) / 100
    compound_years = int(input('Enter compound years: '))
    period = int(input('Enter the amount of years until maturity: '))
    fv = fin.future_value(principal, rate, compound_years, period)

    if option_screen in ['fixed deposit', 'notice account']:
        print(
            f"\nIf you chose to invest R{principal:,.2f} at {rate * 100:.2f}% \n"
            f"for {period} years, you'd have R{fv:,.2f}"
        )
    elif option_screen == 'savings':
        print(
            f"\nIf you chose to save R{principal:,.2f} at {rate * 100:.2f}% \n"
            f"after {period} years, you'd have R{fv:,.2f}"
        )

if option_screen in loans:
    principal = float(input('Enter principal amount: '))
    rate = float(input('Enter rate (%): ')) / 100
    m_rate = fin.monthly_rate(rate)
    months = int(input('Enter loan term in months: '))
    monthly_payments = fin.monthly_installment(principal, m_rate, months)

    print(
        f"If you took out a loan of R{principal:,.2f} at {rate * 100:.2f}% \n"
        f"You'd be required to pay R{monthly_payments:,.2f} for {months} months"
    )

if option_screen == 'savings':
    eligible_products = []
    try:
        with open('interest rates/savings/sa_savings_rates.csv', 'r') as savings_csv:
            reader = csv.DictReader(savings_csv)
            for row in reader:
                try:
                    min_dep = float(row['min_deposit'])
                    max_rate = float(row['max_rate'])
                    access_type = row['access_type']
                    if min_dep <= principal:
                        eligible_products.append(row)
                except (ValueError, KeyError):
                    continue  # instead of breaking on an error, errors are skipped
    except FileNotFoundError:
        print(
            "\nSorry, the savings rates file couldn't be found "
            "(expected at 'interest rates/savings/sa_savings_rates.csv')."
            "\nPlease check the file exists and try again."
        )
    except (csv.Error, PermissionError, OSError) as e:
        print(f"\nSomething went wrong while reading the savings rates file: {e}")
    else:
        eligible_products.sort(key=lambda x: float(x['max_rate']), reverse=True)
        top_products = eligible_products[:3]

        if not eligible_products:
            print(
                f"Your principal amount of R{principal:.2f} is lower than the minimum deposit"
                f"required for all available products."
            )
        else:
            overall_max_rate = max(float(row['max_rate']) for row in eligible_products) / 100
            if rate > overall_max_rate:
                print(
                    f"\nYour desired rate of {rate * 100:.2f}% is higher "
                    f"than the best available rate of {overall_max_rate * 100:.2f}%."
                    "\nConsider adjusting your expectations."
                )
            else:
                print(f"\nHere are the Top 3 Best Savings Products ranked by highest interest rates. \n")
                for index, value in enumerate(top_products, start=1):
                    bank = value['bank']
                    product = value['product_name']
                    access_period = value['access_type']
                    rate_percentage = float(value['max_rate'])
                    rate_decimal = rate_percentage / 100

                    fv = fin.future_value(principal, rate_decimal, compound_years, period)
                    interest = fin.interest_earned(principal, fv)

                    print(f'{index}. {bank} - {product}')
                    print(f'       Max rate : {rate_percentage:.2f}%')
                    print(f'       Future value after {period} years : R{fv:,.2f}')
                    print(f'       Interest earned : R{interest:,.2f}')
                    print(f'       Access Type : {access_period}\n')

if option_screen == 'fixed deposit':
    eligible_products = []
    try:
        with open('interest rates/investments/sa_fixed_deposit_rates.csv', 'r') as fixed_deposit_csv:
            reader = csv.DictReader(fixed_deposit_csv)
            for row in reader:
                try:
                    min_dep = float(row['min_deposit'])
                    nominal_rate = float(row['nominal_rate'])
                    effective_rate = float(row['effective_rate'])
                    investment_period = row['term_months']
                    if min_dep <= principal:
                        eligible_products.append(row)
                except (ValueError, KeyError):
                    continue  # instead of breaking on an error, errors are skipped
    except FileNotFoundError:
        print(
            "\nSorry, the fixed deposit rates file couldn't be found "
            "(expected at 'interest rates/investments/sa_fixed_deposit_rates.csv')."
            "\nPlease check the file exists and try again."
        )
    except (csv.Error, PermissionError, OSError) as e:
        print(f"\nSomething went wrong while reading the fixed deposit rates file: {e}")
    else:
        eligible_products.sort(key=lambda x: float(x['effective_rate']), reverse=True)
        top_products = eligible_products[:3]

        if not eligible_products:
            print(
                f"Your principal amount of R{principal:.2f} is lower than the minimum deposit"
                f"required for all available products."
                "\nConsider adjusting your expectations."
            )
        else:
            max_effective_rate = max(float(row['effective_rate']) for row in eligible_products) / 100
            if rate > max_effective_rate:
                print(
                    f"\nYour desired rate of {rate * 100:.2f}% is higher "
                    f"than the best available rate of {max_effective_rate * 100:.2f}%."
                    "\nConsider adjusting your expectations."
                )
            else:
                print(f"\nHere are the Top 3 Best Fixed Deposit Products ranked by highest interest rates. \n")
                for index, value in enumerate(top_products, start=1):
                    bank = value['bank']
                    investment_term = int(value['term_months']) / 12
                    rate_percentage = float(value['effective_rate']) / 100
                    nominal_rate_percentage = float(value['nominal_rate'])
                    rate_decimal = nominal_rate_percentage / 100
                    min_age = value['min_age']

                    fv = fin.future_value(principal, rate_decimal, 12, investment_term)
                    interest = fin.interest_earned(principal, fv)

                    print(f'{index}. {bank}')
                    print(f'       Max rate: {rate_percentage * 100:.2f}%')
                    print(f'       Investment period : {investment_term * 12} months')
                    print(f'       Future value : R{fv:,.2f}')
                    print(f'       Interest earned : R{interest:,.2f}')
                    print(f'       Minimum age to qualify : {min_age}\n')
        print(f'    Remember funds in a fixed deposit can only be accessed after the investment period is realised'
                    'All these projections have been made to compound monthly as per the \n'
                    'standard SA convention. This is more inline with common investment practices \n'
                    'used by financial institutions in South Africa'
              )

if option_screen == 'notice account':
    eligible_products = []
    try:
        with open('interest rates/investments/sa_notice_account_rates.csv', 'r') as notice_acc_rates_csv:
            reader = csv.DictReader(notice_acc_rates_csv)
            for row in reader:
                try:
                    min_dep = float(row['min_deposit'])
                    nominal_rate = float(row['nominal_rate'])
                    notice_period_in_days = int(row['notice_period_days'])
                    if min_dep <= principal:
                        eligible_products.append(row)
                except (ValueError, KeyError):
                    continue  # instead of breaking on an error, errors are skipped
    except FileNotFoundError:
        print(
            "\nSorry, the notice account rates file couldn't be found "
            "(expected at 'interest rates/investments/sa_notice_account_rates.csv')."
            "\nPlease check the file exists and try again."
        )
    except (csv.Error, PermissionError, OSError) as e:
        print(f"\nSomething went wrong while reading the notice account rates file: {e}")
    else:
        eligible_products.sort(key=lambda x: float(x['nominal_rate']), reverse=True)
        top_products = eligible_products[:3]

        if not eligible_products:
            print(
                f"Your principal amount of R{principal:.2f} is lower than the minimum deposit"
                f"\nrequired for all available products.\n"
                "Consider adjusting your expectations.\n"
            )
        else:
            effective_rates = []
            for row in eligible_products:
                row_nominal_rate = float(row['nominal_rate']) / 100
                effective_rate = fin.cal_effective_rate(row_nominal_rate, 12)
                effective_rates.append(effective_rate)
            max_effective_rate = max(effective_rates)
            if rate > max_effective_rate:
                print(
                    f"\nYour desired rate of {rate * 100:.2f}% is higher "
                    f"than the best available rate of {max_effective_rate * 100:.2f}%."
                    "\nConsider adjusting your expectations."
                )
            else:
                print(f"\nHere are the Top 3 Best Notice Account Products ranked by highest interest rates. \n")
                for index, value in enumerate(top_products, start=1):
                    bank = value['bank']
                    notice_period_days = int(value['notice_period_days'])
                    product_rate = float(value['nominal_rate']) / 100
                    e_rate = fin.cal_effective_rate(product_rate, compound_years)
                    min_age = value['min_age']

                    fv = fin.future_value(principal, product_rate, 12, period)
                    interest = fin.interest_earned(principal, fv)

                    print(f'{index}. {bank}')
                    print(f'       Max rate: {e_rate * 100:.2f}%')
                    print(f'       Future value : R{fv:,.2f}')
                    print(f'       Interest earned : R{interest:,.2f}')
                    print(f'       Notice period : {notice_period_days} days')
                    print(f'       Minimum age to qualify : {min_age}\n')
                print(f'Remember to access funds in your notice account you\'d have to give sufficient notice \n'
                      'to the bank as per the notice period stated. After the notice period you will be able \n'
                      'to access your funds.\n'

                      '\nAll these projections have been made to compound monthly as per the \n'
                      'standard SA convention. This is more inline with common investment practices \n'
                      'used by financial institutions in South Africa'
                      )

if option_screen == 'personal loan':
    all_products = []
    eligible_products = []
    try:
        with open('interest rates/personal-loans/sa_personal_loan_rates.csv', 'r') as loan_rates_csv:
            reader = csv.DictReader(loan_rates_csv)
            for row in reader:
                try:
                    max_amount = int(row['max_amount'])
                    product_rate = float(row['from_rate'])
                    is_nca_fallback_raw = row['is_nca_cap_fallback']
                    max_term_months = int(row['max_term_months'])
                    all_products.append(row)
                    if product_rate <= rate * 100 and principal <= max_amount:
                        eligible_products.append(row)
                except (ValueError, KeyError):
                    continue  # instead of breaking on an error, errors are skipped
    except FileNotFoundError:
        print(
            "\nSorry, the personal loan rates file couldn't be found "
            "(expected at 'interest rates/personal-loans/sa_personal_loan_rates.csv')."
            "\nPlease check the file exists and try again."
        )
    except (csv.Error, PermissionError, OSError) as e:
        print(f"\nSomething went wrong while reading the personal loan rates file: {e}")
    else:
        eligible_products.sort(key=lambda x: float(x['from_rate']), reverse=False)
        top_products = eligible_products[:3]

        if not eligible_products:
            if all_products:
                lowest_rate = min(float(row['from_rate']) for row in all_products) / 100
                print(
                    f"\nNo lender currently matches your target rate of {rate * 100:.2f}% "
                    f"and loan amount of R{principal:,.2f}."
                    f"\nThe lowest rate on record is {lowest_rate * 100:.2f}% "
                    "(subject to loan amount limits)."
                    "\nConsider adjusting your expectations."
                )
            else:
                print("\nNo personal loan products were found.")
        else:
            print(f"\nHere are the Top 3 Best Personal Loan Products ranked by lowest interest rates. \n")
            for index, value in enumerate(top_products, start=1):
                lender = value['lender']
                product_rate = float(value['from_rate']) / 100
                product_monthly_rate = fin.monthly_rate(product_rate)
                is_nca_fallback = value['is_nca_cap_fallback'].strip().upper() == 'TRUE'
                maximum_term = int(value['max_term_months'])
                credit_life = value['credit_life']
                disclaimer = value['notes']

                monthly_repayment = fin.monthly_installment(principal, product_monthly_rate, maximum_term)

                print(f'{index}. {lender}')
                print(f'       Rate : {product_rate * 100:.2f}%')
                if is_nca_fallback:
                    print(f'      this rate is the maximum chargeable as per the National Credit Act\n'
                          '       the institution currently does not have a publicly published rate\n'
                          '       See the disclaimer for more details.'
                          )
                print(f'       Maximum loan term : {maximum_term} months')
                print(f'       Monthly repayment : R{monthly_repayment:,.2f}')
                if credit_life == 'mandatory':
                    print(f'       Credit Life : {credit_life}')
                    #the credit_life_monthly function returns 3 values
                    credit_life_insurance, num_payments, installments = fin.credit_life_monthly(
                        principal, product_monthly_rate, monthly_repayment, maximum_term
                    )
                    avg_credit_life = credit_life_insurance / num_payments
                    true_cost = fin.true_month_cost(monthly_repayment, avg_credit_life)
                    print(f'       Avg. monthly credit life premium : R{avg_credit_life:,.2f}')
                    print(f'       True monthly cost (incl. service fee & credit life) : R{true_cost:,.2f}')
                    print(f'        Real monthly credit life premiums:')    
                    for payment in installments:
                        #installments continuously decrease so no monthly payment is one and the same 
                        indx = installments.index(payment) + 1
                        print(f'        Month {indx} : R{payment:,.2f}')
                else:
                    print(f'       Credit Life : {credit_life}')
                print(f'       Disclaimer : {disclaimer}\n')

            print('Note that these figures have been calculated using the maximum term possible\n'
                  'If you wish to reduce the term you\'ll be able to pay off the loan faster but\n'
                  'the monthly repayments would be higher'

                  '\nloans are tailored to each person based on a credit assessment conducted\n'
                  'by the financial institution offering the credit. These rates and figures should be\n'
                  'treated as speculative. Please consult the official company website for more information.\n'

                  '\nCredit life is an insurance premium paid to the lender by the consumer in order to cover\n'
                  'the loan incase the consumer were unable to do so by nature of disability or loss of income.\n'
                  'The figure listed as "Avg. monthly credit life premium" is just an average of all the \n'
                  'installments made over the full repayment period. Realistically as you pay back the loan\n'
                  'your credit life monthly premium will decrease.'
                  )
