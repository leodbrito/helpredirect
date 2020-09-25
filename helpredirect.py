# -*- coding: utf-8 -*-
# Web app para ajuda na configuração de
# redirects no nginx
# - permite verificar URLs de origem duplicadas
# - permite verificar o destino de URLs
# - permite construir regras de acordo com listas de
#   URLs de origem e de destino
#  
# Criado em 10/07/2020
# Autor: Leonardo Ferreira de Brito <leonardo.brito@g.globo>
# Versão: 1.0 

import os
import time

from flask import Flask, Response, render_template, request, redirect, session, flash, url_for

import settings
from models import HelpRedirect

app = Flask(__name__)
app.secret_key = "j&H20BUC$bQ9"


@app.route("/")
def index():
    return render_template("home.html")

@app.route("/build_rules")
def build_rules():
    source_url = []
    dest_url = []
    validations = HelpRedirect().clear_validations()
    return render_template("build_rules.html", source_url = source_url, dest_url = dest_url, validations = validations)

@app.route("/builded_rules", methods=["POST",])
def builded_rules():
    source_url = request.form["source_url"]
    dest_url = request.form["dest_url"]
    help_redirect = HelpRedirect(source_url, dest_url)
    rule_list = help_redirect.create_rule_list()
    validations = help_redirect.input_validate()
    dest_url_status_list = help_redirect.check_url_status(False)
    dest_url_has_an_error = False
    for dic in dest_url_status_list:
        for k in dic.keys():
            if "error" in k.lower() or "ops" in k.lower():
                dest_url_has_an_error = True
                break
    if validations["match_values_error"] == True or validations["have_duplicates"] == True or \
        validations["have_invalid_source_url"] == True or validations["have_invalid_dest_url"] == True or \
        validations["have_path_duplicates"] == True:
        if validations["match_values_error"] == True:
            flash(validations["match_values_error_msg"])
        return render_template("build_rules.html", source_url = source_url, dest_url = dest_url, validations = validations)
    else:
        return render_template("builded_rules.html", rule_list = rule_list, dest_url_status_list = dest_url_status_list, dest_url_has_an_error = dest_url_has_an_error)

@app.route("/check_url_status")
def check_url_status():
    url_list =[]
    validations = HelpRedirect().clear_validations()
    return render_template("check_url_status.html", url_list = url_list, validations = validations)

@app.route("/url_status", methods=["POST",])
def url_status():
    url_list = request.form["check_url"]
    help_redirect = HelpRedirect(url_list)
    validations = help_redirect.input_validate()
    validations["duplicates_msg"] = "[ Falha ] Na lista de URLs NÃO podem haver duplicatas!"
    validations["invalid_source_url_msg"] = "[ Falha ] URL(s) inválida(s)! Verifique se em sua composição é seguido o modelo protocol://domain/path"
    url_status_list = help_redirect.check_url_status()
    if validations["have_duplicates"] == True or validations["have_invalid_source_url"] == True:
        return render_template("check_url_status.html", url_list = url_list, validations = validations)
    return render_template("url_status.html", url_status_list = url_status_list)

@app.route("/healthcheck")
def healthcheck():
    return f'WORKING'


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888, debug=True)
