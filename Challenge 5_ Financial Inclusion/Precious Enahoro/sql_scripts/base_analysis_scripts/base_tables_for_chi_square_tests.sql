---️Country × Condensed Theme (for chi-square by theme & country)
SELECT
    question_user_country_code AS country,
    financial_theme_condensed,
    COUNT(*) AS n_questions
FROM questions_deduped
WHERE financial_theme_condensed IS NOT NULL
group by 1,2

--Country × Financial vs Non-Financial (for the big “are some countries more financial?” chi-square)
SELECT
    question_user_country_code AS country,
    financial_flag_clean,
    COUNT(*) AS n_questions
FROM questions_deduped
GROUP BY 1, 2;

---Month × Theme (can add country if you want country-level time series later)
--SELECT -- question_user_country_code AS country,
select date_part('month', question_sent::date) as mo, 
    financial_theme_condensed,
    COUNT(*) AS n_questions
FROM questions_deduped

GROUP BY 1, 2
ORDER BY 1, 2
