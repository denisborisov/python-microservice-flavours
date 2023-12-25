# Flashcards Microservice

Flashcards Microservice is a microservice that manages user foreign words and related dictionary entries taken from Google Translate.
<br />
<br />

## Reflected specifics

This microservice leverages Selenium with the Chrome web driver to parse the Google Translate page.
<br />
<br />

## Possible Improvements

#### Related to database

- Break our `details` field in the database into separate fields if we need filtering/sorting by them. Then we will use `ARRAY` type fields and for running tests we will have to abandon SQLite and raise a separate container with a PostgreSQL database.
- Separate the components of the `details` field into separate tables, then SQLite can be left.

#### Related to app

- Use retries, because sometimes the result of the GET API is "no such word", but if you make a second try, this API will reach results from Google API.
- Add logging
- Use a newer version of Python 3.11
- Parameterize additionally source and target languages (separately from the `GOOGLE_TRANSLATOR_URL` environment variable)

#### Related to web scraping

- Make more detailed error handling related to Selenium
- Replace Selenium with an asynchronous framework, e.g. `arsenic`

#### Related to deploy

- Create Helm chart and add its linting
- Create GitLab pipeline
- Strengthen the security of Dockerfile
  - exploit content addressable image identifier (CAAID)
  - unset SUID & SGID permissons
  - add labels
