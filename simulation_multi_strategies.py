import random
from collections import Counter

def is_full(dice):
    """
    Vérifie si la liste 'dice' contient au moins un brelan d'un nombre
    et une paire d'un autre.
    """
    counts = Counter(dice)
    for num, cnt in counts.items():
        if cnt >= 3:
            for num2, cnt2 in counts.items():
                if num2 != num and cnt2 >= 2:
                    return True
    return False

def simulate_full_pairs(n_simulations):
    """
    Stratégie "Paires multiples" :
    - Premier lancer : on conserve 2 paires si possible, sinon une paire (0 ou 2 dés conservés).
    - Second lancer : on recalcule et on essaie de conserver 2 paires ou, si un brelan apparaît, on garde 3 dés.
    - Troisième lancer : on complète.
    """
    successes = 0

    for _ in range(n_simulations):
        kept = []
        success = False

        # Lancer 1
        dice_to_roll = 5 - len(kept)
        roll = [random.randint(1, 6) for _ in range(dice_to_roll)]
        current = kept + roll
        if is_full(current):
            successes += 1
            continue  # passage à la simulation suivante

        # Choix des paires
        cnt = Counter(current)
        pairs = [num for num, c in cnt.items() if c >= 2]
        # On conserve deux paires si possible, sinon une paire, sinon rien
        if len(pairs) >= 2:
            # On conserve exactement deux copies de deux nombres différents
            kept = [pairs[0]] * 2 + [pairs[1]] * 2
        elif len(pairs) == 1:
            kept = [pairs[0]] * 2
        else:
            kept = []

        # Lancer 2
        dice_to_roll = 5 - len(kept)
        roll = [random.randint(1, 6) for _ in range(dice_to_roll)]
        current = kept + roll
        if is_full(current):
            successes += 1
            continue

        # Mise à jour : si on obtient un brelan ou de nouvelles paires, on tente d'optimiser
        cnt = Counter(current)
        new_kept = []
        triple_found = None
        pair_found = None
        # Vérification d'un brelan
        for num, c in cnt.items():
            if c >= 3:
                triple_found = num
                break
        if triple_found is not None:
            new_kept.extend([triple_found] * 3)
        # Chercher une paire sur un autre nombre
        for num, c in cnt.items():
            if num != triple_found and c >= 2:
                pair_found = num
                break
        if pair_found is not None:
            new_kept.extend([pair_found] * 2)
        # Si aucune combinaison n'est complète, on essaie de conserver deux paires
        if not new_kept:
            pairs = [num for num, c in cnt.items() if c >= 2]
            if len(pairs) >= 2:
                new_kept = [pairs[0]] * 2 + [pairs[1]] * 2
            elif len(pairs) == 1:
                new_kept = [pairs[0]] * 2
        kept = new_kept

        # Lancer 3 : on relance les dés restants
        dice_to_roll = 5 - len(kept)
        roll = [random.randint(1, 6) for _ in range(dice_to_roll)]
        final = kept + roll
        if is_full(final):
            successes += 1

    return successes / n_simulations

def simulate_full_priority(n_simulations):
    """
    Stratégie "Priorité brelan" :
    - À chaque lancer, on identifie le nombre le plus fréquent (s'il apparaît au moins 2 fois)
      et on garde jusqu'à 3 exemplaires de ce nombre.
    - On relance les dés restants en espérant obtenir la paire complémentaire.
    """
    successes = 0

    for _ in range(n_simulations):
        kept = []
        candidate = None  # nombre choisi pour viser le brelan
        for roll_num in range(1, 4):
            dice_to_roll = 5 - len(kept)
            roll = [random.randint(1, 6) for _ in range(dice_to_roll)]
            current = kept + roll
            if is_full(current):
                successes += 1
                break

            cnt = Counter(current)
            # Choisir le nombre le plus fréquent (à condition d'avoir au moins 2 exemplaires)
            candidate, freq = None, 0
            for num, c in cnt.items():
                if c >= 2 and c > freq:
                    candidate, freq = num, c

            # Si un candidat est trouvé, on garde jusqu'à 3 exemplaires de celui-ci
            if candidate is not None:
                kept = [candidate] * min(cnt[candidate], 3)
            else:
                kept = []
            # On ne conserve rien d'autre ; on espère obtenir la paire sur un nombre différent au prochain lancer.

            # Dernier lancer : on ajoute tous les dés et cela pourrait former le full
            if roll_num == 3:
                final = kept + roll
                if is_full(final):
                    successes += 1
    return successes / n_simulations


def simulate_mini_basse(n_simulations):
    """
    Stratégie "Basse valeur conservée" :
    - Pour les 2 premiers lancers, on conserve les dés faibles (1 et 2)
      si la somme cumulée reste raisonnable.
    - Au dernier lancer, on complète et on vérifie que la somme < 8.
    """
    successes = 0

    for _ in range(n_simulations):
        kept = []
        # Lancers 1 et 2
        for roll_num in range(1, 3):
            dice_to_roll = 5 - len(kept)
            roll = [random.randint(1, 6) for _ in range(dice_to_roll)]
            # Conserver 1 et 2 si cela ne fait pas dépasser un seuil
            for d in roll:
                if d in [1, 2]:
                    # On conserve le dé si la somme actuelle plus d'ajouter ce dé reste raisonnable.
                    if sum(kept) + d <= 7:
                        kept.append(d)
            # On passe au lancer suivant en relançant les dés non gardés.
        # Lancer 3 : on prend tous les dés restants
        dice_to_roll = 5 - len(kept)
        final_roll = [random.randint(1, 6) for _ in range(dice_to_roll)]
        final = kept + final_roll
        if sum(final) < 8:
            successes += 1

    return successes / n_simulations

def simulate_mini_minimisation(n_simulations):
    """
    Stratégie "Minimisation progressive" :
    - À chaque lancer (sauf le dernier), on conserve les 1 et 2.
    - On conserve également un 3 si la somme actuelle + 3 reste ≤ 7.
    - Au dernier lancer, on complète avec tous les dés restants.
    """
    successes = 0

    for _ in range(n_simulations):
        kept = []
        for roll_num in range(1, 3):
            dice_to_roll = 5 - len(kept)
            roll = [random.randint(1, 6) for _ in range(dice_to_roll)]
            for d in roll:
                if d <= 2:
                    kept.append(d)
                elif d == 3 and (sum(kept) + 3) <= 7:
                    kept.append(d)
        dice_to_roll = 5 - len(kept)
        final_roll = [random.randint(1, 6) for _ in range(dice_to_roll)]
        final = kept + final_roll
        if sum(final) < 8:
            successes += 1

    return successes / n_simulations

if __name__ == "__main__":
    simulations = 10000000

    print("----- full -----")
    pf_pairs = simulate_full_pairs(simulations)
    pf_priority = simulate_full_priority(simulations)
    print(f"Stratégie Paires multiples : {pf_pairs:.4f}")
    print(f"Stratégie Priorité brelan : {pf_priority:.4f}")

    print("\n----- mini (somme < 8) -----")
    pm_basse = simulate_mini_basse(simulations)
    pm_minimisation = simulate_mini_minimisation(simulations)
    print(f"Stratégie Basse valeur conservée : {pm_basse:.4f}")
    print(f"Stratégie Minimisation progressive : {pm_minimisation:.4f}")
