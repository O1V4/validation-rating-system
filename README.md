# Validation-rating-system app in Finnish
# Anonyymi palautteenanto systeemi

## Kuinka testata paikallisesti (tarvitset Postgres tietokannan)

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


### Lopullinen sovellus

![Screenshot from 2023-10-22 21-10-47](https://github.com/oivaaa/validation-rating-system/assets/72695556/34e3705a-3d82-4a1d-b33e-8158acafb723)

#### Kyseessä on anonyymi faktuaalisen tekstin arviointi sovellus, jossa käyttäjät voivat arvioida ja antaa palautetta tekstin laadusta sekä lähettää uusia tekstejä

* Arvioitava teksti voi olla peräisen melkein mistä tahansa tekstityypistä tai -lajista (valitaan tarpeiden mukaan)
* Kuitenkin tekstin teema on hyvä valita siten, että toiset käyttäjät pystyvät arvoimaan sen faktuaalisuutta ja laatua
* Tekstin teemoja voisivat olla esim. historialliset tekstit päiväyksillä tai vaikka huonosti kirjoitetut reddit kommentit
* Käyttäjät pystyvät antamaan toisten käyttäjien teksteille arvosanoja ja arviointeja/palautetta sekä lisämään omia tekstejä
* Käyttäjien antamien arvosanojen perusteella teksteistä muodostetaan tilastollisia tunnuslukuja
* HUOM!: Arvosteluja tietylle tekstille täytyy olla vähintään kolmelta eri käyttäjältä, jotta pystyt huomaamaan keskimääräisen ja mediaani arvion välillä eron
* Ylempänä on tarkat ohjeet sovelluksen testaamiseen

