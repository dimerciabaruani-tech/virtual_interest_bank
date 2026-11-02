# Virtual Interest Bank

A Python command-line app that helps you make smarter money choices. Enter an amount and a target rate, and it ranks the best-matching South African savings, fixed deposit, notice account and personal loan products, projecting what each would earn or cost you.

## Features

- **Four calculators:** savings, fixed deposit, notice account and personal loan.
- **Top 3 ranking** for each product type, filtered to the products you actually qualify for (minimum deposit, loan limits).
- **Projections for every product:** future value and interest earned for investments; monthly repayment for loans.
- **Real loan cost:** includes the initiation fee, the monthly service fee and credit life insurance charged on the declining balance, with a month-by-month premium breakdown.
- **Data-driven:** rates live in CSV files, so updating a rate means editing a file, not code.
- **Forgiving:** invalid menu input is re-prompted, malformed CSV rows are skipped, and missing files give a clear message.

## Getting started

Requires Python 3.6 or newer. There are no third-party dependencies.

```bash
git clone https://github.com/dimerciabaruani-tech/virtual_interest_bank.git
cd virtual_interest_bank
python main.py
```

Run it from the project root: the rate files are loaded using paths relative to the folder you run the command from.

## Usage

1. Type `start` to begin (or `quit` to exit).
2. Choose what to calculate by typing one of: `savings`, `fixed deposit`, `notice account`, `personal loan`.
3. Answer the prompts.

| Product | You enter |
| --- | --- |
| Savings, fixed deposit, notice account | principal, rate (%), compounding periods per year, years until maturity |
| Personal loan | principal, rate (%), loan term in months |

Example (savings, R10,000 at 8% for 5 years, compounded monthly):

```
If you chose to save R10,000.00 at 8.00%
after 5 years, you'd have R14,898.46
```

The app then lists the top three matching products from the rates data.

## How it works

Investments use compound interest, and loans use the standard amortisation formula:

```
FV = P x (1 + r/n) ^ (n x t)
M  = P x [i x (1 + i)^n] / [(1 + i)^n - 1]
```

For loans, the true monthly cost adds three things to the instalment:

- The initiation fee (up to R1,207.50), added to the capital so it accrues interest.
- A R69 monthly service fee.
- Credit life insurance at R4.50 per R1,000 of outstanding balance, so the premium falls as the loan is repaid.

Example: R20,000 at 24% over 36 months gives an instalment of R832.03 and a true monthly cost of about R955.69 (using the average credit life premium of R54.66).

## Project structure

```
virtual_interest_bank/
├── main.py            user input, CSV reading, ranking and display
├── finfunctions.py    financial formulas (pure functions)
└── interest rates/
    ├── savings/
    │   └── sa_savings_rates.csv
    ├── investments/
    │   ├── sa_fixed_deposit_rates.csv
    │   └── sa_notice_account_rates.csv
    └── personal-loans/
        └── sa_personal_loan_rates.csv
```

### Rate file columns

| File | Columns used |
| --- | --- |
| `sa_savings_rates.csv` | `bank`, `product_name`, `min_deposit`, `max_rate`, `access_type` |
| `sa_fixed_deposit_rates.csv` | `bank`, `min_deposit`, `nominal_rate`, `effective_rate`, `term_months`, `min_age` |
| `sa_notice_account_rates.csv` | `bank`, `min_deposit`, `nominal_rate`, `notice_period_days`, `min_age` |
| `sa_personal_loan_rates.csv` | `lender`, `from_rate`, `max_amount`, `max_term_months`, `is_nca_cap_fallback`, `credit_life`, `notes` |

Rates are percentages (for example `8.5`). Where a lender does not publish a rate, `is_nca_cap_fallback` is `TRUE` and the app notes that the figure is the National Credit Act maximum.

## Limitations and roadmap

- Rates are a snapshot and will go out of date; real offers depend on each lender's credit assessment.
- Loans are calculated over the maximum term only.
- The initiation fee is always the maximum amount, which overstates the cost of small loans.
- Planned: input validation, refactoring the product blocks into shared functions, pytest tests for `finfunctions.py`, term comparison for loans, and a web front end.

## Disclaimer

Projections are estimates based on published rates and are not financial advice.

## Author

Dimercia K. Baruani. [GitHub](https://github.com/dimerciabaruani-tech)

## License

Released under the [MIT License](LICENSE).
