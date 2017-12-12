# Effects
  An effect is a property that can be applied to an combatant on the battlefield.  These effects will be used for all contextual changes in an entities capability and viability.  Some effects will be directly visible and parseable things, like "poison", or "sleep".  Other effects will be used by the low level battle system (for example, all games will need to define some sort of "alive" and "dead" effect that the system will use to determine when battle ends and who wins).  Other effects may be hidden, for example an ability like pokemon's "tail whip" could work by applying a "defenseDown" status to an combatant, that could be specified to stack up to 5 times.

## Effect Property Listing 
* "display" (OPTIONAL) - the text that displays next to an combatant with this effect.  
    * Not all effects need to have displays, things like "alive" for example can be hidden
* "onPerformApplied" (OPTIONAL) - the performance text displayed by the battle system when this effect is given to someone
    * This is also options, but can help give feedback on effects that the user is supposed to be aware of, like poison or sleep, or death
* "duration" (OPTIONAL) - a minimum and maximum number of turns this effect lasts before going away
    * defaults to [0, 0]. a duration of [0, 0] implies that the effect will not go away on its own 
    * the actual duration of the effect will be chosen when it is applied to an combatant
* "statModifiers" (OPTIONAL) - a dictionary of stats and their changes, that will be applied to the combatant that has this effect
* "healthPerTurn" (OPTIONAL) - used to make an ability effect change health each turn
    * "points" specifies a base number added to an combatant with this status
    * "percent" specifies a percentage of the combatant's max health added to it each turn
    * this can be used to implement explicit poison type effects
    * this can also be used with hidden effects to create things like armor with life regeneration
* "manaPerTurn" (OPTIONAL) - used to make an ability effect change mana each turn
    * "points" specifies a base number added to an combatant with this status
    * "percent" specifies a percentage of the combatant's max mana added to it each turn
* "stack" (OPTIONAL) - how many times this effect can be stacked on a target
    * defaults to 1
    * most effects should probably not stack, but things like a "defenseDown" applied from tail whip type skills will stack multiple small statModifiers together
* "abilityAdd" (OPTIONAL) - adds new abilities to anyone who recieves this status
* "abilityBlock" (OPTIONAL) - abilities that cannot be used when this status effect is present
* "abilityReplace" (OPTIONAL) - a map of abilities that if present on someone with this effect, will be replaced with other abilities
* "actionBlock" (OPTIONAL) - a list of actions that an combatant cannot do while this effect is present
    * THESE ARE NOT ABILITIES, but action queues.  i.e. "fight" would block any ability that us accessed via the "fight" action
    * these can be specific skills, like "skill.ice1", or top level menus like "fight"
    * this can be used to silence magic, prevent attacks, or more esoteric things like preventing running away
    * "ALL" can be specified to completely disable an combatant (for example, for use with the "dead" effect)
* "suppressEffects" (OPTIONAL) - a list of other effects that this effect will negate
    * this allows a status effect when applied, to cancel out other status effects.
    * for example "dead" might cancel "alive"
* "visibility" (OPTIONAL) - specifies whether a target should be visible on the battlefield (i.e. whether their name appears) as a member of either the party or enemy team
    * For now i expect that this will only be used by the game's "alive" effect - so that all living enemies are visible, and the "dead" effect, which may for example show dead party members, but not dead enemies
    * this could also be used to create invisibility skills for enemies, etc
* "interrupt" (OPTIONAL) - an ability or special key that will instantly cause this effect to vanish
    * "DAMAGE" - any applied damage will cancel this effect, useful for things like final fantasy style "sleep"
* "strikeTypeDamageMultipliers" (OPTIONAL) - a map of damage multipliers applied post-bonus to abilities used of a certain type
    * "ALL" will cause this multiplier to be applied to all damage
* "againstTypeDamageMultipliers" (OPTIONAL) - a map of damage multipliers applied post-bonus when attacked by abilities of a certain type
    * innate status effects on classes could use this to build pokemon style type advantages
	* a piece of armor could have a "-100" multiplier to a type, to implement damage absorb
	* "ALL" will cause this multiplier to be applied to all damage
* "reflectTypeDamageMultipliers" (OPTIONAL) - a map of damage multipliers applied post-bonus to ability casters
    * this can be used to implement things like "thorns" auras, that return damage to the attacker for certain types
	* "ALL" will cause this multiplier to be applied to all damage
* "reflectEffects" (OPTIONAL) - a list of effects if when attempted to be applied to someone with this effect are returned to the caster instead
