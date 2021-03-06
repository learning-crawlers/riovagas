# -*- coding: utf-8 -*-
#######################################
##  RioVagas Empregos 
##    Busca de empregos no riovagas com url, cargo, ramo, salario, local, contratacao, data
##
##    Author: Alex Benincasa Santos 
##    Mail: alexbenincasa@ymail.com
##    2019
#######################################

import os
import time
import json
import platform
import hashlib
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By as by
from selenium.webdriver.support.ui import WebDriverWait
from concurrent.futures import ThreadPoolExecutor,as_completed


# caminho para o binário do geckodriver.exe
if platform.system() == 'Linux':
	from os.path import realpath, dirname, join
	ROOT = realpath(dirname(__file__))
	BIN_PATH = join(ROOT, 'bin')
	bin_path = BIN_PATH
	from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
	cap = DesiredCapabilities().FIREFOX
	cap["marionette"] = False
	os.environ["PATH"] = f'{os.environ["PATH"]}:{bin_path}'
else:
	bin_path = 'C:\\www\\riovagas\\geckodriver.exe'
	cap = None

# função para pegar os dados do emprego
def salvarVaga(url):
	try:
		options = Options()
		options.headless = True
		
		browser = webdriver.Firefox(executable_path=bin_path, options=options,capabilities=cap)
		wait = WebDriverWait(browser, 15)
		browser.get(url)

		anuncio = browser.find_element_by_css_selector('article.post')
		entry_title = anuncio.find_element_by_css_selector('h1.entry-title').text

		# geralmente cargo, salário e local vem separado por " – " (travessão)
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

			# em algumas vagaas sem ramo podem vir a quantidade de vagas
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

		# o hash vai identificar a vaga
		hash = 'data/'+hashlib.sha224(anuncio.text.strip().encode('utf-8')).hexdigest()
		fname = hash+(f'-{cargo}-{salario}-{local}.json'.lower().replace('/',''))
		if os.path.isfile(fname):
			raise ValueError(f'[{entry_title}] Vaga já foi cadastrada')

		vaga = {}
		vaga['fonte'] = 'RioVagas'
		vaga['url'] = url.strip()
		vaga['cargo'] = cargo.strip()
		vaga['ramo'] = ramo.strip()
		vaga['salario'] = salario.strip()
		vaga['local'] = local.strip()
		vaga['contratacao'] = ''

		bairro = None

		for info in anuncio.find_elements_by_css_selector('p'):
			if 'Regime de Contratação' in info.text:
				vaga['contratacao'] = info.text.split(':')[1].strip()

			# mais informação sobre o local da vaga
			if 'Bairro' in info.text:
				if local != info.text.split(':')[1].strip():
					bairro = info.text.split(':')[1].strip()

		data_publicacao = anuncio.find_element_by_css_selector('time').get_attribute('datetime')
		vaga['data'] = data_publicacao.strip()

		if bairro:
			vaga['local'] += ' - '+bairro

		# salvar o arquivo com os dados da vaga
		with open(fname, mode="w") as f:
			f.write(json.dumps(vaga, indent=4))

		browser.quit()

	except Exception as e:
		browser.quit()
		print(f'[{entry_title}] '+str(e))

	exit()

options = Options()
options.headless = True
browser = webdriver.Firefox(executable_path=bin_path, options=options)
wait = WebDriverWait(browser, 15)
browser.get('https://riovagas.com.br/category/riovagas/')

links = []
i = 1
while True and i <= 25:
	for el in browser.find_elements_by_css_selector('article.post'):
		links.append(el.find_element_by_css_selector('h2.entry-title a').get_attribute('href'))

	# mágica da paginação infinita
	try:
		browser.find_element_by_css_selector('a.next.page-numbers').click()
	except:
		break

	i += 1

browser.quit()

# threading no python para executar mais rápido (de forma assíncrona)
with ThreadPoolExecutor() as executor:
	futures = { executor.submit(salvarVaga, url): url for url in links } 
	for thread in as_completed(futures):
		try:
			thread.result()
		except Exception as e:
			print(e)
