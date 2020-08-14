SELECT
    wake_word_id,
    account_id,
    audio_file_name,
    directory_group,
    is_wake_word,
    failed_attempts,
    pitch
FROM
    wake_word.sample
WHERE
    account_id = %(account_id)s
