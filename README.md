# Data Lakehouse

Construindo a imagem:
```bash
docker build -t datalakehouse .
```

Acessando o container:
```bash
docker run -dit -v $(pwd):/app --name datalakehouse datalakehouse  tail -f /dev/null
docker exec -it datalakehouse bash
```

Inicialização:
```bash
conda init
source ~/.bashrc
```