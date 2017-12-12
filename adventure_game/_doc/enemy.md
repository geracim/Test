# Enemy
  Enemy defines a party of combatants that the player party will do battle with
  
# Enemy Property Listing

* "members" - the entities spawned on the team, keyed by display name (which must be unique)
   * "class" - the class of the combatant
   * "level" - the minimum and maximum level of this combatant
   * "spawnChance" (OPTIONAL) - the chance of this combatant appearing in battle
      * defaults to 100
   * "aiOverride" (OPTIONAL) - a specific ai this combatant will use, overriding all class based ai data
* "extraSpoils" - a list of item drops from this battle if victorious
   * to be added to the class drops of the combatants
   * "amount" (OPTIONAL) - min and max amount for each entry
      * defaults to [1, 1]
   * "chance" (OPTIONAL) - min and max percent chance for each amount of this drop
      * defaults to [100, 100]