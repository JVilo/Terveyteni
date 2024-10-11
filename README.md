# Omaterveys

Sovelluksessa voi keskustella terveydenhuollon kanssa ja saada tehtäviä/määräyksiä terveyden hoitoon liittyen.

- Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen. 
- Käyttäjä näkee sovelluksen etusivulla listan alueista missä hänellä on oikeus käydä.
- Käyttäjä voi luoda viestit alueelle uuden ketjun antamalla ketjun otsikon ja aloitusviestin sisällön.
- Käyttäjä voi voi merkitä tehtävän/määräyksen tehdyksi, sekä jatkaa vanhaa keskustelua.
- Käyttäjä voi muokata luomansa ketjun otsikkoa sekä lähettämänsä viestin sisältöä.
- Käyttäjä voi myös poistaa ketjun tai viestin.
- Käyttäjä voi tarkistella ja poistaa valmiiksi merkittyjä keskusteluja.
- Ylläpitäjä voi lisätä ja poistaa keskustelualueita.
- Ylläpitäjä voi luoda määräyksiä/tehtäviä.
- Ylläpitäjä voi luoda salaisen alueen ja määrittää, keillä käyttäjillä on pääsy alueelle.

## Tällähetkellä sovelluksessa toimii seuraavat asiat:
Sovellukseen voi kirjautua sisään ja ulos sekä luoda uuden käyttäjän. <br>
Keskustelun voi aloittaa ja toinen käyttäjä voi vasttata siihen. Käyttäjä voi poistaa viestin, muokata sitä, muokata otsikkoa sekä poistaa kseskustelun kokonaan.<br>
ylläpitäjä/läääkäri voi aktivoida tehtävän bmi ja nähdä tuloksen. käyttäjä potilas voi täydentää tehtävän ja nähdä tuloksen. <br>
Ylläpitäjä/lääkäri voi aloittaa yksityisen keskustelun potilaan kanssa joka näkyy ainoastaan lääkärin ja potilaan välillä.<br>
Lääkärin ja potilaan välistä keskustelua ei voi vielä postaa millään tapaa.

## sovelluksen käynnistäminen:
1. Sovellusta voi testata ainoastaan paikallisesti omalla koneella.<br>
<br>
2. requirements.txt tiedostosta löytyy tarvittavat riippuvuudet, jotka on syytä asentaa.<br>
<br>
3. db.py tiedostosta löytyy kohta -- app.config["SQLALCHEMY_DATABASE_URI"] , johon osoitteeksi kannattaa laittaa itselleen omaan tietokantaan sopiva osoite.<br>
<br>
4. SECRET_KEY on syytä muodostaa .env tiedostoon. esim. mallia SECRET_KEY=123, muuten ei kirjautuminen onnistu.<br>
   (Itse olen käyttänyt sovelluksen tekoon dockeria jolloin bd.py tiedostossa on myös osa joka luo minulle sql taulukot automaattisesti. Dockerin pitäisi käynnistyä komennolla: docker compose up -d.
db.py koodi rivit 11-20 ovat turhia jos käytät koneelle asennettua psql tietokantaa.)<br>
<br>
5. Luo taulukot psqllään schema.sql tiedostosta.<br>
<br>
6. Flask run pitäisi käynnistää sovelluksen.<br>

