# Usa a imagem oficial do Miniconda como base
FROM anaconda/miniconda:latest

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Cria um usuário não-root por questões de segurança
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

ENV CONDA_PLUGINS_AUTO_ACCEPT_TOS=true


# 1. Cria o ambiente 'datalakehouse' com Python 3.10
# 2. Instala o pandas, pyspark (Spark + Spark SQL) e o openjdk pelo canal conda-forge
# 3. Limpa o cache para reduzir o espaço em disco da imagem
RUN conda create -n datalakehouse python=3.10 pandas pyspark openjdk openpyxl -y && \
    conda config --set default_activation_env datalakehouse && \
    conda clean -afy

# Copia o código fonte do seu projeto
COPY . .

EXPOSE 8000
