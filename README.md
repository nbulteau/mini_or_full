# mini_or_full

## simulation_simple_strategy.py

Un programme Python qui simule des parties selon une stratégie heuristique pour chacun des objectifs. Ce code propose deux fonctions de simulation : une pour le full et une pour le mini (la somme des dés inférieure à 8).

simulate_full :
À chaque tour, on lance le nombre de dés non gardés. On vérifie si le total (dés gardés et récemment lancés) forme un full. Ensuite, on conserve les dés qui font partie d’un brelan (ou, à défaut, une paire) pour améliorer les chances au prochain lancer.

simulate_mini :
À chaque lancer, on conserve les dés montrant 1 car ils favorisent d’obtenir une somme faible. Au dernier lancer, tous les dés sont ajoutés et ensuite on vérifie si la somme est inférieure à 8.

La stratégie utilisée est simplifiée et heuristique. Elle n’est pas nécessairement optimale, mais permet d’illustrer la simulation avec 3 lancers et la possibilité de conserver certains dés.

L'approche est Monte Carlo : les probabilités sont estimées en répétant un grand nombre de fois les simulations et en calculant le ratio succès/total.

La classe Counter est utilisée pour compter efficacement les occurrences de chaque valeur dans les dés.

## Counter
`Counter` est une classe de la bibliothèque standard Python `collections` qui permet de compter facilement les occurrences d'éléments dans une séquence. Dans ce programme, elle est utilisée pour compter combien de fois chaque valeur de dé apparaît.

Voici un exemple concret avec le code :

```python
from collections import Counter

# Pour les dés [1, 1, 1, 2, 2]
dice = [1, 1, 1, 2, 2]
counts = Counter(dice)
# Résultat : Counter({1: 3, 2: 2})
# - La clé 1 a une valeur de 3 (trois dés montrant 1)
# - La clé 2 a une valeur de 2 (deux dés montrant 2)
```
Dans le programme, `Counter` est principalement utilisé pour :

1. Détecter un full dans la fonction `is_full()` :
   - Compte les occurrences de chaque valeur
   - Vérifie s'il existe une valeur avec 3 occurrences (brelan) et une autre avec 2 occurrences (paire)

2. Dans les stratégies de jeu pour :
   - Identifier les brelans (valeurs apparaissant 3 fois ou plus)
   - Identifier les paires (valeurs apparaissant 2 fois ou plus)
   - Optimiser la conservation des dés entre les lancers

### Exemple de sortie

Pour 1 000 000 parties simulées, on obtient les résultats suivants :

```bash
python main.py 
Probabilité de full: 0.2324
Probabilité de mini (somme < 8): 0.0599
Le mini a moins de chance d'arriver que le full.
```

## simulation_multi_strategies.py

Ce script implémente et compare plusieurs stratégies pour les objectifs du full et du mini.

### Stratégies Full

1. **Stratégie des Paires Multiples** (`simulate_full_pairs`) :
   - Premier lancer : Conservation de deux paires si possible, sinon une paire
   - Deuxième lancer : Réévaluation des paires ou passage à un brelan si détecté
   - Troisième lancer : Complétion avec les dés restants

2. **Stratégie Priorité Brelan** (`simulate_full_priority`) :
   - À chaque lancer : Identification du nombre le plus fréquent (s'il apparaît au moins deux fois)
   - Conservation de jusqu'à trois exemplaires de ce nombre
   - Relance des dés restants pour obtenir la paire complémentaire

### Stratégies Mini (Somme < 8)

1. **Stratégie Valeurs Basses** (`simulate_mini_basse`) :
   - Deux premiers lancers : Conservation des 1 et 2 si la somme reste acceptable
   - Dernier lancer : Complétion avec les dés restants et vérification somme < 8

2. **Stratégie Minimisation Progressive** (`simulate_mini_minimisation`) :
   - Deux premiers lancers : Conservation systématique des 1 et 2
   - Conservation des 3 si somme actuelle + 3 ≤ 7
   - Dernier lancer : Complétion avec les dés restants

### Exemple de sortie

Pour 1 000 000 parties simulées :

```bash
----- full -----
Stratégie Paires multiples : 0.2647
Stratégie Priorité brelan : 0.2317

----- mini (somme < 8) -----
Stratégie Basse valeur conservée : 0.0938
Stratégie Minimisation progressive : 0.0500
