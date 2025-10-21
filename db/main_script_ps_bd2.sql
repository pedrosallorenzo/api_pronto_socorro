-- Banco de dados para o projeto de 
-- banco de dados - Pronto Socorro

-- Criar e usar o banco de dados
create database bd_ps_bd2;
use bd_ps_bd2;


-- Tabela geral de pascientes e funcionários
create table tb_pessoa
(id int not null primary key auto_increment,
nome varchar(200) not null,
cpf char(11) unique not null,
telefone varchar(20),
dt_nascimento date not null,
criado_em timestamp default current_timestamp); -- Esse comando deixa registrado a hora que um novo registro foi feito


-- Tabela dos pacientes
CREATE TABLE tb_paciente (
  id_pessoa INT PRIMARY KEY, -- Usa o mesmo id da tabela pessoa
  tipo_sanguineo ENUM('A+','A-','B+','B-','AB+','AB-','O+','O-') NOT NULL, -- Limita os valores válidos
  historico_medico TEXT);

-- Regra que garante que só haja paciente se houver pessoa
alter table tb_paciente
add CONSTRAINT fk_paciente_pessoa FOREIGN KEY (id_pessoa) 
REFERENCES tb_pessoa (id);


-- Tabela dos funcionários
CREATE TABLE tb_funcionario (
  id_pessoa INT PRIMARY KEY,
  cargo ENUM('MEDICO','ENFERMEIRO','TEC_ENF') NOT NULL, -- Muito importante para a lógica do sistema
  ativo TINYINT(1) NOT NULL DEFAULT 1); -- Verifica se o funcionário está ativo ou não

-- Garante integridade com a tabela pessoa
ALTER TABLE tb_funcionario
ADD CONSTRAINT fk_func_pessoa FOREIGN KEY (id_pessoa) 
REFERENCES tb_pessoa(id);


-- Tabela das especialidades
CREATE TABLE tb_especialidade (
  id INT PRIMARY KEY AUTO_INCREMENT,
  nome VARCHAR(100) UNIQUE NOT NULL -- Evita especialidades duplicadas 
);


-- Tabela médico_especialidade
CREATE TABLE tb_medico_especialidade (
  id_funcionario INT NOT NULL,
  id_especialidade INT NOT NULL,
  PRIMARY KEY (id_funcionario, id_especialidade));
  
  ALTER TABLE tb_medico_especialidade
ADD COLUMN id_pessoa INT;
  
  -- Garante referencias validas
  ALTER TABLE tb_medico_especialidade
  ADD CONSTRAINT fk_me_func FOREIGN KEY (id_funcionario) 
  REFERENCES tb_funcionario(id_pessoa);
  
  ALTER TABLE tb_medico_especialidade
  ADD CONSTRAINT fk_me_esp FOREIGN KEY (id_especialidade) 
  REFERENCES tb_especialidade(id);
  
   -- Garante que somente os médicos acessem essa area
  create table tb_medico (
  id_pessoa int primary key);
  
  alter table tb_medico
  add constraint fk_medico_funcionario foreign key (id_pessoa)
  references tb_funcionario(id_pessoa);
  
  ALTER TABLE tb_medico_especialidade
  ADD CONSTRAINT fk_me_medico foreign key (id_pessoa) references tb_medico(id_pessoa);


-- Tabela leito
CREATE TABLE tb_leito (
  id INT PRIMARY KEY AUTO_INCREMENT,
  codigo VARCHAR(20) UNIQUE NOT NULL,
  status ENUM('LIVRE','OCUPADO','MANUTENCAO') NOT NULL DEFAULT 'LIVRE' -- Controla a disponibilidade do leito
);


-- Tabela para o cadastro dos pacientes pelo técnico
CREATE TABLE tb_triagem (
id INT PRIMARY KEY AUTO_INCREMENT,
id_paciente INT NOT NULL,
pa VARCHAR(15),                 -- pressão arterial (ex.: 120x80)
pulso SMALLINT,
saturacao TINYINT,
temperatura DECIMAL(4,1),
sintomas TEXT,
prioridade ENUM('LEVE','MODERADA','ALTA') NOT NULL,
id_especialidade_requisitada INT NOT NULL,
id_leito INT NULL,
criado_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP);
  
-- Garante integridade com a tabela paciente
ALTER TABLE tb_triagem 
ADD CONSTRAINT fk_tri_pac FOREIGN KEY (id_paciente) 
REFERENCES tb_paciente(id_pessoa);
  
-- Garante integridade com a tabela especialidade
ALTER TABLE tb_triagem
ADD CONSTRAINT fk_tri_esp FOREIGN KEY (id_especialidade_requisitada) 
REFERENCES tb_especialidade(id);
  
