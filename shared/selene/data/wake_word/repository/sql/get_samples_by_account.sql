SELECT
    ww.setting_name as wake_word,
    s.account_id,
    s.audio_file_name,
    s.audio_file_date,
    s.directory_group
FROM
    wake_word.sample s
    INNER JOIN wake_word.wake_word ww ON ww.id = s.wake_word_id
WHERE
    s.account_id = %(account_id)s
