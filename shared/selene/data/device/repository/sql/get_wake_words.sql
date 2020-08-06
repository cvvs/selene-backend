SELECT
    id,
    setting_name,
    display_name,
    engine,
    account_id IS NOT NULL AS user_defined
FROM
    wake_word.wake_word
WHERE
    account_id IS NULL
    OR account_id = %(account_id)s
