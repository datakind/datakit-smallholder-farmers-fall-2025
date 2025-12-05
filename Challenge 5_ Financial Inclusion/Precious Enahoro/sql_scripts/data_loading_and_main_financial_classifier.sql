--Loading Main Data File
CREATE TABLE my_table_tagged_chunked AS
SELECT *,
row_number() OVER ()  AS org_idx,
FROM read_csv_auto('C:\Users\enaho\Downloads\eng_data.csv');

--Main Financial Categories Classifier
CREATE TABLE questions_financial_tagged_2 AS
SELECT
    t.*,
    CASE 
        WHEN financial_subcategory IS NULL THEN 'No'
        ELSE 'Yes'
    END AS financial_flag
FROM (
    SELECT
        q.*,

        ------------------------------------------------------------
        -- MAIN FINANCIAL SUBCATEGORY CLASSIFIER (CLEANED)
        ------------------------------------------------------------
        CASE
            --------------------------------------------------------
            -- 1. CREDIT / LOANS
            -- getting money/capital/funds/loans (incl. SACCO loans,
            -- capital needed to start)
            --------------------------------------------------------
            WHEN lower(question_content) LIKE '%loan%'
              OR lower(question_content) LIKE '%loans%'
                    OR (lower(question_content) LIKE '%need money%'
                  AND lower(question_content) LIKE '%investment%')
              OR (lower(question_content) LIKE '%need some money%'
                  AND lower(question_content) LIKE '%investment%')
              OR (lower(question_content) LIKE '%need funds%'
                  AND lower(question_content) LIKE '%investment%')

              -- commercial banks to receive investments → credit
              OR ( (lower(question_content) LIKE '%commercial bank%'
                    OR lower(question_content) LIKE '%commercial banks%'
                    OR lower(question_content) LIKE '%bank%')
                   AND lower(question_content) LIKE '%investment%' )
              OR lower(question_content) LIKE '%soft loan%'
              OR lower(question_content) LIKE '%credit%'
              OR lower(question_content) LIKE '%capital%'
              OR lower(question_content) LIKE '%microfinance%'
              OR lower(question_content) LIKE '%micro finance%'
              OR lower(question_content) LIKE '%money lending%'
              OR lower(question_content) LIKE '%lender%'
              OR lower(question_content) LIKE '%lending%'
              OR lower(question_content) LIKE '%borrow%'
              OR lower(question_content) LIKE '%borrowing%'
              --OR lower(question_content) LIKE '%advance%'
              OR lower(question_content) LIKE '%collateral%'
              OR lower(question_content) LIKE '%guarantor%'
              OR lower(question_content) LIKE '%guarantee%'
              OR lower(question_content) LIKE '%installment%'
              OR lower(question_content) LIKE '%instalment%'
              OR lower(question_content) LIKE '%pay back%'
              -- capital & funds for starting/working
              OR lower(question_content) LIKE '%capital needed%'
              OR lower(question_content) LIKE '%capital required%'
              OR lower(question_content) LIKE '%how much capital%'
              OR lower(question_content) LIKE '%capital to start%'
              OR lower(question_content) LIKE '%starting capital%'
              OR lower(question_content) LIKE '%start up capital%'
              OR lower(question_content) LIKE '%startup capital%'
              OR lower(question_content) LIKE '%working capital%'
              OR lower(question_content) LIKE '%need funds%'
              OR lower(question_content) LIKE '%need capital%'
              OR lower(question_content) LIKE '%get funds%'
              OR lower(question_content) LIKE '%get capital%'
              OR lower(question_content) LIKE '%sacco loan%'
              OR lower(question_content) LIKE '%loan from sacco%'
              OR (lower(question_content) LIKE '%sacco%' AND lower(question_content) LIKE '%loan%')
              
                            -- startup money phrased as "money", not "capital"
              OR (lower(question_content) LIKE '%how much money%'
                  AND lower(question_content) LIKE '%start%'
                 )
              OR (lower(question_content) LIKE '%minimum money%'
                  AND lower(question_content) LIKE '%start%'
                 )
              OR (lower(question_content) LIKE '%amount of money%'
                  AND lower(question_content) LIKE '%start%'
                 )

              -- explicit need money for investment → credit
              OR (lower(question_content) LIKE '%need money%'
                  AND lower(question_content) LIKE '%investment%'
                 )
              OR (lower(question_content) LIKE '%need some money%'
                  AND lower(question_content) LIKE '%investment%'
                 )
              OR (lower(question_content) LIKE '%need funds%'
                  AND lower(question_content) LIKE '%investment%'
                 )

              -- lend / borrow money directly
              OR lower(question_content) LIKE '%lend me some money%'
              OR lower(question_content) LIKE '%lend me money%'
              OR lower(question_content) LIKE '%can you lend me%'
              OR lower(question_content) LIKE '%can u lend me%'
              

or (lower(question_content)  LIKE '%lend%' and lower(question_content)  LIKE '%money%')--credit/loans


            THEN 'Credit / Loans'

            --------------------------------------------------------
            -- 2. SAVINGS / INVESTMENT / GROUPS
            -- group savings & saving behaviour (NOT investment eval)
            --------------------------------------------------------
            WHEN lower(question_content) LIKE '%saving%'
              OR lower(question_content) LIKE '%savings%'
              OR lower(question_content) LIKE '%save money%'
              OR lower(question_content) LIKE '%bank account%'
              OR lower(question_content) LIKE '%fixed deposit%'
              OR lower(question_content) LIKE '%vsla%'
              OR lower(question_content) LIKE '%vsl%'
              OR lower(question_content) LIKE '%village savings%'
              OR lower(question_content) LIKE '%sacco%'
              OR lower(question_content) LIKE '%sacco group%'
              OR lower(question_content) LIKE '%cooperative saving%'
              OR lower(question_content) LIKE '%coop saving%'
              OR lower(question_content) LIKE '%rosca%'
              OR lower(question_content) LIKE '%chama%'
              OR lower(question_content) LIKE '%tontine%'
              OR lower(question_content) LIKE '%esusu%'
              OR lower(question_content) LIKE '%merry-go-round%'
              OR lower(question_content) LIKE '%merry go round%'
              OR lower(question_content) LIKE '%share capital%'
              OR lower(question_content) LIKE '%contribution%'
              OR lower(question_content) LIKE '%member contribution%'
            THEN 'Savings / Investment / Groups'

            --------------------------------------------------------
            -- 3. MARKET PRICES
            -- price discovery, “how much”, cost as price
            --------------------------------------------------------
            WHEN lower(question_content) LIKE '%what is the price%'
              OR lower(question_content) LIKE '%market price%'
              OR lower(question_content) LIKE '%current price%'
              OR lower(question_content) LIKE '%selling price%'
              OR lower(question_content) LIKE '%buying price%'
              OR lower(question_content) LIKE '%market rate%'
              OR lower(question_content) LIKE '%rate per%'
              OR lower(question_content) LIKE '%how much%'
              OR lower(question_content) LIKE '%price%'
              OR lower(question_content) LIKE '%prices%'
              OR lower(question_content) LIKE '%cost%'
              OR lower(question_content) LIKE '%costing%'
              OR lower(question_content) LIKE '%quotation%'
              OR lower(question_content) LIKE '%quote%'
              OR lower(question_content) LIKE '%wholesale%'
              OR lower(question_content) LIKE '%retail%'
              OR lower(question_content) LIKE '%market for%'
              OR lower(question_content) LIKE '%where can i sell%'
                   or  (lower(question_content)  LIKE '%money%' and lower(question_content)  LIKE '%kg%')
            or (lower(question_content)  LIKE '%money%' and lower(question_content)  LIKE '%kilogram%')
             or (lower(question_content)  LIKE '%much%' and lower(question_content)  LIKE '%money%')--market prices
            or (lower(question_content)  LIKE '%sell%' and lower(question_content)  LIKE '%much%') --market prices

            THEN 'Market Prices'

            --------------------------------------------------------
            -- 4. PROFITABILITY / ECONOMICS
            -- which business, making money, cheap to start, costs etc.
            --------------------------------------------------------
            WHEN lower(question_content) LIKE '%more profitable%'
              OR lower(question_content) LIKE '%profitable%'
              OR lower(question_content) LIKE '%profit margin%'
              OR lower(question_content) LIKE '%profit%'
              OR lower(question_content) LIKE '%returns%'
              OR lower(question_content) LIKE '%cost benefit%'
              OR lower(question_content) LIKE '%break even%'
              OR lower(question_content) LIKE '%gross margin%'
              OR lower(question_content) LIKE '%gross margins%'
              OR lower(question_content) LIKE '%what business can i do%'
              OR lower(question_content) LIKE '%which business can i do%'
              OR lower(question_content) LIKE '%which business is best%'
              OR lower(question_content) LIKE '%best business%'
              OR lower(question_content) LIKE '%good business%'
              OR lower(question_content) LIKE '%make money%'
              OR lower(question_content) LIKE '%money fast%'
              OR lower(question_content) LIKE '%quick money%'
              OR lower(question_content) LIKE '%viable business%'
              OR lower(question_content) LIKE '%cheap to start%'
              OR lower(question_content) LIKE '%cheapest farming%'
              OR lower(question_content) LIKE '%cheapest system%'
              OR lower(question_content) LIKE '%cheap start%'
              OR lower(question_content) LIKE '%cheap produce%'
              OR lower(question_content) LIKE '%cheap between%'
              OR lower(question_content) LIKE '%low capital business%'
              OR lower(question_content) LIKE '%small capital business%'
              OR lower(question_content) LIKE '%low cost business%'
              OR lower(question_content) LIKE '%small money business%'
              OR lower(question_content) LIKE '%cost of production%'
              OR lower(question_content) LIKE '%production cost%'
              OR lower(question_content) LIKE '%reduce costs%'
              OR lower(question_content) LIKE '%reduce cost%'
              OR lower(question_content) LIKE '%cut costs%'
              OR lower(question_content) LIKE '%lower costs%'
              OR lower(question_content) LIKE '%pay me well%'
              OR lower(question_content) LIKE '%pay me back well%'
              OR lower(question_content) LIKE '%pay me overwhelmingly%'
              OR lower(question_content) LIKE '%pay me faster%'
              OR lower(question_content) LIKE '%invest in%'
              OR lower(question_content) LIKE '%investment in%'
              OR lower(question_content) LIKE '%good investment%'
              OR lower(question_content) LIKE '%minimum investment%'
              OR lower(question_content) LIKE '%investment required%'

              -- generic "good for investment" or "investment in X"
              OR lower(question_content) LIKE '%good for investment%'
              OR lower(question_content) LIKE '%agriculture investment%'
              OR lower(question_content) LIKE '%agric investment%'
              OR lower(question_content) LIKE '%investments in farming%'
              OR lower(question_content) LIKE '%investment in farming%'
              OR lower(question_content) LIKE '%investment in agriculture%'

              -- conceptual / evaluation questions about investment
              OR lower(question_content) LIKE '%suitable investment%'
              OR lower(question_content) LIKE '%which agriculture investment%'
              OR lower(question_content) LIKE '%what investment%'
              OR lower(question_content) LIKE '%why is agric called an investment%'
              OR lower(question_content) LIKE '%asset or investment%'
              OR lower(question_content) LIKE '%investment%'
               OR lower(question_content) LIKE '%investing%'
               
               OR (lower(question_content) LIKE '%cross%' AND lower(question_content) LIKE '%margin%')
              OR (lower(question_content) LIKE '%gross%' AND lower(question_content) LIKE '%margin%')
               
             or regexp_matches(lower(question_content),
                '(make money|make more money|get money in one year|get money fast|money fast|quick money|viable business)')
       

        or regexp_matches(lower(question_content),
                '(cheap to start|cheapest farming|cheapest system|cheap start|cheap produce|cheap between|low capital business|small capital business|low cost business|small money business)')
            OR (
                regexp_matches(lower(question_content),
                    '(cheap|cheapest|low cost|low capital|small capital|little money|small investment|low investment)')
                AND regexp_matches(lower(question_content),
                    '(business|system|method|rearing|venture|enterprise|project|farm|farming|poultry|broiler|layer)')
                AND NOT regexp_matches(lower(question_content),
                    '(manure|fertilizer|fertiliser|seed|feed|chemical|spray|pesticide|herbicide|drug)')
            )
    
                          -- crops / animals / business that bring money
              OR (lower(question_content) LIKE '%which crop%'
                  AND lower(question_content) LIKE '%money%')
              OR (lower(question_content) LIKE '%what crop%'
                  AND lower(question_content) LIKE '%money%')
              OR (lower(question_content) LIKE '%which plant%'
                  AND lower(question_content) LIKE '%money%')
              OR (lower(question_content) LIKE '%what plant%'
                  AND lower(question_content) LIKE '%money%')
              OR (lower(question_content) LIKE '%which business%'
                  AND lower(question_content) LIKE '%money%')
              OR (lower(question_content) LIKE '%what business%'
                  AND lower(question_content) LIKE '%money%')
              OR (lower(question_content) LIKE '%which animal%'
                  AND lower(question_content) LIKE '%money%')
              OR (lower(question_content) LIKE '%which project%'
                  AND lower(question_content) LIKE '%money%')

              -- get / earn / harvest / fetch money from farming
              OR (lower(question_content) LIKE '%get money%'
                  AND (lower(question_content) LIKE '%from %'
                       OR lower(question_content) LIKE '%through %'))
              OR lower(question_content) LIKE '%earn money%'
              OR lower(question_content) LIKE '%harvest money%'
              OR lower(question_content) LIKE '%fetch money%'
              OR lower(question_content) LIKE '%bring money%'
              OR lower(question_content) LIKE '%brings money%'
              OR lower(question_content) LIKE '%gives money%'
              OR lower(question_content) LIKE '%good money%'
              OR lower(question_content) LIKE '%money quickly%'
              OR lower(question_content) LIKE '%money quick%'
              OR lower(question_content) LIKE '%money in short time%'
              OR lower(question_content) LIKE '%money in a short time%'

              -- how much money can I get from X
              OR (lower(question_content) LIKE '%how much money%'
                  AND lower(question_content) LIKE '%get%'
                 )
              OR (lower(question_content) LIKE '%how much money%'
                  AND lower(question_content) LIKE '%from%'
                 )

              -- “cash crop … to obtain money” etc.
              OR (lower(question_content) LIKE '%cash crop%'
                  AND lower(question_content) LIKE '%money%')
                  
                   or  (lower(question_content)  LIKE '%money%' and lower(question_content)  LIKE '%start%')
            or (lower(question_content)  LIKE '%money%' and lower(question_content)  LIKE '%type%')
           or (lower(question_content)  LIKE '%best%' and lower(question_content)  LIKE '%money%') --profitability
                  or (lower(question_content)  LIKE '%get%' and lower(question_content)  LIKE '%money%') --profitability
                         or (lower(question_content)  LIKE '%grow%' and lower(question_content)  LIKE '%money%') --profitability
or (lower(question_content)  LIKE '%type%' and lower(question_content)  LIKE '%cheap%') --profitability
 or (lower(question_content)  LIKE '%between%' and lower(question_content)  LIKE '%money%')
 or (lower(question_content)  LIKE '%bring%' and lower(question_content)  LIKE '%money%')
 or (lower(question_content)  LIKE '%fetch%' and lower(question_content)  LIKE '%money%')
 or (lower(question_content)  LIKE '%earn%' and lower(question_content)  LIKE '%money%')
            THEN 'Profitability / Economics'

            --------------------------------------------------------
            -- 5. GRANTS / SUBSIDIES / SUPPORT
            --------------------------------------------------------
            WHEN (lower(question_content) LIKE '%grant%' AND lower(question_content) LIKE '%farm%')
              OR (lower(question_content) LIKE '%grants%' AND lower(question_content) LIKE '%farm%')
              OR lower(question_content) LIKE '%funding%'
              OR lower(question_content) LIKE '%government funding%'
              OR lower(question_content) LIKE '%subsidy%'
              OR lower(question_content) LIKE '%subsidies%'
              OR lower(question_content) LIKE '%input subsidy%'
              OR lower(question_content) LIKE '%fertilizer subsidy%'
              OR lower(question_content) LIKE '%support program%'
              OR lower(question_content) LIKE '%support scheme%'
              OR lower(question_content) LIKE '%financial support%'
              OR lower(question_content) LIKE '%financial assistance%'
              OR lower(question_content) LIKE '%cash transfer%'
              OR lower(question_content) LIKE '%voucher%'
              OR lower(question_content) LIKE '%redeem voucher%'
              OR lower(question_content) LIKE '%empowerment program%'
              OR lower(question_content) LIKE '%youth program%'
              OR lower(question_content) LIKE '%women program%'
            THEN 'Grants / Subsidies / Support'

            --------------------------------------------------------
            -- 6. PAYMENTS / TRANSACTIONS / PROPOSED SALES
            -- cash out, payment, basic transaction/sale phrasing
            --------------------------------------------------------
            WHEN lower(question_content) LIKE '%cash out%'
              OR lower(question_content) LIKE '%cashout%'
              OR lower(question_content) LIKE '%payment%'
              OR lower(question_content) LIKE '%payments%'
              OR lower(question_content) LIKE '%pay for%'
              OR lower(question_content) LIKE '%pay me%'
              OR lower(question_content) LIKE '%transaction%'
              OR lower(question_content) LIKE '%proposed sale%'
              OR lower(question_content) LIKE '%sale agreement%'
              OR lower(question_content) LIKE '%sell it to me at%'
              OR lower(question_content) LIKE '%sell to me at%'
            THEN 'Payments / Transactions / Proposed Sales'

            --------------------------------------------------------
            -- 7. INSURANCE / RISK / COMPENSATION (CLEANED)
            -- ONLY insurance, insure, compensation
            --------------------------------------------------------
            WHEN lower(question_content) LIKE '%insurance%'
              OR lower(question_content) LIKE '%insure%'
              OR lower(question_content) LIKE '%compensation%'
            THEN 'Insurance / Risk / Compensation'

            --------------------------------------------------------
            -- 8. GENERAL FINANCIAL CHALLENGE
            -- hardship, lack of money/funds, expensive, poverty
            --------------------------------------------------------
            WHEN lower(question_content) LIKE '%no money%'
              OR lower(question_content) LIKE '%lack of money%'
              OR lower(question_content) LIKE '%lack money%'
              OR lower(question_content) LIKE '%lacking money%'
              OR lower(question_content) LIKE '%financial problem%'
              OR lower(question_content) LIKE '%financial challenge%'
              OR lower(question_content) LIKE '%financial issue%'
              OR lower(question_content) LIKE '%no funds%'
              OR lower(question_content) LIKE '%lack of funds%'
              OR lower(question_content) LIKE '%need money%'
              OR lower(question_content) LIKE '%need funds%'
              OR lower(question_content) LIKE '%capital problem%'
              OR lower(question_content) LIKE '%no capital%'
              OR lower(question_content) LIKE '%cannot afford%'
              OR lower(question_content) LIKE '%cant afford%'
              OR lower(question_content) LIKE '%afford to%'
              OR lower(question_content) LIKE '%too expensive%'
              OR lower(question_content) LIKE '%very expensive%'
              OR lower(question_content) LIKE '%things are expensive%'
              OR lower(question_content) LIKE '%everything is expensive%'
              OR lower(question_content) LIKE '%costly%'
              OR lower(question_content) LIKE '%povert%'
                            -- poor but not explicitly "no money"
              OR lower(question_content) LIKE '%am poor%'
              OR lower(question_content) LIKE '%i am poor%'

              -- wefarm money / prize / champion / win money
              OR (lower(question_content) LIKE '%wefarm%'
                  AND lower(question_content) LIKE '%money%')
              OR lower(question_content) LIKE '%win this money%'
              OR lower(question_content) LIKE '%win that money%'
              OR lower(question_content) LIKE '%win money%'
              OR lower(question_content) LIKE '%want to win some money%'
              OR lower(question_content) LIKE '%how can i win this money%'
              OR lower(question_content) LIKE '%how can i win that money%'
              OR lower(question_content) LIKE '%qualify to get the money%'
              OR lower(question_content) LIKE '%who won the money%'
              or (lower(question_content)  LIKE '%help%' and lower(question_content)  LIKE '%money%') --general financial challenge
or (lower(question_content)  LIKE '%dont have%' and lower(question_content)  LIKE '%money%')--General Financial Challenge
or (lower(question_content)  LIKE '%money%' and lower(question_content)  LIKE '%send%')
or (lower(question_content)  LIKE '%money%' and lower(question_content)  LIKE '%raise%')

or regexp_matches(lower(question_content),
                '(no money|dont have money|don''t have money|have no money|lack money|lacking money|no capital)')
            OR regexp_matches(lower(question_content),
                '(no funds|lack of funds)')
            OR regexp_matches(lower(question_content),
                '(financial problem|financial challenge|financial issue)')
            OR regexp_matches(lower(question_content),
                '(cant afford|can''t afford|cannot afford|afford to)')
            OR regexp_matches(lower(question_content),
                '(too expensive|very expensive|so expensive|things are expensive|everything is expensive|costly)')
                
                 or (lower(question_content)  LIKE '%funds%' and lower(question_content)  LIKE '%lack%')
                or (lower(question_content)  LIKE '%funds%' and lower(question_content)  LIKE '%don%')
            THEN 'General Financial Challenge'

            ELSE NULL
        END AS financial_subcategory,

        ------------------------------------------------------------
        -- MATCHED KEYWORD (CLEANED; NO agent, NO ajo)
        ------------------------------------------------------------
       UPDATE questions_financial_tagged_2
SET matched_keyword =
    CASE
        ------------------------------------------------------------
        -- CREDIT / LOANS SUBTHEMES
        ------------------------------------------------------------
        WHEN lower(question_content) LIKE '%loan from sacco%'
          OR lower(question_content) LIKE '%sacco loan%'
          OR (lower(question_content) LIKE '%sacco%' AND lower(question_content) LIKE '%loan%')
        THEN 'credit_sacco_loan'

        
        WHEN (lower(question_content) LIKE '%how much money%'
              AND lower(question_content) LIKE '%start%')
        THEN 'credit_startup_money'

        WHEN (lower(question_content) LIKE '%minimum money%'
              AND lower(question_content) LIKE '%start%')
        THEN 'credit_startup_money'

        WHEN (lower(question_content) LIKE '%amount of money%'
              AND lower(question_content) LIKE '%start%')
        THEN 'credit_startup_money'

        WHEN (lower(question_content) LIKE '%need money%'
              AND lower(question_content) LIKE '%investment%')
          OR (lower(question_content) LIKE '%need some money%'
              AND lower(question_content) LIKE '%investment%')
          OR (lower(question_content) LIKE '%need funds%'
              AND lower(question_content) LIKE '%investment%')
        THEN 'credit_need_funds_investment'

        WHEN lower(question_content) LIKE '%lend me some money%'
          OR lower(question_content) LIKE '%lend me money%'
          OR lower(question_content) LIKE '%can you lend me%'
          OR lower(question_content) LIKE '%can u lend me%'
          or (lower(question_content)  LIKE '%lend%' and lower(question_content)  LIKE '%money%')--credit/loans

        THEN 'credit_lend_me_money'

        WHEN lower(question_content) LIKE '%capital needed%'
          OR lower(question_content) LIKE '%capital%'
          OR lower(question_content) LIKE '%capital required%'
          OR lower(question_content) LIKE '%how much capital%'
          OR lower(question_content) LIKE '%capital to start%'
          OR lower(question_content) LIKE '%starting capital%'
          OR lower(question_content) LIKE '%start up capital%'
          OR lower(question_content) LIKE '%startup capital%'
          OR lower(question_content) LIKE '%working capital%'
        THEN 'credit_startup_capital'
        
		WHEN lower(question_content) LIKE '%need money%'
          AND lower(question_content) LIKE '%investment%'
        THEN 'credit_need_funds_capital'

        WHEN lower(question_content) LIKE '%need some money%'
          AND lower(question_content) LIKE '%investment%'
        THEN 'credit_need_funds_capital'

        WHEN lower(question_content) LIKE '%need funds%'
          AND lower(question_content) LIKE '%investment%'
        THEN 'credit_need_funds_capital'

        WHEN (lower(question_content) LIKE '%commercial bank%'
              OR lower(question_content) LIKE '%commercial banks%'
              OR lower(question_content) LIKE '%bank%')
             AND lower(question_content) LIKE '%investment%'
        THEN 'credit_banks_investment'

        WHEN lower(question_content) LIKE '%soft loan%'
          OR lower(question_content) LIKE '%loan%'
          OR lower(question_content) LIKE '%loans%'
          OR lower(question_content) LIKE '%credit%'
          OR lower(question_content) LIKE '%microfinance%'
          OR lower(question_content) LIKE '%micro finance%'
          OR lower(question_content) LIKE '%money lending%'
          OR lower(question_content) LIKE '%lender%'
          OR lower(question_content) LIKE '%lending%'
          OR lower(question_content) LIKE '%borrow%'
          OR lower(question_content) LIKE '%borrowing%'
          OR lower(question_content) LIKE '%installment%'
          OR lower(question_content) LIKE '%instalment%'
          OR lower(question_content) LIKE '%pay back%'
        THEN 'credit_general_loan'

        WHEN lower(question_content) LIKE '%collateral%'
          OR lower(question_content) LIKE '%guarantor%'
          OR lower(question_content) LIKE '%guarantee%'
        THEN 'credit_collateral_guarantor'

        WHEN lower(question_content) LIKE '%need funds%'
          OR lower(question_content) LIKE '%need capital%'
          OR lower(question_content) LIKE '%get funds%'
          OR lower(question_content) LIKE '%get capital%'
        THEN 'credit_need_funds_capital'

        ------------------------------------------------------------
        -- SAVINGS / GROUPS SUBTHEMES
        ------------------------------------------------------------
        WHEN lower(question_content) LIKE '%vsla%'
          OR lower(question_content) LIKE '%vsl%'
          OR lower(question_content) LIKE '%village savings%'
          OR lower(question_content) LIKE '%sacco group%'
          OR (lower(question_content) LIKE '%sacco%' )
        THEN 'savings_group_vsla_sacco'

        WHEN lower(question_content) LIKE '%rosca%'
          OR lower(question_content) LIKE '%chama%'
          OR lower(question_content) LIKE '%tontine%'
          OR lower(question_content) LIKE '%esusu%'
          OR lower(question_content) LIKE '%merry-go-round%'
          OR lower(question_content) LIKE '%merry go round%'
        THEN 'savings_rotating_group'

        WHEN lower(question_content) LIKE '%saving%'
          OR lower(question_content) LIKE '%savings%'
          OR lower(question_content) LIKE '%save money%'
          OR lower(question_content) LIKE '%bank account%'
          OR lower(question_content) LIKE '%fixed deposit%'
        THEN 'savings_personal_saving'

        WHEN lower(question_content) LIKE '%share capital%'
        THEN 'savings_share_capital'

        WHEN lower(question_content) LIKE '%member contribution%'
          OR lower(question_content) LIKE '%contribution%'
        THEN 'savings_group_contribution'

        ------------------------------------------------------------
        -- MARKET PRICE SUBTHEMES
        ------------------------------------------------------------
        WHEN lower(question_content) LIKE '%market price%'
          OR lower(question_content) LIKE '%current price%'
          OR lower(question_content) LIKE '%selling price%'
          OR lower(question_content) LIKE '%buying price%'
          OR lower(question_content) LIKE '%market rate%'
          OR lower(question_content) LIKE '%rate per%'
          OR lower(question_content) LIKE '%what is the price%'
          OR lower(question_content) LIKE '%how much%'
          OR lower(question_content) LIKE '%price%'
          OR lower(question_content) LIKE '%prices%'
           or  (lower(question_content)  LIKE '%money%' and lower(question_content)  LIKE '%kg%')
            or (lower(question_content)  LIKE '%money%' and lower(question_content)  LIKE '%kilogram%')
               or (lower(question_content)  LIKE '%much%' and lower(question_content)  LIKE '%money%')--market prices
            or (lower(question_content)  LIKE '%sell%' and lower(question_content)  LIKE '%much%') --market prices
        THEN 'prices_price_discovery'

        WHEN lower(question_content) LIKE '%where can i sell%'
          OR lower(question_content) LIKE '%market for%'
        THEN 'prices_market_access'

        WHEN lower(question_content) LIKE '%quotation%'
          OR lower(question_content) LIKE '%quote%'
          OR lower(question_content) LIKE '%wholesale%'
          OR lower(question_content) LIKE '%retail%'
        THEN 'prices_trade_terms'

        WHEN lower(question_content) LIKE '%cost%'
          OR lower(question_content) LIKE '%costing%'
        THEN 'prices_cost_as_price'

        ------------------------------------------------------------
        -- PROFITABILITY / ECONOMICS SUBTHEMES
        ------------------------------------------------------------
        WHEN lower(question_content) LIKE '%more profitable%'
          OR lower(question_content) LIKE '%profitable%'
          OR lower(question_content) LIKE '%profit margin%'
          OR lower(question_content) LIKE '%profit%'
          OR lower(question_content) LIKE '%returns%'
          OR lower(question_content) LIKE '%break even%'
        THEN 'profitability_profit_returns'

        WHEN lower(question_content) LIKE '%gross margin%'
          OR lower(question_content) LIKE '%gross margins%'
          OR (lower(question_content) LIKE '%cross%' AND lower(question_content) LIKE '%margin%')
          OR (lower(question_content) LIKE '%gross%' AND lower(question_content) LIKE '%margin%')
        THEN 'profitability_gross_margin'

        WHEN lower(question_content) LIKE '%what business can i do%'
          OR lower(question_content) LIKE '%which business can i do%'
          OR lower(question_content) LIKE '%which business is best%'
          OR lower(question_content) LIKE '%best business%'
          OR lower(question_content) LIKE '%good business%'
          OR lower(question_content) LIKE '%good money%'
          OR lower(question_content) LIKE '%gives money%'
        THEN 'profitability_business_choice'
        
                WHEN (lower(question_content) LIKE '%which crop%'
              AND lower(question_content) LIKE '%money%')
          OR (lower(question_content) LIKE '%what crop%'
              AND lower(question_content) LIKE '%money%')
          OR (lower(question_content) LIKE '%which plant%'
              AND lower(question_content) LIKE '%money%')
          OR (lower(question_content) LIKE '%what plant%'
              AND lower(question_content) LIKE '%money%')
          OR (lower(question_content) LIKE '%which business%'
              AND lower(question_content) LIKE '%money%')
          OR (lower(question_content) LIKE '%what business%'
              AND lower(question_content) LIKE '%money%')
          OR (lower(question_content) LIKE '%which animal%'
              AND lower(question_content) LIKE '%money%')
          OR (lower(question_content) LIKE '%which project%'
              AND lower(question_content) LIKE '%money%')
        THEN 'profitability_money_option_choice'

        WHEN (lower(question_content) LIKE '%get money%'
              AND (lower(question_content) LIKE '%from %'
                   OR lower(question_content) LIKE '%through %'))
          OR lower(question_content) LIKE '%earn money%'
          OR lower(question_content) LIKE '%harvest money%'
          OR lower(question_content) LIKE '%fetch money%'
        THEN 'profitability_money_from_farming'

        WHEN lower(question_content) LIKE '%money quickly%'
          OR lower(question_content) LIKE '%money quick%'
          OR lower(question_content) LIKE '%money in short time%'
        THEN 'profitability_quick_money'

        WHEN (lower(question_content) LIKE '%how much money%'
              AND lower(question_content) LIKE '%get%')
          OR (lower(question_content) LIKE '%how much money%'
              AND lower(question_content) LIKE '%from%')
        THEN 'profitability_how_much_money_return'

        WHEN (lower(question_content) LIKE '%cash crop%'
              AND lower(question_content) LIKE '%money%')
        THEN 'profitability_cash_crop_money'


        WHEN lower(question_content) LIKE '%make money%'
          OR lower(question_content) LIKE '%money fast%'
          OR lower(question_content) LIKE '%quick money%'
          OR lower(question_content) LIKE '%viable business%'
          or regexp_matches(lower(question_content),
                '(make money|make more money|get money in one year|get money fast|money fast|quick money|viable business)')
        THEN 'profitability_make_money_fast'

        WHEN lower(question_content) LIKE '%cheap to start%'
          OR lower(question_content) LIKE '%cheapest farming%'
          OR lower(question_content) LIKE '%cheapest system%'
          OR lower(question_content) LIKE '%cheap start%'
          OR lower(question_content) LIKE '%cheap produce%'
          OR lower(question_content) LIKE '%cheap between%'
          OR lower(question_content) LIKE '%low capital business%'
          OR lower(question_content) LIKE '%small capital business%'
          OR lower(question_content) LIKE '%low cost business%'
          OR lower(question_content) LIKE '%small money business%'
               or regexp_matches(lower(question_content),
                '(cheap to start|cheapest farming|cheapest system|cheap start|cheap produce|cheap between|low capital business|small capital business|low cost business|small money business)')
            OR (
                regexp_matches(lower(question_content),
                    '(cheap|cheapest|low cost|low capital|small capital|little money|small investment|low investment)')
                AND regexp_matches(lower(question_content),
                    '(business|system|method|rearing|venture|enterprise|project|farm|farming|poultry|broiler|layer)')
                AND NOT regexp_matches(lower(question_content),
                    '(manure|fertilizer|fertiliser|seed|feed|chemical|spray|pesticide|herbicide|drug)')
            )
            or (lower(question_content)  LIKE '%type%' and lower(question_content)  LIKE '%cheap%') --profitability
        THEN 'profitability_cheapest_option'

        WHEN lower(question_content) LIKE '%cost of production%'
          OR lower(question_content) LIKE '%production cost%'
          OR lower(question_content) LIKE '%reduce costs%'
          OR lower(question_content) LIKE '%reduce cost%'
          OR lower(question_content) LIKE '%cut costs%'
          OR lower(question_content) LIKE '%lower costs%'
        THEN 'profitability_cost_structure'

        WHEN lower(question_content) LIKE '%invest in%'
          OR lower(question_content) LIKE '%investment in%'
          OR lower(question_content) LIKE '%good investment%'
        THEN 'profitability_investment_evaluation'

        WHEN lower(question_content) LIKE '%pay me well%'
          OR lower(question_content) LIKE '%pay me back well%'
          OR lower(question_content) LIKE '%pay me overwhelmingly%'
          OR lower(question_content) LIKE '%pay me faster%'
                 or (lower(question_content)  LIKE '%best%' and lower(question_content)  LIKE '%money%') --profitability

        THEN 'profitability_pay_me_well'

        WHEN lower(question_content) LIKE '%minimum investment%'
          OR lower(question_content) LIKE '%investment required%'
           or  (lower(question_content)  LIKE '%money%' and lower(question_content)  LIKE '%start%')
            or (lower(question_content)  LIKE '%money%' and lower(question_content)  LIKE '%type%')
              or (lower(question_content)  LIKE '%get%' and lower(question_content)  LIKE '%money%') --profitability
                         or (lower(question_content)  LIKE '%grow%' and lower(question_content)  LIKE '%money%') 
                         or (lower(question_content)  LIKE '%between%' and lower(question_content)  LIKE '%money%')
                         or (lower(question_content)  LIKE '%bring%' and lower(question_content)  LIKE '%money%')
                         or (lower(question_content)  LIKE '%fetch%' and lower(question_content)  LIKE '%money%')
 or (lower(question_content)  LIKE '%earn%' and lower(question_content)  LIKE '%money%')
        THEN 'profitability_investment_evaluation'

        WHEN lower(question_content) LIKE '%good for investment%'
          OR lower(question_content) LIKE '%suitable investment%'
          OR lower(question_content) LIKE '%which agriculture investment%'
          OR lower(question_content) LIKE '%what investment%'
        THEN 'profitability_business_choice'

        WHEN lower(question_content) LIKE '%investments in farming%'
          OR lower(question_content) LIKE '%investment in farming%'
          OR lower(question_content) LIKE '%investment in agriculture%'
          OR lower(question_content) LIKE '%agriculture investment%'
          OR lower(question_content) LIKE '%investment%'
           OR lower(question_content) LIKE '%investing%'
        THEN 'profitability_investment_evaluation'

        WHEN lower(question_content) LIKE '%why is agric called an investment%'
        THEN 'profitability_investment_concept'

        WHEN lower(question_content) LIKE '%asset or investment%'
        THEN 'profitability_asset_vs_investment'
        
       
        ------------------------------------------------------------
        -- GRANTS / SUBSIDIES / SUPPORT SUBTHEMES
        ------------------------------------------------------------
        WHEN (lower(question_content) LIKE '%grant%' AND lower(question_content) LIKE '%farm%')
              OR (lower(question_content) LIKE '%grants%' AND lower(question_content) LIKE '%farm%')
          OR lower(question_content) LIKE '%funding%'
          OR lower(question_content) LIKE '%government funding%'
        THEN 'support_grants_funding'

        WHEN lower(question_content) LIKE '%subsidy%'
          OR lower(question_content) LIKE '%subsidies%'
          OR lower(question_content) LIKE '%input subsidy%'
          OR lower(question_content) LIKE '%fertilizer subsidy%'
        THEN 'support_subsidy_inputs'

        WHEN lower(question_content) LIKE '%cash transfer%'
        	OR lower(question_content) LIKE '%financial assistance%'
        THEN 'support_cash_transfer'

        WHEN lower(question_content) LIKE '%voucher%'
          OR lower(question_content) LIKE '%redeem voucher%'
        THEN 'support_voucher'

        WHEN lower(question_content) LIKE '%support program%'
          OR lower(question_content) LIKE '%support scheme%'
          OR lower(question_content) LIKE '%financial support%'
          OR lower(question_content) LIKE '%empowerment program%'
          OR lower(question_content) LIKE '%youth program%'
          OR lower(question_content) LIKE '%women program%'
        THEN 'support_programs'

        ------------------------------------------------------------
        -- PAYMENTS / TRANSACTIONS SUBTHEMES
        ------------------------------------------------------------
        WHEN lower(question_content) LIKE '%cash out%'
          OR lower(question_content) LIKE '%cashout%'
        THEN 'payment_cash_out'

        WHEN lower(question_content) LIKE '%payment%'
          OR lower(question_content) LIKE '%payments%'
          OR lower(question_content) LIKE '%pay for%'
          OR lower(question_content) LIKE '%pay me%'
        THEN 'payment_payment_language'

        WHEN lower(question_content) LIKE '%transaction%'
        THEN 'payment_transaction'

        WHEN lower(question_content) LIKE '%proposed sale%'
          OR lower(question_content) LIKE '%sale agreement%'
          OR lower(question_content) LIKE '%sell it to me at%'
          OR lower(question_content) LIKE '%sell to me at%'
        THEN 'payment_proposed_sale'

        ------------------------------------------------------------
        -- INSURANCE SUBTHEMES
        ------------------------------------------------------------
        WHEN lower(question_content) LIKE '%insurance%'
        	OR lower(question_content) LIKE '%insure%'
        THEN 'insurance_insurance'

        WHEN lower(question_content) LIKE '%compensation%'
        THEN 'insurance_compensation'

        ------------------------------------------------------------
        -- GENERAL FINANCIAL CHALLENGE SUBTHEMES
        ------------------------------------------------------------
        WHEN lower(question_content) LIKE '%no money%'
          OR lower(question_content) LIKE '%lack of money%'
          OR lower(question_content) LIKE '%lack money%'
          OR lower(question_content) LIKE '%lacking money%'
          OR lower(question_content) LIKE '%no funds%'
          OR lower(question_content) LIKE '%lack of funds%'
        THEN 'hardship_no_funds'

        WHEN lower(question_content) LIKE '%financial problem%'
          OR lower(question_content) LIKE '%financial challenge%'
          OR lower(question_content) LIKE '%financial issue%'
        THEN 'hardship_financial_problem'

        WHEN lower(question_content) LIKE '%need money%'
          OR lower(question_content) LIKE '%need funds%'
       or (lower(question_content)  LIKE '%help%' and lower(question_content)  LIKE '%money%') --general financial challenge
or (lower(question_content)  LIKE '%dont have%' and lower(question_content)  LIKE '%money%')--General Financial Challenge
or (lower(question_content)  LIKE '%money%' and lower(question_content)  LIKE '%send%')
or (lower(question_content)  LIKE '%money%' and lower(question_content)  LIKE '%raise%')
        THEN 'hardship_need_money'

        WHEN lower(question_content) LIKE '%capital problem%'
          OR lower(question_content) LIKE '%no capital%'
        THEN 'hardship_capital_problem'

        WHEN lower(question_content) LIKE '%cannot afford%'
          OR lower(question_content) LIKE '%cant afford%'
          OR lower(question_content) LIKE '%afford to%'
        THEN 'hardship_cannot_afford'

        WHEN lower(question_content) LIKE '%too expensive%'
          OR lower(question_content) LIKE '%very expensive%'
          OR lower(question_content) LIKE '%things are expensive%'
          OR lower(question_content) LIKE '%everything is expensive%'
          OR lower(question_content) LIKE '%costly%'
        THEN 'hardship_too_expensive'

        WHEN lower(question_content) LIKE '%am poor%'
          OR lower(question_content) LIKE '%i am poor%'
        THEN 'hardship_poor'

        WHEN (lower(question_content) LIKE '%wefarm%'
              AND lower(question_content) LIKE '%money%')
          OR lower(question_content) LIKE '%win this money%'
          OR lower(question_content) LIKE '%win that money%'
          OR lower(question_content) LIKE '%win money%'
          OR lower(question_content) LIKE '%want to win some money%'
          OR lower(question_content) LIKE '%qualify to get the money%'
          OR lower(question_content) LIKE '%who won the money%'
        THEN 'hardship_wefarm_reward_money'

        WHEN lower(question_content) LIKE '%povert%'
        THEN 'hardship_poverty'

        
            WHEN regexp_matches(lower(question_content),
                '(no money|dont have money|don''t have money|have no money|lack money|lacking money|no capital)')
            OR regexp_matches(lower(question_content),
                '(no funds|lack of funds)')
            OR regexp_matches(lower(question_content),
                '(financial problem|financial challenge|financial issue)')
                or (lower(question_content)  LIKE '%funds%' and lower(question_content)  LIKE '%lack%')
                or (lower(question_content)  LIKE '%funds%' and lower(question_content)  LIKE '%don%')
        THEN 'hardship_no_funds'

        WHEN regexp_matches(lower(question_content),
                '(cant afford|can''t afford|cannot afford|afford to)')
        THEN 'hardship_cannot_afford'

        WHEN regexp_matches(lower(question_content),
                '(too expensive|very expensive|so expensive|things are expensive|everything is expensive|costly)')
        THEN 'hardship_too_expensive'
        ------------------------------------------------------------
        -- FALLBACK: KEEP EXISTING matched_keyword IF YOU WANT,
        -- OR NULL OUT IF YOU WANT ONLY SUBTHEMES
        ------------------------------------------------------------
        ELSE NULL
    END;

        END AS matched_keyword

    FROM my_table_tagged_chunked AS q
) AS t;
