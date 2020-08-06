-- Wake word classifier indicating if the audio in a wake word sample is a
-- correctly recognized wake word.  The “almost” value indicates a word or
-- words similar to the wake word triggered the recognizer.  For example,
-- “Hey Minecraft” triggered a “Hey Mycroft” wake word.
CREATE TYPE is_wake_word_enum AS ENUM ('yes', 'no', 'almost');
