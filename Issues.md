# TODO list

## FIXME
* Dissociate bg and text image, to add bg fade everywhere!, then fusion at diffusion
* PIPE FULL bug ?
* Sometime; Pipe not close on ctrl-c

## GFX
* add a function (wand api?) to print fixed chase text (metrix for max letter width and hop)

* random over text decoration  
  pl = Drawing()  
  print(len(pl.TEXT_DECORATION_TYPES)) //random over deco

## MINOR
* how import lib after args parsing (if missing depency lib --help doesn't work)

* debug mode over all functions

* Class pour la generation de text :
option sur les parametres : taille / style / uniforme_taille / uniforme_style / color ...

* Class pour la generation des tiles (img_gen) ?
x, y , align, ...

* Class pour les evolutions , avec un tirage au sort pour contredire'
- changement de couleur/taille progressif ~interpolation ...

* Take a look to python-img-generator loop



# Generator data sources
« cinq grands maux » / Five giants: pauvreté, insalubrité, maladie, ignorance, chomage.  William Beveridge (19e-20e)
Want (misère), Disease, Ignorance, Squalor (condition misérable) and Idleness
++++ ~pollution, liberté

voir ;Développement humain / Amartya Sen (20e)
le développement est désormais considéré par le Pr Sen comme un processus qui
supprime les principaux facteurs de blocage aux libertés tels la pauvreté, la
tyrannie, l’absence d’opportunités économiques, les conditions sociales précaires,
l’intolérance ou la répression autoritaire. 

** positive
*** creative commons
- wikipedia volume & freq modification - appli qui fait les bulles
https://fr.wikipedia.org/wiki/Sp%C3%A9cial:Statistiques
https://fr.wikipedia.org/wiki/Wikip%C3%A9dia:Statistiques
- public services / public invest
- temporary automomous zone
- us bank failed (weekly update on monday)- https://www.fdic.gov/bank/individual/failed/banklist.html
** negative
- stock market pluvalue (no downvalue counterside : market crash could not be totaly considered has 'goodnews')
https://www.euronext.com/pt-pt/reports-statistics/cash/daily-statistics
- cumul des emissions carbonne "cait climate data explorer 2015" / http://cait.wri.org
- qualite de l'air'
- flightradar24
- https://fr.flightaware.com/live/cancelled/today ou https://www.flightstats.com/v2/global-cancellations-and-delays [prendre last day pour etre sur de maj?]
- https://uk.flightaware.com/commercial/data/fuelprices - Feed samples
- https://wid.world/fr/donnees/ - Le Laboratoire sur les Inégalités Mondiales

--What data sources are available online?

# Issues
* Sometime; Pipe not close on `ctrl-c`
* Froze after some long time - (pipe full bug?) - mpv 0.6.2-2 / debian 8
