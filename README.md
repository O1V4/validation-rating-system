# validation-rating-system

## Kuinka testata paikallisesti

Git kloonaa repo tietokoneellesi esim seuraavalla komennolla:

    git clone https://github.com/oivaaa/validation-rating-system.git

Siirry kloonattuun repoon cd-komennolla:

    cd validation-rating-system

ja sitten luo kloonatulle repolle uusi virtuaaliympäristö:

    python3 -m venv venv

Aktivoi luotu virtuaaliympäristö:

    source venv/bin/activate

ja pip installoi tarvittavat paketit:

    pip install -r requirements.txt

Käynnistä postgres tulkki:
    
    psql

tai muulla tavalla ja 
luo uusi tietokanta, jotta omat samannimiset taulut eivät menisi sekaisin (annetaan nimeksi valsystem):

    CREATE DATABASE "valsystem";

Poistu postgres tulkista ja palaa kloonattuun repoon. Aja seuraava komento uuden tietokannan skeeman määrittelemiseksi:

    psql -d valsystem < schema.sql


Luo kloonattuun repoon uusi ".env"-niminen tiedosto, johon lisäät tietokannan osoitteen ja salausavaimen seuraavasti:

    touch .env
    echo "DATABASE_URL=postgresql:///valsystem" >> .env
    echo "SECRET_KEY=<sinun salausavain>" >> .env 
    
Lopuksi siirry takaisin git kloonattuun repoon jos et ollut siellä valmiiksi, ja käynnistä flask sovellus komennolla:

    flask run


**Huom(1)!** Uuden salausavaimen voit luoda python3 tulkissa seuraavasti terminaalia käyttäen.
Avaa tulkki:

    python3

Generoi salausavain:

    import secrets
    secrets.token_hex(16)

**Huom(2)!** Jos tietokannan osoite ei toimi niin voit koittaa tarkempaa formaattia osoiteelle (tämä vaatii, että olet määrittänyt salasanan postgres käyttäjälle), kuten:

    DATABASE_URL=postgresql://postgres:<salasana>@localhost/valsystem

**Huom(3)!** Jos postgres tulkin käynnistys ei onnistu niin vaihda ensin postgres käyttäjään ja sitten yritä käynnistää tulkki. Tämä onnistuu komennoilla:

    sudo -i -u postgres
    psql


#### Kyseessä on faktuaalisen tekstin arviointi sovellus, jossa käyttäjät voivat arvioida ja antaa palautetta tekstin laadusta
* Arvioitava teksti voi olla peräisen melkein mistä tahansa tekstipohjaisesta datasetistä (valitaan tarpeiden mukaan)
* Kuitenkin tekstin teema on hyvä valita siten, että käyttäjät pystyvät arvoimaan sitä
* Tesktin teemoja voisivat olla esim. historialliset tekstit päiväyksillä tai vaikka huonosti kirjoitetut reddit kommentit
* Käyttäjien antamien arviointejen ja luokittelun perusteella voidaan muodostaa tilastollisia tunnuslukuja tekstistä

#### Välipalautus

Sovelluksen nykyinen tilanne on ihan hyvä, mutta sovellus vaatii jonkin verran hiomista ja joidenkin asioiden muuttamista/lisäämistä. Sovelluksen ulkoasu on hyvässä jamassa, mutta jotakin funktionaalisuutta voisi vielä lisätä. Ylempänä on tarkat ohjeet sovelluksen testaamiseen.
