---
license: cc0-1.0
task_categories:
- tabular-regression
- time-series-forecasting
language:
- pt
tags:
- fipe
- veiculos
- brasil
- carros
- precos
pretty_name: fipeX - Dados de Veículos da Tabela FIPE
size_categories:
- 1M<n<10M
---

# fipeX: Dataset Completo da Tabela FIPE

Este dataset contém preços históricos e atuais de veículos comercializados no Brasil, baseados na Tabela FIPE (Fundação Instituto de Pesquisas Econômicas).
Os dados foram extraídos e organizados pelo projeto [fipeX](https://www.fipex.com.br), uma iniciativa independente para facilitar o acesso a dados automotivos públicos.

## Sobre o Dataset

Este conjunto de dados é ideal para:
- Análise de depreciação de veículos.
- Previsão de preços (Machine Learning).
- Estudos econômicos sobre o mercado automotivo brasileiro.
- Criação de aplicações de consulta.

### Estrutura dos Dados

**Formato do Arquivo**  : O arquivo original utiliza tabulação (\t) como separador (TSV), em vez de vírgulas. Isso garante a integridade dos dados, evitando conflito com vírgulas presentes nos nomes de modelos ou marcas.

| Coluna           | Tipo   | Descrição                                                    |
|------------------|--------|--------------------------------------------------------------|
| codigo_fipe      | string | Código único do veículo na FIPE.                             |
| nome_modelo      | string | Nome do modelo (ex: Palio 1.0, Corolla XEi).                 |
| nome_marca       | string | Fabricante do veículo (ex: Fiat, Toyota).                    |
| nome_combustivel | string | Tipo de combustível (Gasolina, Diesel, etc).                 |
| ano_modelo       | int    | Ano de fabricação do modelo                                  |
| valor_centavos   | int    | Valor do veículo em centavos (evita erros de ponto flutuante |
| valor_formatado  | string | Valor do veículo em Reais (R$) para facilidade de leitura.   |
| mes_referencia   | int    | Mês de referência da tabela FIPE (1-12).                     |
| ano_referencia   | int    | Ano de referência da tabela FIPE.                            |

## Aviso Legal

Este dataset é derivado de informações públicas disponibilizadas pela FIPE. O fipeX é um projeto independente e **não possui afiliação** com a Fundação Instituto de Pesquisas Econômicas (FIPE).

Os dados são fornecidos "como estão", sem garantias de precisão absoluta. Recomenda-se utilizar com cautela para decisões financeiras críticas.

## Atualização

Os dados são extraídos do banco de dados do FipeX. A intenção é manter este dataset atualizado mensalmente conforme a FIPE libera novas tabelas.
