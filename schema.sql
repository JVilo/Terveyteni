CREATE TABLE IF NOT EXISTS users (
        id SERIAL NOT NULL,
        name VARCHAR,
        password VARCHAR,
        role INTEGER,
        PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS activ_bmi (
        id SERIAL NOT NULL,
        activ INTEGER,
        PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS messages (
        id SERIAL NOT NULL,
        title VARCHAR,
        content VARCHAR,
        user_id INTEGER NOT NULL,
        sent_at TIMESTAMP WITHOUT TIME ZONE,
        visible INTEGER,
        ref_key INTEGER,
        PRIMARY KEY (id),
        FOREIGN KEY(user_id) REFERENCES users (id),
        FOREIGN KEY(ref_key) REFERENCES messages (id)
);

--BEGIN;
-- ALTER TABLE private_messages DROP CONSTRAINT private_messages_sender_id_fkey;
-- ALTER TABLE private_messages DROP COLUMN sender_id;
-- ALTER TABLE private_messages ADD user_id INTEGER REFERENCES users;
------ ALTER TABLE private_messages ADD doctor_id INTEGER REFERENCES users;
----  ALTER TABLE private_messages ADD sender_id INTEGER REFERENCES users;
-- commit;
--END;

CREATE TABLE IF NOT EXISTS private_messages (
        id SERIAL NOT NULL,
        title VARCHAR,
        content VARCHAR,
        user_id INTEGER NOT NULL,
        doctor_id INTEGER,
        patient_id INTEGER,
        sent_at TIMESTAMP WITHOUT TIME ZONE,
        visible INTEGER,
        ref_key INTEGER,
        PRIMARY KEY (id),
        FOREIGN KEY(user_id) references users (id),
        FOREIGN KEY(doctor_id) references users (id),
        FOREIGN KEY(patient_id) REFERENCES users (id),
        FOREIGN KEY(ref_key) REFERENCES private_messages (id)
);

CREATE TABLE IF NOT EXISTS bmi (
        id SERIAL NOT NULL,
        weight INTEGER,
        height INTEGER,
        user_id INTEGER NOT NULL,
        active INTEGER,
        PRIMARY KEY (id),
        FOREIGN KEY(user_id) REFERENCES users (id)
);