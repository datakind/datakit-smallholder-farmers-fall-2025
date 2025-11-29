--Use this file to see some ideas of how I cleaned up the data even more! The aim was to fill in the country codes and question_sent columns as much as possible.

ALTER TABLE questions_deduped
ADD COLUMN temp_swap VARCHAR;

-- 2. Save the original country_code into temp
UPDATE questions_deduped
SET temp_swap = question_user_country_code
WHERE question_user_created_at = 'ke';

-- 3. Move created_at → country_code
UPDATE  questions_deduped
SET question_user_country_code = question_user_created_at
WHERE question_user_created_at = 'ke';

-- 4. Move temp (original country_code) → created_at
UPDATE  questions_deduped
SET question_user_created_at = temp_swap
WHERE temp_swap IS NOT NULL;

-- 5. Remove temp column
ALTER TABLE  questions_deduped
DROP COLUMN temp_swap;


--using gender and dob columns to update created_at; WHERE question_user_created_at in ('farmer', 'male', 'live')
UPDATE questions_deduped
SET question_user_created_at = question_user_gender
WHERE question_user_created_at in ('farmer', 'male', 'live')
--lower(question_user_country_code) NOT IN ('ke', 'tz', 'ug', 'gb', 'swa')
  --AND question_user_gender IS NOT NULL;

UPDATE questions_deduped
SET question_user_country_code = question_user_status
WHERE question_user_status IN ('ke', 'tz', 'ug', 'gb', 'swa')

UPDATE questions_deduped
SET question_sent = question_user_created_at
WHERE question_sent is null


UPDATE questions_deduped
SET question_sent = question_user_status
WHERE TRY_CAST(question_sent AS DATE) IS NULL
      AND question_sent IS NOT NULL
      AND question_sent <> ''
      
UPDATE questions_deduped
SET question_sent = question_user_gender
WHERE TRY_CAST(question_sent AS DATE) IS NULL
      AND question_sent IS NOT NULL
      AND question_sent <> ''

UPDATE questions_deduped
SET question_sent = question_user_dob
WHERE TRY_CAST(question_sent AS DATE) IS NULL
      AND question_sent IS NOT NULL
      AND question_sent <> ''
--WHERE lower(question_user_country_code) NOT IN ('ke', 'tz', 'ug', 'gb', 'swa')
      
UPDATE questions_deduped
SET question_sent = question_user_created_at
WHERE TRY_CAST(question_sent AS DATE) IS NULL
      AND question_sent IS NOT NULL
      AND question_sent <> ''
      
UPDATE questions_deduped
SET question_sent = null
where year(question_sent::date) < 2016

UPDATE questions_deduped
SET question_sent = question_topic
WHERE TRY_CAST(question_topic AS DATE) IS not NULL and question_sent is null
