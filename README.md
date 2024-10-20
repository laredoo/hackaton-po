# hackaton-po
# Modelagem de Problema de Alocação de Pacientes do Instituto Borboleta Azul

**Desafio UniSoma 2024: Daniel Nascimento e Lucas Laredo**  
**Data:** 19 de Outubro de 2024

## Definição do Problema

O objetivo é otimizar o processo de agendamento semanal de atendimentos psicológicos, maximizando a quantidade de atendimentos reais, alocando pacientes (Adultos, Adolescentes e Crianças) a profissionais voluntários ou estagiários, respeitando suas disponibilidades de horários (Segunda até Sábado, 8:00 às 20:00) e restrições de locais (podendo ser remoto ou presencial).

## Conjuntos

Sejam:

- **P**: Conjunto de pacientes (Adultos, Adolescentes, Crianças), indexado por $p$.
- **R**: Conjunto de profissionais (voluntários ou estagiários), indexado por $r$.
- **H**: Conjunto de horários disponíveis, considerando dias e horas (De Seg a Sábado, de 8h às 20h), indexado por $h$.
- **L**: Conjunto de locais, incluindo atendimentos presenciais e virtuais, indexado por $l$.
- **D**: Subconjunto de horários do mesmo dia.
- **LP**: Subconjunto de Locais Presenciais $LP \subset L$.

## Parâmetros

- $z_{p,r}$: Se o paciente $p \in P$ pode ser atendido pelo profissional $r \in R$.  
  (1 se pode ser atendido, 0 caso contrário)
- $dispP_{p,h,l}$: Disponibilidade do paciente $p \in P$ no horário $h \in H$ e local $l \in L$ (1 se disponível, 0 caso contrário).
- $dispR_{r,h,l}$: Disponibilidade do profissional $r \in R$ no dia $d \in D$, horário $h \in H$ e local $l \in L$ (1 se disponível, 0 caso contrário).
- $o_{r}$: Horas disponíveis de cada profissional $r \in R$ na semana.

## Variável de Decisão

$$
x_{p,r,h,l} =
\begin{cases}
    1, & \text{se o paciente } p \in P \text{ for atendido pelo profissional } r \in R,\\
    & \text{no horário } h \in H, \text{ no local } l \in L, \\
    0, & \text{caso contrário}.
\end{cases}
$$

## Função Objetivo

A função objetivo é maximizar o número total de atendimentos realizados:

$$
\text{Maximizar} \quad Z = \sum_{p \in P} \sum_{r \in R} \sum_{h \in H} \sum_{l \in L} x_{p,r,h,l}
$$

## Restrições

### Restrição 1: Cada paciente deve ser atendido no máximo uma vez por semana, por um profissional, em um único dia, horário e local

$$
\sum_{r \in R} \sum_{h \in H} \sum_{l \in L} x_{p,r,h,l} \leq 1 \quad \forall p \in P
$$

### Restrição 2: Um paciente por vez por profissional

$$
\sum_{p \in P} \sum_{l \in L} x_{p,r,h,l} \leq 1 \quad \forall r \in R, \forall h \in H
$$

### Restrição 3: Disponibilidade de pacientes e profissionais

$$
x_{p,r,h,l} \leq dispP_{p,h,l} \cdot dispR_{r,h,l} \cdot z_{p,r} \quad \forall p \in P, \forall r \in R, \forall h \in H, \forall l \in L
$$

### Restrição 4: Limite de horas semanais por profissional

$$
\sum_{p \in P} \sum_{h \in H} \sum_{l \in L} x_{p,r,h,l} \leq o_{r} \quad \forall r \in R
$$

### Restrição 5: Cada profissional pode atender em no máximo um local presencial por dia

$$
\sum_{p \in P} \sum_{r \in R} \sum_{h \in D} x_{p,r,h,l} \leq 1 \quad \forall d \in D, \forall l \in LP
$$
