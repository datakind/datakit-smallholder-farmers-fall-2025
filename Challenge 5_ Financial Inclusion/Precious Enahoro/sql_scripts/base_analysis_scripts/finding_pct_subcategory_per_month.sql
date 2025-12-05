WITH monthly AS (
    SELECT
        financial_subcategory,
        date_part('month', question_sent::date) AS month,
        COUNT(*) AS n
    FROM questions_deduped
    WHERE financial_subcategory IS NOT NULL
    GROUP BY 1, 2
),

totals AS (
    SELECT
        financial_subcategory,
        SUM(n) AS total_n
    FROM monthly
    GROUP BY 1
)

SELECT
    m.financial_subcategory,
    m.month,
    m.n,
    t.total_n,
    (m.n * 1.0 / t.total_n) * 100 AS pct_of_subcategory
FROM monthly m
JOIN totals t USING (financial_subcategory)
ORDER BY financial_subcategory, month;
