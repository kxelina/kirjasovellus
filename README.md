# Tietokantasovellus, Kirjasovellus
Sovelluksen tarkoitus on, että käyttäjät voivat lisätä lukemiaan kirjoja kansioihin. Käyttäjät voivat antaa kirjalliseen palautteen tai 1-5 arvion kirjalle.

Sovellus ei ole testattavissa Fly.iossa. Sovellusta on testattu itse ja voi testata käynnistysohjeiden avulla.
## Sovelluksen ominaisuuksia:
- Käyttäjä voi luoda tunnuksen, kirjautua, lisää oma kuvan profiiliin, vaihtaa salasanan  **tehty**
- Käyttäjä voi lisätä kirjoja sovellukseen ja etsiä kirjoja **tehty**
- Käyttäjä voi lisätä kirjoja want to read, currently reading, read ja dropped kansioihin **tehty**
- Käyttäjä voi tehdä omia kansioita ja lisätä kirjoja sinne; voi lisätä kirjailijan, julkaisemisvuoden ja kuvan **tehty, paitsi kuvan lisääminen**
- Käyttäjät voivat kirjoittaa palautteen ja lukea muiden antamia palautteita kirjasta **tehty**
- Käyttäjä voi poistaa kirjan kansiosta **kesken**


## Sovelluksen jatkokehityideat:
- Lisätään järjestelmänvalvoja: Kirjojen, käyttäjien ja kommenttejen poistaminen
- Käyttäjä voi lukita kirjan siten, että muut ei pysty muokkamaan kirjan tietoja tai sitten lisää kirjan kaikkien käyttöön
- Käyttäjä voi lisätä genre tagin esim. horror lukemaansaan kirjaan (vastaava toiminto kirjan lisäminen kansioon)
- Kirjan lukemiseen kulunut aika tallennetaan tietokantaan ja se näkyy käyttäjälle
- Käyttäjä voi etsiä kirjoja arvion, tagin, kirjailijan tai julkaisemis vuoden perusteella
- Sovelluksessa on lukuryhmiä
- Sovellus suosittelee käyttäjälle esim. lukuryhmän murhamysteerin, koska käyttäjä on lukennut paljon murhamysteeri kirjoja 
- Käyttäjä voi suositella kirjoja muille käyttäjille
- Käyttäjä lähettää kaveripyynnön toiselle käyttäjälle


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
