import os

# Configurando o Proxy
os.environ['http_proxy']='proxy.globoi.com:3128'
os.environ['HTTP_PROXY']='proxy.globoi.com:3128'
os.environ['https_proxy']='proxy.globoi.com:3128'
os.environ['HTTPS_PROXY']='proxy.globoi.com:3128'
os.environ['NO_PROXY']='localhost,127.0.0.1, 10.,.globoi.com,i.s3.glbimg.com'