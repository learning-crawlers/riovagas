# -*- coding: utf-8 -*-
#######################################
##  STF Remuneração 
##    Lista de remuneração de servidores ativos do stf com nome, cargo, fc/cj, bruto (R$), líquido (R$)
##
##    Author: Alex Benincasa Santos 
##    Mail: alexbenincasa@ymail.com
##    2019
#######################################

import os
import time
import json
import hashlib
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By as by
from selenium.webdriver.support.ui import WebDriverWait
from concurrent.futures import ThreadPoolExecutor,as_completed

# caminho para o binário do geckodriver.exe
bin_path = 'C:\\www\\olx-empregos\\geckodriver.exe'

# função para pegar os dados do emprego
def salvarVaga(url):
	try:
		options = Options()
		options.headless = True
		
		browser = webdriver.Firefox(executable_path=bin_path, options=options)
		wait = WebDriverWait(browser, 15)
		browser.get(url)

		anuncio = browser.find_element_by_css_selector('article.post')
		entry_title = anuncio.find_element_by_css_selector('h1.entry-title').text

		if ' – ' not in entry_title:
			raise ValueError(f'[{entry_title}] Vaga sem valor de salário')

		info = entry_title.split(' – ')

		if len(info) == 5:
			cargo = info[0]
			ramo = info[1]
			salario = info[2]
			local = info[3]
		elif len(info) == 4:
			cargo = info[0]
			ramo = info[1]
			salario = info[2]
			local = info[3]

			if 'R$' in ramo:
				cargo = info[0]
				ramo = ''
				salario = info[1]
				local = info[2]

		elif len(info) == 3:
			cargo = info[0]
			ramo = ''
			salario = info[1]
			local = info[2]
		else:
			salario = None

		# não cadastra anuncio se não tiver salário
		if 'R$' not in salario:
			raise ValueError(f'[{entry_title}] Vaga sem valor de salário')

		hash = 'data/'+hashlib.sha224(anuncio.text.strip().encode('utf-8')).hexdigest()
		fname = hash+f'-{cargo}-{salario}-{local}.json'.lower()
		if os.path.isfile(fname):
			raise ValueError(f'[{entry_title}] Vaga já foi cadastrada')

		vaga = {}
		vaga['Url'] = url.strip()
		vaga['Cargo'] = cargo.strip()
		vaga['Ramo'] = ramo.strip()
		vaga['Salario'] = salario.strip()
		vaga['Local'] = local.strip()
		vaga['Contratacao'] = ''

		bairro = None

		for info in anuncio.find_elements_by_css_selector('p'):
			if 'Regime de Contratação' in info.text:
				vaga['Contratacao'] = info.text.split(':')[1].strip()

			if 'Bairro' in info.text:
				if local != info.text.split(':')[1].strip():
					bairro = info.text.split(':')[1].strip()

		data_publicacao = anuncio.find_element_by_css_selector('time').get_attribute('datetime')
		vaga['Data'] = data_publicacao.strip()

		if bairro:
			vaga['Local'] += ' - '+bairro

		browser.quit()

		with open(fname, mode="w") as f:
			f.write(json.dumps(vaga, indent=4))

	except Exception as e:
		print(f'[{entry_title}] ERRO')
		print(e)
		browser.quit()

	exit()

options = Options()
options.headless = True
browser = webdriver.Firefox(executable_path=bin_path, options=options)
wait = WebDriverWait(browser, 15)
browser.get('https://riovagas.com.br/category/riovagas/')

links = []
i = 1
while True and i <= 5:
	for el in browser.find_elements_by_css_selector('article.post'):
		links.append(el.find_element_by_css_selector('h2.entry-title a').get_attribute('href'))

	try:
		browser.find_element_by_css_selector('a.next.page-numbers').click()
	except:
		break

	i += 1

browser.quit()

with ThreadPoolExecutor() as executor:
	futures = { executor.submit(salvarVaga, url): url for url in links } 
	for future in as_completed(futures):
		try:
			future.result()
		except Exception as er:
			print(er)