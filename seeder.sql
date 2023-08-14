CREATE TABLE article
(
    id INTEGER NOT NULL
        CONSTRAINT a_pk PRIMARY KEY,
    name VARCHAR(512) NOT NULL
);

CREATE TABLE ref
(
    id INTEGER NOT NULL
        CONSTRAINT a_pk PRIMARY KEY AUTOINCREMENT,
    parent_article_id INTEGER NOT NULL
        CONSTRAINT a_fk REFERENCES article(parent_article_id),
    article_id INTEGER NOT NULL
        CONSTRAINT a_fk REFERENCES article(article_id)
);