-- Table: tasks
DROP TABLE IF EXISTS tasks CASCADE;
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    status_id INTEGER,
    user_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- автоматично буде вказана поточна дата при створенні нових задач (для поточних сгенерую рандомні дати)
    FOREIGN KEY (status_id) REFERENCES status (id)
      ON DELETE SET NULL -- при видаленні статусу, залишаю null, щоб задачі не зникали
      ON UPDATE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users (id)
      ON DELETE CASCADE
      ON UPDATE CASCADE
);

-- Table: status
DROP TABLE IF EXISTS status CASCADE;
CREATE TABLE status (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL CHECK (name IN ('new', 'in progress', 'completed'))
);

-- Table: users
DROP TABLE IF EXISTS users CASCADE;
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    fullname VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);