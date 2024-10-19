# Terveyteni

Sovelluksessa voi keskustella terveydenhuollon kanssa ja saada tehtäviä/määräyksiä terveyden hoitoon liittyen.

- Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen. 
- Käyttäjä näkee sovelluksen etusivulla listan alueista missä hänellä on oikeus käydä.
- Käyttäjä voi luoda viestit alueelle uuden ketjun antamalla ketjun otsikon ja aloitusviestin.
- Käyttäjä voi voi täydentää/suorittaa tehtävän, sekä jatkaa vanhaa keskustelua.
- Käyttäjä voi muokata luomansa ketjun otsikkoa sekä lähettämänsä viestin sisältöä.
- Käyttäjä voi myös poistaa ketjun tai viestin.
- Käyttäjä voi tarkistella ja poistaa valmiiksi merkittyjä keskusteluja.
- Ylläpitäjä voi lisätä ja poistaa keskustelualueita jos hän on luonut keskustelun.
- Ylläpitäjä voi aktivoida määräyksiä/tehtäviä.
- Ylläpitäjä voi luoda salaisen alueen ja määrittää, kenellä käyttäjillä on pääsy alueelle.

## Tällähetkellä sovelluksessa toimii seuraavat asiat:
Sovellukseen voi kirjautua sisään ja ulos sekä luoda uuden käyttäjän. <br>
Keskustelun voi aloittaa ja toinen käyttäjä voi vasttata siihen. Käyttäjä voi poistaa viestin, muokata sitä, muokata otsikkoa sekä poistaa kseskustelun kokonaan.<br>
ylläpitäjä/läääkäri voi aktivoida tehtävän bmi ja nähdä tuloksen. käyttäjä potilas voi täydentää tehtävän ja nähdä tuloksen. <br>
Ylläpitäjä/lääkäri voi aloittaa yksityisen keskustelun potilaan kanssa joka näkyy ainoastaan lääkärin ja potilaan välillä.<br>
Keskustelun voi kuitata valmiiksi/jäädyttää, jolloin keskustelu on edelleen luettavissa ja omia viestejä voi poistaa(ylläpitäjä voi poistaa kaikkia), mutta niihin ei voi vastata.<br>
Lääkärin voi poistaa yksityis keskustelun kaikkia viestejä paitsi ensimmäisen viestin, potilas voi poistaa omia viestejä.<br>
Lääkäri voi kuitata yksityis keskustelun valmiiksi. Valmista keskustelua voi tarkistella jälkikäteen.

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

