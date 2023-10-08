# validation-rating-system

# Kuinka testata paikallisesti

Git kloonaa repo tietokoneellesi esim seuraavalla komennolla:

    git clone https://github.com/oivaaa/validation-rating-system.git

Siirry kloonattuun repoon cd-komennolla:

    cd validation-rating-system

ja sitten luo kloonatulle repolle uusi virtuaaliympäristö komennolla:

    python3 -m venv venv

Aktivoi virtuaaliympäristö komennolla:

    source venv/bin/activate

ja pip installoi tarvittavat paketit komennolla:

    pip install -r ./requirements.txt

Avaa postgres tulkki komennolla:
    
    psql

tai muulla tavallla ja 
luo uusi tietokanta, jotta omat samannimiset tietokanta taulut eivät menisi sekaisin (annetaan nimeksi valsystem):

    CREATE DATABASE "valsystem";

Poistu postgres tulkista ja palaa kloonattuun repoon. Aja seuraava komento uuden tietokannan skeeman määrittelemiseksi:

    psql -d valsystem < schema.sql


Luo git kloonattuun repoon uusi ".env"-niminen tidosto, johon lisäät tietokannan osoitteen ja salausavaimen seuraavasti:

    DATABASE_URL=postgresql:///valsystem
    SECRET_KEY=<sinun salausavain>
    
Lopuksi siirry takaisin git kloonattuun repoon jos et siellä valmiiksi ollut, ja käynnistä flask sovellus komennolla:

    flask run


**Huom(1)!** uuden salausavaimen voit luoda pythonissa seuraavasti:

**Huom(2)!** Jos tietokannan osoite ei toimi niin voit koittaa tarkempaa syntaksia kuten:






## Kyseessä on faktuaalisen tekstin arviointi sovellus, jossa käyttäjät voivat arvioida ja antaa palautetta tekstin laadusta
* Arvioitava teksti voi olla peräisen melkein mistä tahansa tekstipohjaisesta datasetistä (valitaan tarpeiden mukaan)
* Kuitenkin tekstin teema on hyvä valita siten, että käyttäjät pystyvät arvoimaan sitä
* Tesktin teemoja voisivat olla esim. historialliset tekstit päiväyksillä tai vaikka huonosti kirjoitetut reddit kommentit
* Käyttäjien antamien arviointejen ja luokittelun perusteella voidaan muodostaa tilastollisia tunnuslukuja tekstistä

### Välipalautus 2

Sovelluksen nykyinen tilanne on ihan hyvä. Jonkin verran vielä hiomista ja joidenkin asioiden muuttelemista tulee tapahtumaan. Sovellusta voi testata itse git clonaamalla ja luomalla olennaiset postgres tablet.  
