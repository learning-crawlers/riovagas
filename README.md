[![HitCount](http://hits.dwyl.com/learning-crawlers/riovagas.svg)](http://hits.dwyl.com/learning-crawlers/riovagas)

# RioVagas Empregos

Extração de dados com Selenium para encontrar empregos no RioVagas

## Instalação

```
pip install selenium futures hashlib
```

## Modo de usar

Procure o path do python instalado no Windows:

```
/mnt/c/Users/alexb/AppData/Local/Programs/Python/Python37-32/python.exe run.py
```

## Resultado

**Header**

Url, Cargo, Ramo, Salario, Local, Contratacao, Data

**Dados**

```json
{
	"fonte": "RioVagas",
    "url": "https://riovagas.com.br/riovagas/atendente-comercial-consultoria-r-1-30000-pechincha/",
    "cargo": "Atendente Comercial",
    "ramo": "Consultoria",
    "salario": "R$ 1.300,00",
    "local": "Pechincha",
    "contratacao": " CLT \u2013 Efetivo",
    "data": "2019-11-08T13:29:42-03:00"
}
```