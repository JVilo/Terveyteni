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

CREATE TABLE IF NOT EXISTS "RR_tasks" (
        id SERIAL NOT NULL,
        "RRm1_sys" INTEGER,
        "RRm1_dia" INTEGER,
        "RRm2_sys" INTEGER,
        "RRm2_dia" INTEGER,
        "RRmed1_sys" INTEGER,
        "RRmed1_dia" INTEGER,
        "RRmed2_sys" INTEGER,
        "RRmed2_dia" INTEGER,
        "RRe1_sys" INTEGER,
        "RRe1_dia" INTEGER,
        "RRe2_sys" INTEGER,
        "RRe2_dia" INTEGER,
        "RRemed1_sys" INTEGER,
        "RRemed1_dia" INTEGER,
        "RRemed2_sys" INTEGER,
        "RRemed2_dia" INTEGER,
        user_id INTEGER NOT NULL,
        active INTEGER,
        PRIMARY KEY (id),
        FOREIGN KEY(user_id) REFERENCES users (id)
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