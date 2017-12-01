The battle system will be activated with two lists of entities called "party", and "enemy"
   * Each combatant must define a a display name, a class, a level, a list of equipment, and a list of item rewards

# Battle Phases

## The Introduction

* The battle system will display introductory text, telling the player they are being attacked.
* The battlefield will be laid out in the ui, showing all visible entities
* this phase will run on a timer, dropping automatically to the next phase when expired

## Player ability menu

* The player will be presented with all top-level  abilities for an combatant in the party
  * If the combatant has no available actions (i.e.  if a status effect blocks all actions) it will  be skipped
  * All typing options will be listed to the player
  * Some options (for example "item") may present  a sub-menu of sub options
  * The player can type "help" on all options to  get a description
  * The player may type "back" to return to the  previous level menu
* specifying an ability may ask the player to  specify a target
  * If only one valid target is available for the  action, this step will be skipped
  * Abilities will also store any availble  fallback targets (i.e. other valid targets that  were not selected)
  * typing "back" will return to the previous  selection menu 
* When the player selects an ability and target, the top level ability list for the next party member will open

## Enemy ai decision

* All non-player controlled entities on the field  will select their battle abilities and targets  based on their ai configuration and the state of  the battle field
* This process, while at times rather complicated, will be instantaneous from the end user perspective, and as such has no ui/ux concerns

## Battle model update

* All selected combatant abilities will be sorted  according to the speed of the combatant and ability.
* The resulting state changes for each ability  will be applied in order
  * If an combatant's desired target is no longer  present, it will instead use the ability on the  next listed fallback target
  * If an combatant is not able to perform their  ability at all (either because all available  targets are dead, or because it has aquired a  status effect during the model update that  prevents it)
  * Each successfully performed ability will push  a performance node to the performer for the  acting combatant
  * The attack will cycle through each target,  checking the hit/evade ratio to select for  misses and hits
    * on miss, this target will no have its model  effected, and a "miss" performance node will  be added to the performer for the target combatant
  * Health deltas will be applied according to the  ability, and will be capped between 0 and the  target's max hitpoints
    * health deltas will take into account the  power range, strike with/against ratios
    * in the case of a critical hit roll (for  applicable abilities) the final damage will be  multiplied and a critical hit performance node  will be added for the target combatant
    * The health delta will be applied to the  performance node for the target combatant
    * if the ability has an absorb ratio, the  stolen health will be applied to the acting  combatant, and a performance node to show that  health delta will be shown
  * status effect deltas will be pushed to the  combatant according to the ability
  * If any target's health hits zero, the status  effect listed under "applyWhenHealthExhausted"  will be applied as a delta to it
  * the absolute status effect deltas over the course of the ability eval will be pushed to the performance node for the effected entities

## Performer update

* Each queued performance noce will be executed in  turn
* A performance node will consist of the console  saying "X has used Y [on Z]" which will be  displayed on a timer
* The performance node may describe damage being done to the enemies, and status effects applied

## Defeat check

* The game will validate that at least one member of the party has the status effect listed under "teamLosesWithoutAnyone"
* if this check fails, a defeat message will be displayed on a timer, dynamicState.battle_result will be tagged "defeat", and the battle state will close
* if the check passes, the next phase will be triggered

## Victory check

* The game will validate that at least one member  of the enemy has the status effect listed under  "teamLosesWithoutAnyone"
* if this check passes, the game will cycle back  to the PlayerAbilityMenu phase
* if this check fails, the next phase will be triggered

## Spoils phase

* the experience from each enemy with the status "spoilsAwardedFor" will be evenly distributed between all party members not exhibiting the "gainExperienceIf" status
* any party members who's experience has crossed a level-up threshold will present level-up message, displaying all stat changes and new skills learned
* any member of the enemy with the status "spoilsAwardedFor" will add their item rewards to the player's inventory.


# Internal Battle Sub-calculatons

### Global
* battle_duration
   * How long the battle has lasted
* shsw_duration
   * How much longer this battle is estimated to last in rounds 
   * (if all combatants from now on acted as 100% smart/healer/survivor/winners)

### Per Team
* shsw_result
   * How much total health our team will still have at the end of this battle
      * A negative number implies our team expects to lose, and the enemy team will have this much
   * (if all combatants from now on acted as 100% smart/healer/survivor/winners)
* sah_party_power_estimate
   * The total amount of damage your party would apply the next turn
* sah_party_overpower_estimate
   * The total amount of damage your party would apply, minus the total amount of damage the enemy party would apply next turn
   * (if all combatants acted as a 100% smart/harming/assassins)
   
### Per Combatant
* effects
   * A list of active effect ids, attached to the number of turns until they deactivate (0, if infinite)
* transforms
   * A list of class transformation ids, attached to the number of turns until they deactivate (0, if infinite)
* agro_damages
   * A dictionary of the total damage that has been applied to this combatant listed by the names of other combatants
* pattern_index
   * For ai's utilizing an attack pattern, this is the numeric index of the next ability to use in the chain