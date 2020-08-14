-- Contains references to samples submitted by users for use in Precise model training.
-- The classification columns will be null until classification is complete, at which point
-- they will be populated with the matching values on the classification table.
CREATE TABLE wake_word.sample (
    id              uuid                PRIMARY KEY DEFAULT gen_random_uuid(),
    wake_word_id    uuid                NOT NULL REFERENCES wake_word.wake_word ON DELETE CASCADE,
    account_id      uuid                REFERENCES account.account ON DELETE CASCADE,
    audio_file_name text                NOT NULL,
    audio_file_date date                NOT NULL DEFAULT CURRENT_DATE,
    directory_group INTEGER,
    insert_ts       TIMESTAMP           NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (account_id, audio_file_name)
);
