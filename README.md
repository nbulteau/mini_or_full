# mini_or_full
Un programme Python qui simule des parties selon une stratégie heuristique pour chacun des objectifs. Ce code propose deux fonctions de simulation : une pour le full (full house) et une pour le mini (la somme des dés inférieure à 8).

simulate_full_house :
À chaque tour, on lance le nombre de dés non gardés. On vérifie si le total (dés gardés et récemment lancés) forme un full house. Ensuite, on conserve les dés qui font partie d’un brelan (ou, à défaut, une paire) pour améliorer les chances au prochain lancer.

simulate_mini :
À chaque lancer, on conserve les dés montrant 1 car ils favorisent d’obtenir une somme faible. Au dernier lancer, tous les dés sont ajoutés et ensuite on vérifie si la somme est inférieure à 8.


## Installation

```bash
git clone
```

## Utilisation

```bash
python main.py 1000
```

## Exemple de sortie

Pour 1000000 parties simulées, on obtient les résultats suivants :

```bash
python main.py 
Probabilité de full: 0.2324
Probabilité de mini (somme < 8): 0.0599
Le mini a moins de chance d'arriver que le full.
```
## Notes
La stratégie utilisée est simplifiée et heuristique. Elle n’est pas nécessairement optimale, mais permet d’illustrer la simulation avec 3 lancers et la possibilité de conserver certains dés.