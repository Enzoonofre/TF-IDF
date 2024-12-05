import spacy
import os
import sys
import math


# Carregar o modelo de linguagem portuguesa
nlp = spacy.load("pt_core_news_lg")

# Encontrar o caminho da pasta
def encontrar_caminho_pasta(pastas, caminho_base):
    x = []
    encontrou_arquivo = False
    caminho_arquivo = None

    for pasta in pastas:
        if pasta.startswith("base"):
            caminho_pasta = os.path.join('.', pasta)
            arquivos2 = os.listdir(caminho_pasta)

            for arquivo in arquivos2:
                arquivo = arquivo.strip()  # Remove quebras de linha e espaços
                if arquivo == caminho_base.split(os.path.sep)[-1]:  # Verifica apenas o nome do arquivo
                    encontrou_arquivo = True
                    caminho_arquivo = os.path.join(caminho_pasta, arquivo)

                    # Verifica se o arquivo existe antes de tentar abrir
                    if os.path.exists(caminho_arquivo):
                        with open(caminho_arquivo, "r", encoding="utf-8") as linhas:
                            for linha in linhas:
                                x.append(linha)
                    else:
                        print(f"Arquivo {caminho_arquivo} não encontrado!")

            if encontrou_arquivo:
                return caminho_pasta, x

    # Caso não encontre a pasta ou arquivo
    if not encontrou_arquivo:
        return "Arquivo não encontrado"



#----------------Construção do Indice Invertido---
class Termo:
    def __init__(self, palavra):
        self.palavra = palavra
        self.ocorrencias = {}  # Um dicionário simples

    def adicionar_ocorrencia(self, doc_id):
        if doc_id in self.ocorrencias:
            self.ocorrencias[doc_id] += 1
        else:
            self.ocorrencias[doc_id] = 1

    def __str__(self):
        return f"{self.palavra}: {self.ocorrencias}"


def processar_textos(textos):
    termos = {}
    for i, texto in enumerate(textos, start=1):  # Enumerar a partir de 1 para identificar o documento
        doc = nlp(texto)
        for token in doc:
            # Remover stopwords, verificar se é alfabético e fazer lematização
            if not token.is_stop and token.is_alpha:
                palavra_lema = token.lemma_.lower()
                if palavra_lema not in termos:
                    termos[palavra_lema] = Termo(palavra_lema)
                # Atualizar a quantidade de vezes que a palavra aparece no documento atual
                termos[palavra_lema].adicionar_ocorrencia(i)
    return termos

def gerarIndiceInvertido(termos, caminho_pasta):
    termos_ordenados = sorted(termos, key=lambda termo: termo.palavra)
    with open(os.path.join(caminho_pasta, "indice.txt"), "w", encoding="utf-8") as f:
        for termo in termos_ordenados:
            if termo.ocorrencias:
                f.write(f"{termo.palavra}: ")
                for doc_id, count in termo.ocorrencias.items():
                    f.write(f"{doc_id}: {count}; ")
                f.write("\n")



#-----------------TF-IDF

def extrair_termos_frequencia(caminho_pasta):
    indice_path = os.path.join(caminho_pasta, "indice.txt")
    termos_frequencia = {}

    with open(indice_path, 'r') as file:
        for linha in file:
            # Remover espaços em branco e quebras de linha
            linha = linha.strip()

            # Separar o termo dos documentos e frequências
            termo, docs = linha.split(": ", 1)

            # Lista para armazenar (documento, frequência) para este termo
            freq_por_doc = []

            # Separar cada documento e sua frequência
            for doc_freq in docs.split(";"):
                if doc_freq.strip():  # Ignorar se houver um campo vazio
                    # Separar doc e freq, removendo espaços extras
                    doc, freq = map(str.strip, doc_freq.split(":"))
                    freq_por_doc.append((int(doc), int(freq)))

            # Armazenar no dicionário
            termos_frequencia[termo] = freq_por_doc

    return termos_frequencia


def calcular_tf_idf(termos_frequencia, N_total, caminho_pasta, x):
    # Caminho do arquivo de saída
    pesos_path = os.path.join(caminho_pasta, "pesos.txt")

    # Organizar termos por documento e calcular TF-IDF
    termos_por_documento = {}

    # Agrupar os termos por documento com suas respectivas frequências
    for termo, freq_por_doc in termos_frequencia.items():
        for doc, freq in freq_por_doc:
            if doc not in termos_por_documento:
                termos_por_documento[doc] = []
            termos_por_documento[doc].append((termo, freq))

    # Calcular TF-IDF e escrever no arquivo
    with open(pesos_path, 'w') as file:
        for i, doc in enumerate(sorted(termos_por_documento.keys())):
            nome_doc = x[i]  # Obter o nome do documento da lista x
            file.write(f"{nome_doc}: ")
            termos_pesos = []
            for termo, freq in termos_por_documento[doc]:
                # Calcular TF
                tf = 1 + math.log(freq) if freq >= 1 else 0
                # Calcular DF
                df = len(termos_frequencia[termo])  # número de documentos em que o termo aparece
                # Calcular IDF
                idf = math.log10(N_total / df) if df >= 1 else 0
                # Calcular TF-IDF
                tf_idf = tf * idf

                # Adicionar termo e seu peso à lista de termos
                termos_pesos.append(f"{termo},{tf_idf:.14f}")  # Adiciona o termo e seu peso

            # Escrever os pesos no formato desejado
            file.write(" ".join(termos_pesos) + "\n")  # Junta os termos com espaço



#----------Main---------

if __name__ == "__main__":
    # Verifica se o número de argumentos é o esperado
    if len(sys.argv) != 2:
        print("Uso: python tfidf.py <base.txt> ")
        sys.exit(1)

    # Listando todos os arquivos da pasta base
    caminho_principal = '.'
    caminho_base = sys.argv[1]  # Caminho para a base de documentos
    # Listar apenas pastas dentro do caminho principal
    pastas = [nome for nome in os.listdir(caminho_principal) if os.path.isdir(os.path.join(caminho_principal, nome))]

    caminho_pasta, x = encontrar_caminho_pasta(pastas, caminho_base)
    textos = []

    x = [arquivo_nome.strip() for arquivo_nome in x]

    #Leitura do conteúdo de cada arquivo e salvando na lista "textos"
    for arquivo_nome in x:
        caminho_arquivo = os.path.join(caminho_pasta, arquivo_nome)  # Use o caminho base

        try:
            with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
                conteudo = arquivo.read()
                textos.append(conteudo)
        except FileNotFoundError:
            print(f"Arquivo não encontrado: {caminho_arquivo}")

    N_total = len(x)

    # Processar os textos
    tokens_lemmatizados = processar_textos(textos)

    # Transformar o dicionário em uma lista de objetos da classe Termo
    lista_termos = list(tokens_lemmatizados.values())

    gerarIndiceInvertido(lista_termos, caminho_pasta)

    resultado = extrair_termos_frequencia(caminho_pasta)

    calcular_tf_idf(resultado, N_total, caminho_pasta,x)
