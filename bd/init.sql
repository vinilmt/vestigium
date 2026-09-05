CREATE TABLE USUARIO (
    id UUID PRIMARY KEY,
    email VARCHAR NOT NULL UNIQUE,
    senha_hash VARCHAR NOT NULL,
    data_criacao TIMESTAMP NOT NULL
);


CREATE TABLE INVESTIGACAO (
    id UUID PRIMARY KEY,
    usuario_id UUID NOT NULL,
    titulo VARCHAR NOT NULL,
    tipo_entrada VARCHAR NOT NULL,
    conteudo_original TEXT NOT NULL,
    status VARCHAR NOT NULL,
    data_criacao TIMESTAMP NOT NULL,
    data_atualizacao TIMESTAMP NOT NULL,

    CONSTRAINT fk_investigacao_usuario
        FOREIGN KEY (usuario_id)
        REFERENCES USUARIO(id)
);


CREATE TABLE FONTE (
    id UUID PRIMARY KEY,
    investigacao_id UUID NOT NULL,
    url TEXT NOT NULL,
    titulo VARCHAR NOT NULL,
    conteudo TEXT,
    tipo VARCHAR,
    data_acesso TIMESTAMP,

    CONSTRAINT fk_fonte_investigacao
        FOREIGN KEY (investigacao_id)
        REFERENCES INVESTIGACAO(id)
);


CREATE TABLE AFIRMACAO (
    id UUID PRIMARY KEY,
    investigacao_id UUID NOT NULL,
    fonte_id UUID,
    texto TEXT NOT NULL,
    relevancia DECIMAL,
    data_criacao TIMESTAMP NOT NULL,

    CONSTRAINT fk_afirmacao_investigacao
        FOREIGN KEY (investigacao_id)
        REFERENCES INVESTIGACAO(id),

    CONSTRAINT fk_afirmacao_fonte
        FOREIGN KEY (fonte_id)
        REFERENCES FONTE(id)
);


CREATE TABLE PERGUNTA (
    id UUID PRIMARY KEY,
    afirmacao_id UUID NOT NULL,
    texto TEXT NOT NULL,
    resposta TEXT,
    tipo VARCHAR,
    data_criacao TIMESTAMP NOT NULL,

    CONSTRAINT fk_pergunta_afirmacao
        FOREIGN KEY (afirmacao_id)
        REFERENCES AFIRMACAO(id)
);


CREATE TABLE EVIDENCIA (
    id UUID PRIMARY KEY,
    afirmacao_id UUID NOT NULL,
    fonte_id UUID NOT NULL,
    descricao TEXT NOT NULL,
    trecho TEXT,
    tipo VARCHAR,
    data_criacao TIMESTAMP NOT NULL,

    CONSTRAINT fk_evidencia_afirmacao
        FOREIGN KEY (afirmacao_id)
        REFERENCES AFIRMACAO(id),

    CONSTRAINT fk_evidencia_fonte
        FOREIGN KEY (fonte_id)
        REFERENCES FONTE(id)
);


CREATE TABLE REFLEXAO (
    id UUID PRIMARY KEY,
    afirmacao_id UUID NOT NULL,
    texto TEXT NOT NULL,
    data_criacao TIMESTAMP NOT NULL,

    CONSTRAINT fk_reflexao_afirmacao
        FOREIGN KEY (afirmacao_id)
        REFERENCES AFIRMACAO(id)
);


CREATE TABLE CONCLUSAO (
    id UUID PRIMARY KEY,
    investigacao_id UUID NOT NULL UNIQUE,
    texto TEXT NOT NULL,
    data_criacao TIMESTAMP NOT NULL,
    data_atualizacao TIMESTAMP NOT NULL,

    CONSTRAINT fk_conclusao_investigacao
        FOREIGN KEY (investigacao_id)
        REFERENCES INVESTIGACAO(id)
);
