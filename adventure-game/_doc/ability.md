# Abilities
  An ability is a possible action that may be taken during battle by an enemy.  All possible actions will ultimately work via ability.  Abilities may be learned by an combatant via leveling up their character class (such as magic spells), be granted by equipping a weapon (such as "fight"), applied by items (i.e. all types of consumable items like potions will reference an ability describing what they do), and more triggers may be introduced by plot/narrative as time goes on.

## Ability Property Listing
* "action" (OPTIONAL) - what to type in the player ability phase to use this.  
    * dot delimited chains can be used to construct sub-menus
* "description" - what is displayed if the user types "help" and then the action
* "charges" (OPTIONAL) - the number of times this ability may be used by an combatant
    * defaults to 0
    * 0 indicates it is not limited by ability specific charges
* "manaCost" (OPTIONAL) - the number of mana points consumed in using this ability
    * defaults to 9
* "skillPointCost" (OPTIONAL) - the number of skill points needed in this round to use the ability
    * defaults to 0
* "type" - the type key used by enemy armor solutions to determine damage multipliers
* "power" (OPTIONAL) - the minimum and maximum base power of the ability converted to damage
    * defaults to [0, 0]
    * this is the total damage in hit points done to a target, when no stats or modifiers, or type advantages are in place
    * two numbers specified will result in a random value between the two being chosen
    * 0, 0 implies an ability that does not deal damage as a primary effect
    * negative numbers should be used for abilities that heal targets
* "absorbPercent" (OPTIONAL) - a percentage (0-100) of the net applied damage to all targets to be returned to the caster as healing
    * defaults to 0
* "effectMask" - a list of effects that an combatant must have in order to be a valid target
    * generally, all games will need to define some effect similar to "alive" that most abilities will mask on
    * some abilities, such as revive, may mask on "dead" status rather than "alive"
    * masks lists like ["alive", "poisoned"] can also be used to specify things like antidotes only being usable on targets that are poisoned
* "group" - which battlefield entities constitute valid targets
    * self - can use this skill only on yourself
    * ally - can use this skill on anyone in your party except you (defaults to first ally)
    * party - can use this skill on anyone in your party (defaults to you)
    * enemy - can use this skill on an enemy (defaults to first enemy)
   all - can use this skill anywhere on the battlefield (defaults to first enemy)
* "target" - the number of targets this ability can effect simultaneously
    * single - targets only one combatant in the targetable group
    * distributable - defaults to targeting only one combatant, but can distribute power across the entire targetable group
    * all - targets all entities in the valid group
* "strikeWith"/"strikeAgainst" - multipliers added to the offense and defense check to augment the ability's base damage
    * this field is not optional, you must specify both lists, even if those lists are empty
    * strength, magic, defense, resist, hit, speed - uses combatant's current post-bonus stat
      * if your game defines other stats for all classes, they will also work
    * baseStrength, baseMagic, baseDefense, baseResist, baseHit, baseSpeed - uses combatant's current pre-bonus stat
      * if your game defines other stats for all classes, putting "base" in front of them will work
    * you can technically use "crit" or "evade" if you like, but since those are designed to center around 0 instead of 100, they will likely result in unwanted behavior
    * "TYPEADVANTAGE" - returns the composite advantage that the ability has against the target's armor type
    * "WEAPONPOWER" - returns the absolute power of the weapon initiating the ability
    * "WEAPONADVANTAGE" - returns the absolute power of the weapon multiplier by typeAdvantage minus target's armor
* "statModifiers" (OPTIONAL) - changes to the stats of the caster which will be added only during the casting of this ability
    * for example, having an ability that gives a { "speed" : 100 } will add 100% to the caster speed while using this skill, such as with pokemon's "quick attack"
* "canEvade" (OPTIONAL) - true/false value indicating whether the caster hit/target evade stats should be rolled
    * default false if not specified
    * when false, the hit/evade calculation will be skipped - meaning this ability can never miss; such as with pokemon's "swift", or pseudo-abilities, like a consumable item battleAbility
* "critPercent" (OPTIONAL) - the percent damage multiplier (should be over 100%) when a critical hit is achieved
    * defaults to zero, zero indicates an ability that does not use the critical system
* "casterEffects"/"targetEffects" (OPTIONAL) - a dictionary of possible effects applied to the casting/target combatant when the ability is used, mapped to each effects percent chance of appearing
* "classTransform" (OPTIONAL) - a heavy handed way to completely replace basically everything property of a combatant except their level and equipment during battle, like turning them into a chicken
    * "duration" (OPTIONAL) - a list with a min and max value for the turns this lasts
	   * defaults to [0, 0], which implies a permanent transformation
	* "priority" (OPTIONAL)
	   * defaults to 1
	   * this effects how multiple transforms interact.  For example, lets say "turn into chicken" (pri 2) and "turn into ghost" (pri 1) are transforms, each with a duration of 5 turns:
	      * if I turn someone into a ghost, and then a chicken, they will spend 5 turns as a chicken, and then 5 turns as a ghost, then back to normal
		  * if I turn someone into a chicken, and then a ghost, they will spend 5 turns as a ghost, then back to normal.  The higher ghost priority cancels the previous chicken transform
		  * transforms of the same priority always chain with each other.
