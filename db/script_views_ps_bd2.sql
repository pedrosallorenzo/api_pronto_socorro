-- Arquivo para criar as views do sistema
use bd_ps_bd2;
show tables;

-- View para a tela dos médicos
create view vw_fila_medico as
select t.id as id_triagem,
p.id_pessoa as id_paciente,
pe.nome as nome_paciente,
timestampdiff(year, pe.dt_nascimento, CURDATE()) as idade, -- Calcula a idade do paciente
t.prioridade, e.nome as especialidade_requisitada,
l.codigo as leito, t.criado_em,
(select pe2.nome from tb_atendimento a 					   -- Esse comando mostra o último enfermeiro que atendeu o paciente
	join tb_funcionario f2 on f2.id_pessoa = a.id_profissional
	join tb_pessoa pe2 on pe2.id = f2.id_pessoa
    where a.id_triagem = t.id and a.tipo='ENFERMAGEM'
    order by a.iniciado_em desc limit 1) as enfermeiro_responsavel
from tb_triagem t											   -- Juntam as informações necessárias da triagem, pessoa e especialidade e opcionalmente o leito
join tb_paciente p     on p.id_pessoa = t.id_paciente
join tb_pessoa pe      on pe.id = p.id_pessoa
join tb_especialidade e on e.id = t.id_especialidade_requisitada
left join tb_leito l    on l.id = t.id_leito;


-- View que remove os pacientes que já estão sendo atendidos por um médico
create view vw_alocacao_medico as
select v.* from vw_fila_medico v
where not exists (					-- Impede dois médicos no mesmo caso
  select 1 from tb_atendimento a
  where a.id_triagem = v.id_triagem
	and a.tipo='MEDICO'
    and a.status='EM_ANDAMENTO');
    


-- View para a tela do enfermeiro (completa)
create view vw_alocacao_enfermagem as
select
  t.id as id_triagem,
  pe.nome as nome_paciente,
  t.prioridade,
  e.nome as especialidade_requisitada,
  l.codigo as leito,
  t.criado_em
from tb_triagem t
join tb_paciente p on p.id_pessoa = t.id_paciente
join tb_pessoa pe on pe.id = p.id_pessoa
join tb_especialidade e on e.id = t.id_especialidade_requisitada
left join tb_leito l on l.id = t.id_leito
where not exists (
  select 1 from tb_atendimento a
  where a.id_triagem = t.id
   and a.tipo='ENFERMAGEM'
   and a.status='EM_ANDAMENTO');