from typing import List, Sequence
import random
from collections import Counter


def is_full(dice: Sequence[int]) -> bool:
    """
    Vérifie si, parmi les dés, il est possible de former un full
    (un brelan d'une valeur et une paire d'une autre valeur).
    """
    counts = Counter(dice)
    for u, count_u in counts.items():
        if count_u >= 3:
            for v, count_v in counts.items():
                if v != u and count_v >= 2:
                    return True
    return False


def simulate_full(n_simulations: int) -> float:
    """
    Simule des parties visant à obtenir un full en 3 lancers.
    Stratégie heuristique :
    - Au premier lancer, si un full est obtenu, c'est gagné.
    - Sinon, on garde les dés faisant partie d'un brelan si présent, sinon une paire.
    - On relance les autres dés lors des lancers suivants.
    """
    successes: int = 0
    kept: List[int] = []

    for _ in range(n_simulations):
        kept = []  # dés conservés
        dice_to_roll: int = 5

        for roll_num in range(1, 4):
            # Lancer les dés non gardés
            roll = [random.randint(1, 6) for _ in range(dice_to_roll)]
            current = kept + roll

            # Vérifier immédiatement si l'objectif est atteint
            if is_full(current):
                successes += 1
                break

            # Stratégie pour choisir les dés à garder pour tenter d'obtenir un full
            counts = Counter(current)
            new_kept: List[int] = []

            triple_candidate: int | None = None
            pair_candidate: int | None = None

            # Rechercher un brelan
            for num, cnt in counts.items():
                if cnt >= 3:
                    triple_candidate = num
                    break
            if triple_candidate is not None:
                # Garder exactement trois dés de cette valeur
                new_kept.extend([triple_candidate] * 3)

            # Chercher une paire d'une autre valeur
            for num, cnt in counts.items():
                if num != triple_candidate and cnt >= 2:
                    pair_candidate = num
                    break
            if pair_candidate is not None:
                new_kept.extend([pair_candidate] * 2)

            # Si aucune combinaison n'est partiellement constituée, conserver au moins une paire s'il y en a
            if not new_kept:
                for num, cnt in counts.items():
                    if cnt >= 2:
                        new_kept.extend([num] * 2)
                        break

            # Mise à jour
            kept = new_kept
            dice_to_roll = 5 - len(kept)
            # Au dernier lancer, on relance tous les dés restants.
            if roll_num == 3:
                # On vérifie le résultat final (aucune autre action possible)
                final_dice = kept + roll
                if is_full(final_dice):
                    successes += 1

    return successes / n_simulations


def simulate_mini(n_simulations: int) -> float:
    """
    Simule des parties visant à obtenir un mini (somme des dés < 8) en 3 lancers.
    Stratégie heuristique :
    - Conserver à chaque lancer les dés qui affichent "1".
    - Au dernier lancer, tous les dés sont pris, puis on vérifie la somme.
    """
    successes: int = 0

    for _ in range(n_simulations):
        kept: List[int] = []
        dice_to_roll: int = 5

        for roll_num in range(1, 4):
            roll: List[int] = [random.randint(1, 6) for _ in range(dice_to_roll)]
            # Au dernier lancer, on accepte tous les dés
            if roll_num == 3:
                kept.extend(roll)
            else:
                # Garder les dés qui montrent 1
                for d in roll:
                    if d == 1:
                        kept.append(d)
                # Le reste sera relancé
            dice_to_roll = 5 - len(kept)

        if sum(kept) < 8:
            successes += 1

    return successes / n_simulations

if __name__ == "__main__":
    import time
    simulations = 10000000

    # Full simulation with timing
    start_time = time.time()
    pf = simulate_full(simulations)
    full_time = time.time() - start_time

    # Mini simulation with timing
    start_time = time.time()
    pm = simulate_mini(simulations)
    mini_time = time.time() - start_time

    print(f"Probabilité de full: {pf:.4f} (temps: {full_time:.2f}s)")
    print(f"Probabilité de mini (somme < 8): {pm:.4f} (temps: {mini_time:.2f}s)")
    print(f"Temps total: {full_time + mini_time:.2f}s")

    if pf < pm:
        print("Le full a moins de chance d'arriver que le mini.")
    elif pm < pf:
        print("Le mini a moins de chance d'arriver que le full.")
    else:
        print("Les chances sont approximativement égales.")
