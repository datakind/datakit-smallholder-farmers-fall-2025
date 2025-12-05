--Making the sub-themes more condensed, so the number of fields is reduced for more efficient analysis

ALTER TABLE questions_deduped 
ADD COLUMN financial_theme_condensed VARCHAR;

UPDATE questions_deduped
SET financial_theme_condensed =
    CASE
        ------------------------------------------------------------
        -- MARKET PRICES
        ------------------------------------------------------------
        WHEN matched_keyword IN (
            'prices_price_discovery',
            'prices_cost_as_price',
            'prices_trade_terms'
        ) THEN 'price_discovery'

        WHEN matched_keyword = 'prices_market_access'
        THEN 'market_access'   -- or also 'price_discovery' if you want 1 bucket

        ------------------------------------------------------------
        -- CREDIT / LOANS
        ------------------------------------------------------------
        -- Loan access: general borrowing, SACCO, banks, “lend me money”
        WHEN matched_keyword IN (
            'credit_general_loan',
            'credit_sacco_loan',
            'credit_banks_investment',
            'credit_lend_me_money',
            'credit_need_funds_investment'
        ) THEN 'loan_access'

        -- Startup capital / money to start
        WHEN matched_keyword IN (
            'credit_startup_capital',
            'credit_startup_money',
            'credit_need_funds_capital'
        ) THEN 'startup_capital'

        -- Loan requirements
        WHEN matched_keyword = 'credit_collateral_guarantor'
        THEN 'loan_requirements'

        ------------------------------------------------------------
        -- PROFITABILITY / ECONOMICS
        ------------------------------------------------------------
        -- Profit & returns
        WHEN matched_keyword IN (
            'profitability_profit_returns',
            'profitability_gross_margin',
            'profitability_cash_crop_money'
        ) THEN 'profit_returns'

        -- Investment evaluation / which enterprise, is it a good investment
        WHEN matched_keyword IN (
            'profitability_investment_evaluation',
            'profitability_business_choice',
            'profitability_money_option_choice',
            'profitability_money_from_farming'
        ) THEN 'investment_evaluation'

        -- Cheapest / low-cost options
        WHEN matched_keyword = 'profitability_cheapest_option'
        THEN 'cheap_option'

        -- Quick money / short-term return
        WHEN matched_keyword IN (
            'profitability_make_money_fast',
            'profitability_quick_money'
        ) THEN 'quick_money'

        -- “Pay me well”, income expectation language
        WHEN matched_keyword = 'profitability_pay_me_well'
        THEN 'income_expectation'

        ------------------------------------------------------------
        -- GENERAL FINANCIAL CHALLENGE
        ------------------------------------------------------------
        -- General money hardship
        WHEN matched_keyword IN (
            'hardship_need_money',
            'hardship_no_funds',
            'hardship_cannot_afford',
            'hardship_too_expensive'
        ) THEN 'money_hardship'

        -- Poverty / financial stress
        WHEN matched_keyword IN (
            'hardship_poverty',
            'hardship_poor',
            'hardship_financial_problem'
        ) THEN 'poverty_financial_stress'

        -- Reward / WeFarm prize money
        WHEN matched_keyword = 'hardship_wefarm_reward_money'
        THEN 'reward_money'

        ------------------------------------------------------------
        -- SAVINGS / INVESTMENT / GROUPS
        ------------------------------------------------------------
        WHEN matched_keyword = 'savings_personal_saving'
        THEN 'personal_savings'

        WHEN matched_keyword IN (
            'savings_group_contribution',
            'savings_group_vsla_sacco',
            'savings_rotating_group'
        ) THEN 'group_savings'

        ------------------------------------------------------------
        -- PAYMENTS / TRANSACTIONS / PROPOSED SALES
        ------------------------------------------------------------
        WHEN matched_keyword IN (
            'payment_payment_language',
            'payment_transaction',
            'payment_cash_out'
        ) THEN 'payments'

        WHEN matched_keyword = 'payment_proposed_sale'
        THEN 'proposed_sales'

        ------------------------------------------------------------
        -- GRANTS / SUBSIDIES / SUPPORT
        ------------------------------------------------------------
        WHEN matched_keyword IN (
            'support_subsidy_inputs',
            'support_programs',
            'support_cash_transfer'
        ) THEN 'subsidies_inputs'

        WHEN matched_keyword IN (
            'support_grants_funding',
            'support_voucher'
        ) THEN 'grants_funding'

        ------------------------------------------------------------
        -- INSURANCE / RISK / COMPENSATION
        ------------------------------------------------------------
        WHEN matched_keyword = 'insurance_insurance'
        THEN 'insurance'

        WHEN matched_keyword = 'insurance_compensation'
        THEN 'compensation'

        ------------------------------------------------------------
        -- EVERYTHING ELSE
        ------------------------------------------------------------
        ELSE NULL
    END;
        
        
