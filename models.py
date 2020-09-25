import re
import requests


class HelpRedirect:
    def __init__(self, source_url=None, dest_url=None):
        self.source_url = source_url
        self.dest_url = dest_url

    def clear_validations(self):
        validations = {
                        "match_values_error": False, 
                        "match_values_error_msg": "[ Falha ] Para que a construção das regras seja correto é necessário o mesmo número de URLs de origem e destino!",
                        "have_duplicates": False,
                        "duplicates_msg": "[ Falha ] Na lista de URLs de origem NÃO podem haver duplicatas!",
                        "source_urls_duplicates_list": [],
                        "have_path_duplicates": False,
                        "path_duplicates_msg": "[ Falha ] Na lista de URLs de origem NÃO podem haver duplicatas de 'PATH'!",
                        "source_urls_path_duplicates_list": [],
                        "have_invalid_source_url": False,
                        "invalid_source_url_msg": "[ Falha ] URL(s) de origem inválida(s)! Verifique se em sua composição é seguido o modelo protocol://domain/path",
                        "invalid_source_url_list": [],
                        "have_invalid_dest_url": False,
                        "invalid_dest_url_msg": "[ Falha ] URL(s) de destino inválida(s)! Verifique se em sua composição é seguido o modelo protocol://domain/path",
                        "invalid_dest_list": []
                        }
        return validations

    def input_validate(self):
        source_url = str(self.source_url).strip().split()
        dest_url = str(self.dest_url).strip().split()
        invalid_source_url_list = []
        invalid_dest_url_list = []
        source_urls_duplicates_list = []
        source_urls_path_list = []
        source_urls_path_duplicates_list = []
        validations = self.clear_validations()
        # Verificando se na lista de URLs de destino, caso seja > 1, tem a mesma quantidade de URLs de origem 
        if len(dest_url) > 1 and len(dest_url) != len(source_url):
            validations["match_values_error"] = True
        # Verificando se na lista de URLs de origem tem duplicatas ou URLs inválidas
        for url in source_url:
            if re.search('\.(com|br|globo)/.', url.lower()):
                if source_url.count(url) > 1 and source_urls_duplicates_list.count(url) == 0:
                    source_urls_duplicates_list.append(url)
                else:
                    # Criando uma lista de paths
                    path = re.sub("^.+\.(com|globo|br)/", "/", url)
                    if not re.search("/$", path):
                        path = path.replace(path, path+"/",1)
                    source_urls_path_list.append(path)
            else:
                invalid_source_url_list.append(url)
        for path in source_urls_path_list:
            if source_urls_path_list.count(path) > 1 and source_urls_path_duplicates_list.count(path) == 0:
                source_urls_path_duplicates_list.append(path)

        # Preenchendo as listas com os erros encontrados
        if len(source_urls_duplicates_list) > 0:
            validations["have_duplicates"] = True
            validations["source_urls_duplicates_list"] = source_urls_duplicates_list
        if len(source_urls_path_duplicates_list) > 0:
            validations["have_path_duplicates"] = True
            validations["source_urls_path_duplicates_list"] = source_urls_path_duplicates_list
        if len(invalid_source_url_list) > 0:
            validations["have_invalid_source_url"] = True
            validations["invalid_source_url_list"] = invalid_source_url_list
        for url in dest_url:
            if not re.search('^(http|https)://.+\.(com|br|globo|info|net|org|biz|name|pro|aero|asia|cat|coop|edu|eu|gal|gov|int|jobs|mil|mobi|museum|news|tel|travel|xxx)/?', url.lower()):
                invalid_dest_url_list.append(url)
        if len(invalid_dest_url_list) > 0:
            validations["have_invalid_dest_url"] = True
            validations["invalid_dest_url_list"] = invalid_dest_url_list
        return validations

    def create_rule_list(self):
        source_url = str(self.source_url).strip().split()
        dest_url = str(self.dest_url).strip().split()
        validations = self.input_validate()
        rule_list = []
        compile1 = re.compile(r'^.+\.(com|globo|br)/', flags=re.IGNORECASE)
        if validations["match_values_error"] == False and validations["have_duplicates"] == False and validations["have_invalid_source_url"] == False:
            for url in source_url:
                if len(dest_url) == 1:
                    compiled = str(compile1.sub(r'rewrite ^/',url))
                    if url.rfind('.',-6) != -1:
                        rule_list.append(compiled+f'$ {dest_url[0]} permanent;')
                    elif url.rfind('/',-1) != -1:
                        rule_list.append(compiled+f'?$ {dest_url[0]} permanent;')
                    else:
                        rule_list.append(compiled+f'/?$ {dest_url[0]} permanent;')
                elif len(dest_url) == len(source_url):
                    compiled = str(compile1.sub(r'rewrite ^/',url))
                    if url.rfind('.',-6) != -1:
                        rule_list.append(compiled+f'$ {dest_url[source_url.index(url)]} permanent;')
                    elif url.rfind('/',-1) != -1:
                        rule_list.append(compiled+f'?$ {dest_url[source_url.index(url)]} permanent;')
                    else:
                        rule_list.append(compiled+f'/?$ {dest_url[source_url.index(url)]} permanent;')
        return rule_list

    def check_url_status(self, is_source=True):
        if is_source:
            url_list = str(self.source_url).strip().split()
        else:
            url_list = str(self.dest_url).strip().split()
        url_status_list = []
        request_error = False
        for url in url_list:
            url_status = {
                            "URL": url,
                            "history_list": [],
                            "Server": "",
                            "X-Sered-from": "",
                            "Cache-Control": "",
                            "Via": ""
                        }
            if not re.search('^(http://|https://)', url.lower()):
                url = f'http://{url}'
            try:
                request = requests.get(url, timeout = 1)
                request.raise_for_status()
            except requests.exceptions.HTTPError as errh:
                url_status["Http Error"] = errh
            except requests.exceptions.ConnectionError as errc:
                url_status["Error Connecting"] = errc
            except requests.exceptions.Timeout as errt:
                url_status["Timeout Error"] = errt
            except requests.exceptions.RequestException as err:
                url_status["Ops, Something Else"] = err
            try:
                request
            except:
                request_error = True
            url_status["history_list"] = []
            if request_error == False:
                for location in request.history:
                    url_status["history_list"].append({"Location": location.url, "HTTP Status Code": location.status_code})
                url_status["history_list"].append({"Location": request.url, "HTTP Status Code": request.status_code})
            try:
                headers = request.headers
            except:
                headers = None
            if headers != None:
                for k, v in headers.items():
                    if "server" in k.lower():
                        url_status["Server"] = v
                    if "x-served-from" in k.lower():
                        url_status["X-Sered-from"] = v
                    if "cache-control" in k.lower():
                        url_status["Cache-Control"] = v
                    if "via" in k.lower():
                        url_status["Via"] = v
            url_status_list.append(url_status)
        return url_status_list