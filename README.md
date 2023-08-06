# Tietokantasovellus, Kirjasovellus
Sovelluksen tarkoitus on, että käyttäjät voivat lisätä lukemiaan kirjoja kansioihin. Käyttäjät voivat antaa kirjalliseen palautteen tai 1-5 arvion kirjalle.

## Sovelluksen ominaisuuksia:
- Käyttäjä voi luoda tunnuksen, kirjautua, lisää oma kuvan profiiliin, vaihtaa salasanan  *tehty* 
- Käyttäjä voi lisätä kirjoja sovellukseen ja etsiä kirjoja *tehty*
- Käyttäjä voi lisätä kirjoja want to read, currently reading, read ja dropped kansioihin *tekemisissä*
- Kirjan lukemiseen kulunut aika tallennetaan tietokantaan ja se näkyy käyttäjälle
- Käyttäjä voi tehdä omia kansioita ja lisätä kirjoja sinne; voi lisätä kirjailijan, julkaisemisvuoden ja kuvan *tekemisissä*
- Käyttäjä voi lisätä genre tagin esim. horror lukemaansaan kirjaan
- Käyttäjä voi etsiä kirjoja arvion, tagin, kirjailijan tai julkaisemis vuoden perusteella
- Käyttäjät voivat lukea muiden antamia palautteita kirjasta


## Sovelluksen jatkokehityideat:
- Sovelluksessa on lukuryhmiä
- Sovellus suosittelee käyttäjälle esim. lukuryhmän murhamysteerin, koska käyttäjä on lukennut paljon murhamysteeri kirjoja 
- Käyttäjä voi suositella kirjoja muille käyttäjille
- Käyttäjä lähettää kaveripyynnön toiselle käyttäjälle


Sovellus ei ole testattavissa Fly.iossa. 
## Käynnistysohje
Kloonaa repositori, luo kansioon .env tiedostoon 
```
DATABASE_URL=<tietokannan-paikallinen-osoite>
SECRET_KEY=<salainen-avain>
```
Aktivoi virtuaaliympäristö seuravilla komennolla:
```
python3 -m venv venv
source venv/bin/activate
pip install -r ./requirements.txt
```
Määrittele vielä schema:
```
psql < schema.sql
```
Sovellus käynnistyy komennolla:
```
flask run
```
