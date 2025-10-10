-- Migration: Création de la table ai_answers
-- Cette table stocke toutes les interactions avec l'assistant SQL AI

CREATE TABLE IF NOT EXISTS ai_answers (
    id SERIAL PRIMARY KEY,
    question TEXT NOT NULL,
    sql TEXT NOT NULL,
    reponse JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index pour améliorer les performances de recherche
CREATE INDEX IF NOT EXISTS idx_ai_answers_created_at ON ai_answers(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_ai_answers_question ON ai_answers USING gin(to_tsvector('french', question));

-- Commentaires sur les colonnes
COMMENT ON TABLE ai_answers IS 'Historique des questions posées à l''assistant SQL AI';
COMMENT ON COLUMN ai_answers.id IS 'Identifiant unique auto-incrémenté';
COMMENT ON COLUMN ai_answers.question IS 'Question posée par l''utilisateur en langage naturel';
COMMENT ON COLUMN ai_answers.sql IS 'Requête SQL générée par l''IA';
COMMENT ON COLUMN ai_answers.reponse IS 'Résultat de l''exécution (status, row_count, colonnes, erreurs, etc.)';
COMMENT ON COLUMN ai_answers.created_at IS 'Date et heure de la question';

