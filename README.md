# HelpRedirect
É um sistema bem simples desenvolvido em python 3 + Flask para auxiliar na construção de regras básicas de redirect com foco inicial no Nginx. Permite construir automaticamente essas regras a partir de listas de URLS com validação de "inputs" evitando erros em sua construção, permite, através de um botão, copiar o resultado para área de transferência para que o mesmo possa ser levado ao arquivo de configuração com um simples "Ctrl + v" e permite ainda verificar o status das URLs trazendo informações de locations, códigos HTTP e alguns items do cabeçalho do request.

# Utilização Local
A utilização local é muito simples e seguirá basicamentes os seguintes passos:
* Caso seu sistema não possua, fazer o download e instalação do Python 3;
* Caso seu sistema não possua, fazer a instalação do Virtualenv;
* Efetuar o clone do projeto;
* Configurar e iniciar o Virtualenv no diretorio clonado;
* Instalar os pré-requisitos através do arquivo __requeriments.txt__;
* Rodar o arquivo principal __helpredirect.py__.

__Obs:__ Para a utilização local é necessário desativar as configurações de proxy da app acrescentando o caracter __'#'__ no início da linha 18 `import settings` do arquivo __helpredirect.py__, ficando `#import settings`.


## Download e instalação do Python 3
Siga as instruções desse link: https://wiki.python.org/moin/BeginnersGuide/Download

## Instalação do Virtualenv
Siga as instruções do link: https://virtualenv.pypa.io/en/latest/installation.html

## Clone with HTTPS
```
git clone https://gitlab.globoi.com/leonardo.brito/helpredirect.git
```

## Ou

## Clone with SSH
```
git clone gitlab@gitlab.globoi.com:leonardo.brito/helpredirect.git
```

## Configure e Inicie o Virtualenv
Para configurar o Virtualenv defina a versão do Python, clolocando o PATH de instalação do seu binário no parâmetro __"--python"__, conforme exemplo abaixo:
```
virtualenv --python=<path para a versão do python a ser usada> <NOME_DO_AMBIENTE>
```

Inicie o ambiente no diretório do projeto:
```
virtualenv <NOME_DO_AMBIENTE>\bin\activate` ou `. <NOME_DO_AMBIENTE>\bin\activate
```

Quando for desligar o ambiente:
```
deactivate
```

## Instale os Pré-requisitos
Com o ambiente Virtualenv ativado instale os pré-requisitos:
```
pip install -r requeriments.txt
```

## Execute o Arquivo Principal
Com o ambiente Virtualenv ativado execute o arquivo principal:
```
python helpredirect.py
```
