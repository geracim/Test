# Items
  items constitute and shared collectable anythings in the party.  These need not necessarily be true "items".  Some may be consumable items or equippable things.  Others may be quest specific items,  Currency and achievements can also be represented by the item system, and placed in categories that keep them out of the "usable" inventory.  Similarly, "hidden" item categories could be a general purpose way to track non-linear player progress.  For example, a side quest could give a player a secret "complimentedMedusasHair" item or something that might inject some fluffy bullshit into the game's ending sequence.

## Item Property Listing

* "description" - text shown when typing "help {itemName}" in the battle selection menu
    * probably also in equip screens and shops, if and when we get to that
* "category" - which type of item this is. 
    * The battle system will only surface the existence of items listed in the "battleItemCategory" in battle.json.
    * All equipment and consumable items should probably be in the same main category
    * As mentioned before, other examples of categories could be currencies, non-usable directly usable quest items like "zelda's letter", achievements, tallies of how in love with you your party members are... whatever.
* "battleAbility" (OPTIONAL) - an ability that this item triggers when used in battle
    * causes this item to appear in battle as an option for all party members under the "item" category
    * intended for potions, etc
* "consumable" (OPTIONAL) - whether or not this item is consumed when used in battle
    * defaults to false
    * only matters right now for items with a battleAbility
    * Example 1: a potion would be consumable, and have a battle ability.  you use one up in battle and it does a thing
    * Example 2: the gen 1 pokeflute would havea battle ability, but would not be consumable
    * Example 3: a rare candy would be consumable but would not have a battle ability.  instead it would probably have a menuAbility, or something like that when we add more menus/game dynamics
* "equipSlot" (OPTIONAL) - which of the slots defined in config.json's "equipSlots" this item can be equipped to
    * When not specified, this item cannot be equipped
* "equipClassMask" (OPTIONAL) - a list of classes that can equip this item
    * This only matters for items with an equip slot
    * If blank, any class can equip it
* "equipGrantAbility" (OPTIONAL) - a list of abilities the user can use when this item is equipped
    * All items intended as weapons should probably grant some ability that is surfaced with an action like "fight" or "attack".  That way, we can specify all weapons using the existing ability system, which means that weapons need not just do damage.  we can have thigns like healing rods.  Also, this will set it up so if you have no weapons equiped, the "fight" option will automatically disappear
  
* "power" (OPTIONAL) - min and max power value
    * defaults to [0, 0]
    * intended for itmes that act as weapons when equipped.  power will only be used for the abilities listed under "equipGrantAbility"
    * abilities using "weaponAdvantage" or "weaponPower" strikes will use this value as a multiplier on the ability's base power
    * if different numbers specified, the applied multiplier will be randomly select from the range - allowing for weapons that do inconsistent damage
* "protection" (OPTIONAL) - reduces the damage of abilities using the "weaponAdvantage" strike parameter
    * defaults to 0
    * penalty surface against an attacker's abilitypower*itempower*typeEffectiveness when using the "weaponAdvantage" metric
    * intended for items that act as armor when equipped
* "typeEffectiveness" (OPTIONAL) - specifies a damage multiplier by type when equipped, used to increase (or decrease) vulnerability against various ability types
    * 100: no effect, <100: this element hurts people with this armor less, >100: this element hurts people with this armor more 
    * intended for items that act as armor when equipped
* "applyEffects" (OPTIONAL)
    * when this item is equipped, this effect will be innately present at all times
	   * this could be used for things like fire-absorb armor
	* when this item is triggered via battleAbility, these effects are immediately added to the item's target(s)
	   * potions of long term regeneration could be implemented this way, for example
* "suppressEffects" (OPTIONAL)
    * when this item is equipped, it prevents these effects from being applied to the combatant.  Can be used to make poison resist rings, etc.
    * when this item is triggered via battleAbility, these effects are immediately removed from the item's target(s)
* "max" (OPTIONAL) - the maximum number of this item you can hold at a time
    * defaults to 1
* "value" (OPTIONAL) - the base market cost of this item, in other items (for example currency)
    * THIS IS NOT USED BY THE BATTLE SYSTEM
    * but I thought i'd include it to demonstrate how this kind of thing might work, and how to make another category like currency interact with equippable items.