# Índice Invertido e TF-IDF com SpaCy

## Ideia do Trabalho
O objetivo deste projeto é usar apenas a biblioteca **SpaCy** para:

- Criar um índice invertido.
- Implementar um algoritmo de TF-IDF para calcular a relevância de termos em documentos.

O script gera dois arquivos:

- **indice.txt**: Contém o índice invertido.
- **pesos.txt**: Contém os pesos TF-IDF calculados para os termos.

## Estrutura do Código

O código é dividido em três partes, separadas por comentários com "----":

1. **Índice Invertido**: Funções para criar o índice invertido.
2. **TF-IDF**: Processa o índice e calcula os pesos dos termos.
3. **Main**: Executa as funções das duas partes anteriores.

## Pré-requisitos

- O script precisa estar na mesma pasta que as pastas `base1` e `base_samba`.
- Caso esteja dentro de uma das pastas de base, será necessário ajustar o código.

## Lógica do Programa

1. O programa recebe o nome de uma base (`base.txt`).
2. Ele localiza a base nas pastas `base1` ou `base_samba`.
3. Lê os documentos referenciados na base e tokeniza os textos.
4. Cria objetos da classe `termo` com os seguintes atributos:
   - `palavra`: O termo identificado.
   - `ocorrência`: Um dicionário indicando:
     - Em quais documentos o termo aparece.
     - Quantas vezes aparece.
     - Exemplo: `amor: 0:4, 4:2` (onde 0 e 4 são IDs dos documentos, e os números após os dois pontos indicam a frequência).
5. Na etapa de **TF-IDF**:
   - O índice invertido é processado.
   - Calcula-se a relevância de cada termo em relação aos documentos.
   - Resultados são salvos em `indice.txt` e `pesos.txt`.

## Como Executar

1. Abra o CMD na pasta onde está o arquivo `tfidf.py`.
2. Use o comando:

   ```bash
   python tfidf.py base.txt
