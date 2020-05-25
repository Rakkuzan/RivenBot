def weaponsList():
    weaponlist = []
    weaponlist.extend(weaponsPrimary())
    weaponlist.extend(weaponsSecondary())
    weaponlist.extend(weaponsMelee())
    return weaponlist

def weaponsPrimary():
    return [
        # S tier
        "Kuva Bramma",  # Very Common
        "Kohm",  # Very Common
        "Acceltra",  # Common
        # A tier
        "Rubico",  # Very Common
        "Ignis",  # Common
        "Fulmin",  # Common
        "Corinth",  # Common
        "Kuva Chakkhurr",  # Common
        "Vectis",  # Common
        "Kohm",  # Very Common
    ]

def weaponsSecondary():
    return [
        # S Tier
        "Nukor",  # Common
        "Catchmoon",  # Common
    ]

def weaponsMelee():
    return [
        # S Tier
        #  "Redeemer", # bugged
        "Kronen",
        "Gram",
        #  "Sepfahn", # bugged
        "Dokrahm",
        "Pennant",
    ]