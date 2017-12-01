# Ai
  Ai defines how a computer controlled character selects abilities and targets during battle
  
## Ai Property Listing

* "intelligence" - percentage, between 0 and 100
   * how often this ai "thinks through" their choices.
   * An intelligence 0 combatant will always randomly select from their available actions and the targets for those actions with no forethought
   * An intelligence 100 combatant will always use the ai system to make a choice that fits their idea of "smart"
   * An intelligence 25 combatant will make an informed decision a quarter of the time, and act randomly otherwise
   * An intelligence 100 combatant with no other traits will still be completely random, as it won't know how to define the smartness of moves
   
* "winning" (OPTIONAL) - weighting, expected to be 0 to 100, but doesn't have to be
   * Weights the smartness of each available action by the immediate total absolute damage that action will distribute across the opposing team
   * "winning" ais will prefer a spell that deals 25 damage to 4 enemies, over a spell that deals 50 to one
 
* "harming" (OPTIONAL) - weighting, expected to be 0 to 100, but doesn't have to be
   * Weights the smartness of each available action by the highest total damage it could apply to an individual target
   * "harming" ais will prefer a spell that deals 50 damage to one enemy, over a spell that deals 25 to 4
   * "harming" ais will also preferentially target the enemy to which a spell will be most effective
   
* "assassin" (OPTIONAL) - weighting, expected to be 0 to 100, but doesn't have to be
   * If any ability this turn can result in immediately killing one or more enemies on the field, it will be weighted by those target's combined max health
   * WARNING: While generally obvious from a player perspective, ais who do this in games tend to annoy most players who like single player experiences.  Generally, not doing this is the kind of "stupid" that player want computers to be.

* "survivor" (OPTIONAL) - weighting, expected to be 0 to 100, but doesn't have to be
   * Weights the smartness of each available action based on how much they will heal the caster
   
* "healer" (OPTIONAL) - weighting, expected to be 0 to 100, but doesn't have to be
   * Weights the smartness of each available action based on how much they will heal other member's of the caster's party

* "disabler" (OPTIONAL) - weighting, expected to be 0 to 100, but doesn't have to be
   * If any ability this turn can result in disabling any of a target's actions, it will be weighted at the target's max health

* "agro" (OPTIONAL) - weighting, expected to be 0 to 100, but doesn't have to be
   * Does not effect ability selection, but effects the weighting of target selection based on the total aboslute damage each target has done to the caster

* "tactician" (OPTIONAL) - weighting, expected to be 0 to 100, but doesn't have to be
   * Weights abilities based on the amount they instantly shift the total balance of estimated team power
   * For example, a target statMod skill like tail-whip on an enemy increases the absolute power potential of our team.  A caster statmod skill like swords dance increases the power potential of our team as well.
   * An ai with both winning and tactician intelligence will either attack, or tactically stat mod based on whether the total team power potential change outweighs the direct damage

* "strategist" (OPTIONAL) - weighting, expected to be 0 to 100, but doesn't have to be
   * Weights abilities based on the smart/winner estimate of the final outcome of the battle
   * I.e., choses the ability that most increases this team's chances of "winning" the battle - assuming winning-optimal choices

* [CLASS] (OPTIONAL) - weighting, expected to be 0 to 100, but doesn't have to be
   * You can specify a particular class that this ai preferentially targets

* [ABILITY] (OPTIONAL) - weighting, expected to be 0 to 100, but doesn't have to be
   * You can specify specific abilities as having higher weightings - to create ais that are preferential to doing a specific thing

* "pattern" (OPTIONAL) - a dictionary with a weighting, and a list of abilities
   * This ai will consider it smart to execute each ability in this list in order, in a continuing loop over the course of battle
   * If the current ability in the chain is unable to be cast, due to lack of targets, lack of mana, etc, it will be skipped and the next will be prioritized instead
   * using an intelligence 100, pattern 100 ai, with no other traits, is a simple way to construct nintendo style bosses which have a set pattern like "firestorm, sword strike, heal, barrier"...
