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
    "Url": "https://riovagas.com.br/riovagas/atendente-comercial-consultoria-r-1-30000-pechincha/",
    "Cargo": "Atendente Comercial",
    "Ramo": "Consultoria",
    "Salario": "R$ 1.300,00",
    "Local": "Pechincha",
    "Contratacao": " CLT \u2013 Efetivo",
    "Data": "2019-11-08T13:29:42-03:00"
}
```