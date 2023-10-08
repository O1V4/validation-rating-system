# validation-rating-system

## Kuinka testata paikallisesti

git kloonaa repo tietokoneelle esim seuraavalla komennolla:

    git clone https://github.com/oivaaa/validation-rating-system.git


## Kyseessä on faktuaalisen tekstin arviointi sovellus, jossa käyttäjät voivat arvioida ja antaa palautetta tekstin laadusta
* Arvioitava teksti voi olla peräisen melkein mistä tahansa tekstipohjaisesta datasetistä (valitaan tarpeiden mukaan)
* Kuitenkin tekstin teema on hyvä valita siten, että käyttäjät pystyvät arvoimaan sitä
* Tesktin teemoja voisivat olla esim. historialliset tekstit päiväyksillä tai vaikka huonosti kirjoitetut reddit kommentit
* Käyttäjien antamien arviointejen ja luokittelun perusteella voidaan muodostaa tilastollisia tunnuslukuja tekstistä

### Välipalautus 2

Sovelluksen nykyinen tilanne on ihan hyvä. Jonkin verran vielä hiomista ja joidenkin asioiden muuttelemista tulee tapahtumaan. Sovellusta voi testata itse git clonaamalla ja luomalla olennaiset postgres tablet.  