-- Garante integridade com a tabela leito
ALTER TABLE tb_triagem
ADD CONSTRAINT fk_tri_leito FOREIGN KEY (id_leito) 
REFERENCES tb_leito(id);


-- Tabela do atendimento (enfermeros e médicos)
-- A cada caso pego, aperece um registro aqui
CREATE TABLE tb_atendimento (
id INT PRIMARY KEY AUTO_INCREMENT,
id_paciente INT NOT NULL,
id_triagem INT NOT NULL,
tipo ENUM('ENFERMAGEM','MEDICO') NOT NULL,
id_profissional INT NOT NULL,
status ENUM('AGUARDANDO','EM_ANDAMENTO','FINALIZADO') NOT NULL DEFAULT 'AGUARDANDO',
iniciado_em DATETIME NULL,
finalizado_em DATETIME NULL);
  
-- Essas regras "juntam" as informações da triagem, paciente e dos medicos / enfermeiros
alter table tb_atendimento
add constraint fk_at_pac foreign key (id_paciente) 
references tb_paciente(id_pessoa);
  
alter table tb_atendimento
add constraint fk_at_tri foreign key (id_triagem)
references tb_triagem(id);
  
alter table tb_atendimento
add constraint fk_at_prof foreign key (id_profissional)
references tb_funcionario(id_pessoa);


-- Tabela de seleção / alternancia dos casos
CREATE TABLE tb_selecoes_atendimento (
id INT PRIMARY KEY AUTO_INCREMENT,
id_atendimento INT NOT NULL,
id_profissional INT NOT NULL,
selecionado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP);

-- Essas regras evitam que dois profissionais com o mesmo cargo selecionem o mesmo caso
alter table tb_selecoes_atendimento
add constraint fk_sel_at foreign key (id_atendimento)
references tb_atendimento(id);

alter table tb_selecoes_atendimento
add constraint fk_sel_prof foreign key (id_profissional) 
references tb_funcionario(id_pessoa);

-- Tabela para os prontuários
CREATE TABLE tb_prontuario (
  id INT PRIMARY KEY AUTO_INCREMENT,
  id_paciente INT NOT NULL,
  id_atendimento INT NULL,
  texto TEXT,
  criado_por INT NOT NULL,  -- funcionário autor
  criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP);
  
  -- Relacionamentos para o id_paciente, id_atendiemnto
  alter table tb_prontuario
  add constraint fk_pr_pac foreign key (id_paciente)
  references tb_paciente(id_pessoa);
  
  alter table tb_prontuario
  add constraint fk_pr_at foreign key (id_atendimento) 
  references tb_atendimento(id);
  
  -- Garante quem criou o prontuario
  alter table tb_prontuario
  add constraint fk_pr_autor foreign key (criado_por) 
  references tb_funcionario(id_pessoa);


-- Tabela para internação pelo médico
CREATE TABLE tb_internacao (
  id INT PRIMARY KEY AUTO_INCREMENT,
  id_paciente INT NOT NULL,
  id_leito INT NOT NULL,
  motivo TEXT NOT NULL,
  admitido_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  alta_em DATETIME NULL,
  deu_alta INT NULL);  -- médico responsável pela alta
  
  -- Cria os relacionamentos para os dados de id_paciente, id_leito
  alter table tb_internacao
  add constraint fk_int_pac foreign key (id_paciente) 
  references tb_paciente(id_pessoa);
  
  alter table tb_internacao
  add constraint fk_int_leito foreign key (id_leito) 
  references tb_leito(id);
  
  -- Mostra o médico responsável pela alta do paciente
  alter table tb_internacao
  add constraint fk_int_med foreign key (deu_alta) 
  references tb_funcionario(id_pessoa);


-- Tabela de cadastro / login
CREATE TABLE tb_usuario_auth (
  id_funcionario INT PRIMARY KEY,
  hash_senha VARCHAR(255) NOT NULL,
  ultimo_login DATETIME NULL,
  bloqueado TINYINT(1) NOT NULL DEFAULT 0);
  
  -- Relaciona o id_funcionario da tabela tb_funcionario
  alter table tb_usuario_auth
  add constraint fk_auth_func foreign key (id_funcionario) 
  references tb_funcionario(id_pessoa);


-- Índices para as telas e filas
-- Aceleram as consultas das telas de fila e relatórios:
CREATE INDEX ix_tri_prioridade ON tb_triagem (prioridade, criado_em);
CREATE INDEX ix_tri_esp ON tb_triagem (id_especialidade_requisitada, prioridade, criado_em);
CREATE INDEX ix_at_status ON tb_atendimento (tipo, status);
CREATE INDEX ix_int_leito ON tb_internacao (id_leito, alta_em);