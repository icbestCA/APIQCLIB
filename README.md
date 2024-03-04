# APIQCLIB
# Web Scraping API for Bibliotheque de la Ville de Québec

[https://www.bibliothequedequebec.qc.ca/](https://www.bibliothequedequebec.qc.ca/)

This RESTful API work with Python and Selenium, the requests are handled with Flask.

## Hosting the API
To self-host the API do the following steps, I consider that you already have PIP and Python.
1. Install flask with PIP  `pip install flask`
2. Intsall Selenium with PIP `pip install selenium`
3. Download [firefox](https://www.mozilla.org/en-US/firefox/all/#product-desktop-release) and [geckodriver](https://github.com/mozilla/geckodriver/releases), this API work with the firefox browser.
4. Dowload my Python script (app.py)
5. Unzip the gecko driver folder and add the directory in the file app.py at line 26
6. Run this command in the directory of the app.py `flask run`

## Requests

For a request you will need to POST json data, here an example in python
```
api_url = 'http://127.0.0.1:5000/login'

data_to_extract = ['welcome_message', 'selected_value', 'documents_en_retard']

# JSON data containing the username, password, and data_to_extract
data = {'username': username, 'password': password, 'data_to_extract': data_to_extract}

# Send a POST request to the API
response = requests.post(api_url, json=data)
```

The API url is the one of the flask app which is by default localhost:5000 .
See rqts.py for a complete example of the a request.

## Data

Username is 6 digit: 012345
Password could be anything

| Value Name            | Meaning                                                                    | Response                                         |
| --------------------- | -------------------------------------------------------------------------- | ------------------------------------------------ |
| total_prets           | Total of actual books borrowed                                             | Numerical value: 0, 1, 2, ...                    |
| docs_retard           | Total of actual books borrowed overdue                                     | Numerical value: 0, 1, 2, ...                    |
| email                 | Get the email associaoted to the account if exist                          | example@example.com                              |
| user_name             | Get last and first name of the user                                        | Smith, Jack                                      |
| biblio_pref           | The library set as preference by the user (most of the time the nearest)   | MAIS    --  4 letter code see [[#Library Table]] |
| frais_table           | Table in html of all the things the user should pay                        | Raw html table                                   |
| payment_history_table | Table of the history of what the user already paid. (not always available) | Raw html table                                   |




## Library Table

| Code | Library                  |
| ---- | ------------------------ |
| ALIE | Aliette-Marchand         |
| BONP | Bon-Pasteur              |
| CHAM | Champigny                |
| CHAH | Charles-H.-Blais         |
| CHRY | Chrystine-Brouillet      |
| CLAI | Claire-Martin            |
| COLL | Collège-des-Jésuites     |
| DUCH | Du-Chemin-Royal          |
| ETIE | Etienne-Parent           |
| FELI | Félix-Leclerc            |
| FERN | Fernand-Dumont           |
| JEAN | Jean-Baptiste-Duberger   |
| LEBO | Lebourgneuf              |
| LETO | Le Tournesol             |
| MAIS | Maison de la littérature |
| MARI | Marie-Claire-Blais       |
| MONI | Monique-Corriveau        |
| NEUF | Neufchâtel               |
| PAUL | Paul-Aimé-Paiement       |
| ROGE | Roger-Lemelin            |
| ROMA | Romain-Langlois          |
| STAL | Saint-Albert             |
| STAN | Saint-André              |
| STCH | Saint-Charles            |
| STSA | Saint-Sauveur            |
