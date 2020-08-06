-- A record of all wake words in use by devices running Mycroft Core and paired to Selene.
-- It will also contain wake words curated using Selene and Precise for third parties.
CREATE TABLE wake_word.wake_word (
    id              uuid                    PRIMARY KEY DEFAULT gen_random_uuid(),
    setting_name    text                    NOT NULL,
    display_name    text                    NOT NULL,
    account_id      uuid                    REFERENCES account.account ON DELETE CASCADE,
    engine          wake_word_engine_enum   NOT NULL,
    insert_ts       TIMESTAMP               NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (account_id, setting_name)
);
