--Deduping questions with multiple answers to reduce the size of the dataset since we are only focusing on the questions asked for this analysis

CREATE TABLE questions_deduped AS
SELECT *
FROM (
    SELECT
        q.*,

        -- completeness score: higher = more complete
        (
            CASE WHEN question_content IS NOT NULL AND question_content <> '' THEN 1 ELSE 0 END +
            CASE WHEN question_topic IS NOT NULL AND question_topic <> '' THEN 1 ELSE 0 END +
            CASE WHEN question_user_country_code IS NOT NULL AND question_user_country_code <> '' THEN 1 ELSE 0 END +
            CASE WHEN financial_subcategory IS NOT NULL AND financial_subcategory <> '' THEN 1 ELSE 0 END +
            CASE WHEN matched_keyword IS NOT NULL AND matched_keyword <> '' THEN 1 ELSE 0 END
        ) AS completeness_score,

        ROW_NUMBER() OVER (
            PARTITION BY question_id
            ORDER BY
                -- 1) most complete row
                (
                    CASE WHEN question_content IS NOT NULL AND question_content <> '' THEN 1 ELSE 0 END +
                    CASE WHEN question_topic IS NOT NULL AND question_topic <> '' THEN 1 ELSE 0 END +
                    CASE WHEN question_user_country_code IS NOT NULL AND question_user_country_code <> '' THEN 1 ELSE 0 END +
                    CASE WHEN financial_subcategory IS NOT NULL AND financial_subcategory <> '' THEN 1 ELSE 0 END +
                    CASE WHEN matched_keyword IS NOT NULL AND matched_keyword <> '' THEN 1 ELSE 0 END
                ) DESC,
                -- 2) tiebreaker: keep the row with highest org_idx (you can change this)
                org_idx DESC
        ) AS rn

    FROM questions_financial_tagged_2 AS q
) t
WHERE rn = 1;
