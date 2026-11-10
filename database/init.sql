CREATE TABLE IF NOT EXISTS prediction_history (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    predicted_genre VARCHAR(50) NOT NULL,
    confidence FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);