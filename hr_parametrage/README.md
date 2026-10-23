# Module hr_anciennete

## Installation

1. Copier le dossier `hr_anciennete` dans votre répertoire `custom-addons`
2. Redémarrer Odoo : `sudo service odoo restart`
3. Activer le mode développeur (Settings > Activer le mode développeur)
4. Aller dans Apps > Mettre à jour la liste des apps
5. Rechercher "Barème Ancienneté" et cliquer sur **Installer**

## Accès dans l'interface

```
Menu : Paie > Configuration > Barèmes > Ancienneté
```

Les 6 tranches du barème sont pré-configurées automatiquement à l'installation.

## Utilisation dans une règle salariale

Dans le code Python de votre règle salariale (ex: Prime d'Ancienneté) :

```python
# Calcul de l'ancienneté en années
anciennete = (payslip.date_to - contract.date_start).days / 365.0

# Lecture dynamique du barème configuré manuellement
taux = env['hr.anciennete'].get_taux_for_anciennete(anciennete)

# Résultat
result = contract.wage * taux
```

## Barème par défaut

| Début (années) | Fin (années) | Taux  |
|---------------|-------------|-------|
| 0             | 2           | 0 %   |
| 2             | 5           | 5 %   |
| 5             | 12          | 10 %  |
| 12            | 20          | 15 %  |
| 20            | 25          | 20 %  |
| 25            | 60          | 25 %  |

Ces données peuvent être modifiées directement depuis l'interface Odoo.

## Droits d'accès

- **Utilisateur Paie** : lecture seule
- **Responsable Paie** : lecture, écriture, création, suppression
