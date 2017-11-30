The battle system will be activated with two lists of entities called "party", and "enemy"
   * Each entity must define a a display name, a class, a level, a list of equipment, and a list of item rewards

A battle will undergo the following phases
   # The Introduction
     * The battle system will display introductory text, telling the player they are being attacked.
     * The battlefield will be laid out in the ui, showing all visible entities
     * this phase will run on a timer, dropping automatically to the next phase when expired
   # Player ability menu
     * The player will be presented with all top-level abilities for an entity in the party
       * If the entity has no available actions (i.e. if a status effect blocks all actions) it will be skipped
       * All typing options will be listed to the player
       * Some options (for example "item") may present a sub-menu of sub options
       * The player can type "help" on all options to get a description
       * The player may type "back" to return to the previous level menu
     * specifying an ability may ask the player to specify a target
       * If only one valid target is available for the action, this step will be skipped
       * Abilities will also store any availble fallback targets (i.e. other valid targets that were not selected)
       * typing "back" will return to the previous selection menu 
     * When the player selects an ability and target, the top level ability list for the next party member will open
   # Enemy ai decision
     * All non-player controlled entities on the field will select their battle abilities and targets based on their ai configuration and the state of the battle field
     * This process, while at times rather complicated, will be instantaneous from the end user perspective, and as such has no ui/ux concerns
   # Battle model update
     * All selected entity abilities will be sorted according to the speed of the entity and ability.
     * The resulting state changes for each ability will be applied in order
       * If an entity's desired target is no longer present, it will instead use the ability on the next listed fallback target
       * If an entity is not able to perform their ability at all (either because all available targets are dead, or because it has aquired a status effect during the model update that prevents it)
       * Each successfully performed ability will push a performance node to the performer for the acting entity
       * The attack will cycle through each target, checking the hit/evade ratio to select for misses and hits
         * on miss, this target will no have its model effected, and a "miss" performance node will be added to the performer for the target entity
       * Health deltas will be applied according to the ability, and will be capped between 0 and the target's max hitpoints
         * health deltas will take into account the power range, strike with/against ratios
         * in the case of a critical hit roll (for applicable abilities) the final damage will be multiplied and a critical hit performance node will be added for the target entity
         * The health delta will be applied to the performance node for the target entity
         * if the ability has an absorb ratio, the stolen health will be applied to the acting entity, and a performance node to show that health delta will be shown
       * status effect deltas will be pushed to the entity according to the ability
       * If any target's health hits zero, the status effect listed under "applyWhenHealthExhausted" will be applied as a delta to it
       * the absolute status effect deltas over the course of the ability eval will be pushed to the performance node for the effected entities
   # Performer update
     * Each queued performance noce will be executed in turn
     * A performance node will consist of the console saying "X has used Y [on Z]" which will be displayed on a timer
     * The performance node may describe damage being done to the enemies, and status effects applied
   # Defeat check
     * The game will validate that at least one member of the party has the status effect listed under "teamLosesWithoutAnyone"
     * if this check fails, a defeat message will be displayed on a timer, dynamicState.battle_result will be tagged "defeat", and the battle state will close
     * if the check passes, the next phase will be triggered
   # Victory check
     * The game will validate that at least one member of the enemy has the status effect listed under "teamLosesWithoutAnyone"
     * if this check passes, the game will cycle back to the PlayerAbilityMenu phase
     * if this check fails, the next phase will be triggered
   # Spoils phase 
     * the experience from each enemy with the status "spoilsAwardedFor" will be evenly distributed between all party members not exhibiting the "gainExperienceIf" status
     * any party members who's experience has crossed a level-up threshold will present level-up message, displaying all stat changes and new skills learned
     * any member of the enemy with the status "spoilsAwardedFor" will add their item rewards to the player's inventory.

---------------------------------------------------

Effects: (in battle.json)
  An effect is a property that can be applied to an entity on the battlefield.  These effects will be used for all contextual changes in an entities capability and viability.  Some effects will be directly visible and parseable things, like "poison", or "sleep".  Other effects will be used by the low level battle system (for example, all games will need to define some sort of "alive" and "dead" effect that the system will use to determine when battle ends and who wins).  Other effects may be hidden, for example an ability like pokemon's "tail whip" could work by applying a "defenseDown" status to an entity, that could be specified to stack up to 5 times.

(Effect Property Listing)
  "display" (OPTIONAL) - the text that displays next to an entity with this effect.  
    * Not all effects need to have displays, things like "alive" for example can be hidden
  "onPerformApplied" (OPTIONAL) - the performance text displayed by the battle system when this effect is given to someone
    * This is also options, but can help give feedback on effects that the user is supposed to be aware of, like poison or sleep, or death
  "duration" (OPTIONAL) - a minimum and maximum number of turns this effect lasts before going away
    * defaults to [0, 0]. a duration of [0, 0] implies that the effect will not go away on its own 
    * the actual duration of the effect will be chosen when it is applied to an entity
  "statModifiers" (OPTIONAL) - a dictionary of stats and their changes, that will be applied to the entity that has this effect
  "healthPerTurn" (OPTIONAL) - used to make an ability effect change health each turn
    * "points" specifies a base number added to an entity with this status
    * "percent" specifies a percentage of the entity's max health added to it each turn
    * this can be used to implement explicit poison type effects
    * this can also be used with hidden effects to create things like armor with life regeneration
  "manaPerTurn" (OPTIONAL) - used to make an ability effect change mana each turn
    * "points" specifies a base number added to an entity with this status
    * "percent" specifies a percentage of the entity's max mana added to it each turn
  "stack" (OPTIONAL) - how many times this effect can be stacked on a target
    * defaults to 1
    * most effects should probably not stack, but things like a "defenseDown" applied from tail whip type skills will stack multiple small statModifiers together
  "actionBlock" (OPTIONAL) - a list of actions that an entity cannot do while this effect is present
    * these can be specific skills, like "skill.ice1", or top level menus like "fight"
    * this can be used to silence magic, prevent attacks, or more esoteric things like preventing running away
    * "ALL" can be specified to completely disable an entity (for example, for use with the "dead" effect)
  "suppressEffects" (OPTIONAL) - a list of other effects that this effect will negate
    * this allows a status effect when applied, to cancel out other status effects.
    * for example "dead" might cancel "alive"
  "visibility" (OPTIONAL) - specifies whether a target should be visible on the battlefield (i.e. whether their name appears) as a member of either the party or enemy team
    * For now i expect that this will only be used by the game's "alive" effect - so that all living enemies are visible, and the "dead" effect, which may for example show dead party members, but not dead enemies
    * this could also be used to create invisibility skills for enemies, etc

---------------------------------------------------

Abilities:
  An ability is a possible action that may be taken during battle by an enemy.  All possible actions will ultimately work via ability.  Abilities may be learned by an entity via leveling up their character class (such as magic spells), be granted by equipping a weapon (such as "fight"), applied by items (i.e. all types of consumable items like potions will reference an ability describing what they do), and more triggers may be introduced by plot/narrative as time goes on.

(Ability Property Listing)
  "action" (OPTIONAL) - what to type in the player ability phase to use this.  
    * dot delimited chains can be used to construct sub-menus
  "description" - what is displayed if the user types "help" and then the action
  "charges" (OPTIONAL) - the number of times this ability may be used by an entity
    * defaults to 0
    * 0 indicates it is not limited by ability specific charges
  "manaCost" (OPTIONAL) - the number of mana points consumed in using this ability
    * defaults to 9
  "skillPointCost" (OPTIONAL) - the number of skill points needed in this round to use the ability
    * defaults to 0
  "type" - the type key used by enemy armor solutions to determine damage multipliers
  "power" (OPTIONAL) - the minimum and maximum base power of the ability converted to damage
    * defaults to [0, 0]
    * this is the total damage in hit points done to a target, when no stats or modifiers, or type advantages are in place
    * two numbers specified will result in a random value between the two being chosen
    * 0, 0 implies an ability that does not deal damage as a primary effect
    * negative numbers should be used for abilities that heal targets
  "absorbPercent" (OPTIONAL) - a percentage (0-100) of the net applied damage to all targets to be returned to the caster as healing
    * defaults to 0
  "effectMask" - a list of effects that an entity must have in order to be a valid target
    * generally, all games will need to define some effect similar to "alive" that most abilities will mask on
    * some abilities, such as revive, may mask on "dead" status rather than "alive"
    * masks lists like ["alive", "poisoned"] can also be used to specify things like antidotes only being usable on targets that are poisoned
  "group" - which battlefield entities constitute valid targets
    * self - can use this skill only on yourself
    * ally - can use this skill on anyone in your party except you (defaults to first ally)
    * party - can use this skill on anyone in your party (defaults to you)
    * enemy - can use this skill on an enemy (defaults to first enemy)
   all - can use this skill anywhere on the battlefield (defaults to first enemy)
  "target" - the number of targets this ability can effect simultaneously
    * single - targets only one entity in the targetable group
    * distributable - defaults to targeting only one entity, but can distribute power across the entire targetable group
    * all - targets all entities in the valid group
  "strikeWith"/"strikeAgainst" - multipliers added to the offense and defense check to augment the ability's base damage
    * this field is not optional, you must specify both lists, even if those lists are empty
    * strength, magic, defense, resist, hit, speed - uses entity's current post-bonus stat
      * if your game defines other stats for all classes, they will also work
    * baseStrength, baseMagic, baseDefense, baseResist, baseHit, baseSpeed - uses entity's current pre-bonus stat
      * if your game defines other stats for all classes, putting "base" in front of them will work
    * you can technically use "crit" or "evade" if you like, but since those are designed to center around 0 instead of 100, they will likely result in unwanted behavior
    * "typeAdvantage" - returns the composite advantage that the ability has against the target's armor type
    * "weaponPower" - returns the absolute power of the weapon initiating the ability
    * "weaponAdvantage" - returns the absolute power of the weapon multiplier by typeAdvantage minus target's armor
  "statModifiers" (OPTIONAL) - changes to the stats of the caster which will be added only during the casting of this ability
    * for example, having an ability that gives a { "speed" : 100 } will add 100% to the caster speed while using this skill, such as with pokemon's "quick attack"
  "canEvade" (OPTIONAL) - true/false value indicating whether the caster hit/target evade stats should be rolled
    * default false if not specified
    * when false, the hit/evade calculation will be skipped - meaning this ability can never miss; such as with pokemon's "swift", or pseudo-abilities, like a consumable item battleAbility
  "critPercent" (OPTIONAL) - the percent damage multiplier (should be over 100%) when a critical hit is achieved
    * defaults to zero, zero indicates an ability that does not use the critical system
  "casterEffects"/"targetEffects" (OPTIONAL) - a dictionary of possible effects applied to the casting/target entity when the ability is used, mapped to each effects percent chance of appearing
  "ai" - the high level purpose of this ability, used by computer controlled enemies when selecting attacks
    * offensive - chosen by an ai that wants primarily to deal damage
    * healing - chosen by an ai that wants primarily to restore health (i.e. pokemon's recover, heal potions)
    * disable - chosen by an ai that wants primarily to temporarily disable or weaken a target (i.e. pokemon's sleep powder or thunder wave)
    * strategic - chosen by an ai that wants to effect the long term team vs team balance, for use in ability that have more subtle lasting effects (i.e. pokemon's growl or a mana potion)

---------------------------------------------------

Classes:
  A class defines a type of entity - used both for enemy types and defining the player's party members.

(Class Property Listing)
  "description" - help text for the class
    * displayed when typing "help {enemyName}" or "help {partyMemberName}" on the battlefield action selection phase
  "innateStatus" (OPTIONAL) - status effects that will be present when this entity starts battle.
    * most classes should innately have "alive" effect or equivalent
    * this can also be used to define classes that have innate life regen, or other effect based properties
    * a skeleton summon could be defined without being innately "alive" - and would enter the battlefield invisibly so that a necromancer could 'revive' it later
  "startingEquipment" (OPTIONAL) - a list of items that will be equipped by default on this class.  
    * This can be a simple way to set up party members to join the party with starting equipment
    * Especially on enemies, this equipment doesn't have to be actual user surfaced game items
    * For example, a way to implement the pokemon type system, would be to have all fire pokemon start with "fire_armor", water pokemon start with "water_armor", the armor would define all the fire/water type strengths and weaknesses, and then just not have an armor equip screen in the game, and no armor in the shops.
  "startingInventory" (OPTIONAL) - a list of items that will be granted to the team when this entity is instantiated
    * For now items belong to the party, not an entity
    * Any entity assigned to the player party will give its items to the player's item pool.
    * Giving the main character's class starting items is a simple way to make the player start with "stuff"
    * Giving an enemy class items can be a way to include consumable choices on the enemy, for example if you want a boss that has 3 heal potions, or 2 full restores, etc.
  "skills" (OPTIONAL) - a map of abilites that this class learns, and the level the ability is learned at.  If an entity with this class achieves these levels, the skills will automatically appear in their action lists
  "immunities" (OPTIONAL) - a list of effects or types that this class resists based on their level.
    * this can list either status effects, or ability types.  (i.e. a class can be immune to water skills, poison status, etc)
    * 100 implies complete immunity
    * 50 implies that this effect when applied by an ability won't take half the time
  "stats" - the base stats of the class
    * most stats are generally meant to be used as percentages, and should start at 100 and modify from there.  If you prefer menu design where the stats start at numbers like "5" or "20" instead of 100, i reccommend you leave the stats at 100, and we implement a display multiplier in the menus.  Otherwise tuning battle will be far harder to intuitively work with.  Don't make any stats negative.  Just... don't.  Stats are the core of the battle system, and making them weird will cause the bugs.  The bugs will weird and time-wastey.

    * "maxHealth" - the maximum hit points an entity can have by level
    * "maxMana" - the maximum mana points an entity can have by level
    * "skillRoll" - at the beginning of each battle round, a number will be rolled between zero and this, and certain skills will be dependent on that roll

    * "strength" - expected to be used as a strikeWith for physical skills
    * "magic" - expected to be used as a strikeWith for non-physical skills
    * "defend" - expected to be used as a strikeAgainst for physical skills
    * "resist" - expected to be used as a strikeAgainst for non-physical skills

      * NOTE: I say "expected", because the battle system itself will never know anything about these 4 stats.  All 4 are optional.  it's merely a convention that they exist and that abilities use them.  You can have as few or as many of them as you like - "strength, magic, defend, resist" is merely my implmentation of a pokemon/final fantasy style dual power spectrum.  All that matters, is that anything that abilities list as "strikeWith", or "strikeAgainst" be defined for each class as a stat (excluding special things like typeAdvantage)

    * "crit" - the percent chance of the entity performing critical hits with abilities (only used for abilities with a critMultiplier)
    * "hit/evade" - when an ability is tagged "canMiss", the (caster's hit)-(target's evade) specifies the percent chance of an ability landing. 
      * for "all" target abilities, the average evade of all targets will be used
      * for "distribute" target abilities, each target will roll for contact seperately - some may hit and others may miss
    * "speed" - used to determine the ability execution order in battle.  All entities will attack in order of decreasing speed, including bonuses from items, effects, and the selected abilities.  If two entities resolve to the exact same speed on their abilities, one of them will be randomly selected to attack first
  "experience" (OPTIONAL) - the experience points awarded to the party when one of these enemies is defeated.
    * after battle, all experience will be combined from the enemy team, and distributed across the party evenly between all entities with the "gainExperienceIf" effect specified in the battle.json
    * if you want dead party members not to recieve experience, specify this field with the "alive" effect
    * if you do want dead party members to recieve experience, leave this field as an empty string
    * if you want to be crazy, you could do shit like only people with some "meditation" effect get experience after battle or some shit like that.
  "spoils" (OPTIONAL) - a dictionary of rewards this enemy adds to the pool of battle spoils when defeated
    * each item listed can specify and amount and drop chance based on the level of the defeated entity
    * if for example, something has an amount of 3, and a drop rate of 50, that would imply killing an entity of this class makes the battle system will roll 50% odds for the item 3 times in a row.

---------------------------------------------------

Items:
  items constitute and shared collectable anythings in the party.  These need not necessarily be true "items".  Some may be consumable items or equippable things.  Others may be quest specific items,  Currency and achievements can also be represented by the item system, and placed in categories that keep them out of the "usable" inventory.  Similarly, "hidden" item categories could be a general purpose way to track non-linear player progress.  For example, a side quest could give a player a secret "complimentedMedusasHair" item or something that might inject some fluffy bullshit into the game's ending sequence.

(Item Property Listing)

  "description" - text shown when typing "help {itemName}" in the battle selection menu
    * probably also in equip screens and shops, if and when we get to that
  "category" - which type of item this is. 
    * The battle system will only surface the existence of items listed in the "battleItemCategory" in battle.json.
    * All equipment and consumable items should probably be in the same main category
    * As mentioned before, other examples of categories could be currencies, non-usable directly usable quest items like "zelda's letter", achievements, tallies of how in love with you your party members are... whatever.
  "battleAbility" (OPTIONAL) - an ability that this item triggers when used in battle
    * causes this item to appear in battle as an option for all party members under the "item" category
    * intended for potions, etc
  "consumable" (OPTIONAL) - whether or not this item is consumed when used in battle
    * defaults to false
    * only matters right now for items with a battleAbility
    * Example 1: a potion would be consumable, and have a battle ability.  you use one up in battle and it does a thing
    * Example 2: the gen 1 pokeflute would havea battle ability, but would not be consumable
    * Example 3: a rare candy would be consumable but would not have a battle ability.  instead it would probably have a menuAbility, or something like that when we add more menus/game dynamics
  "equipSlot" (OPTIONAL) - which of the slots defined in config.json's "equipSlots" this item can be equipped to
    * When not specified, this item cannot be equipped
  "equipClassMask" (OPTIONAL) - a list of classes that can equip this item
    * This only matters for items with an equip slot
    * If blank, any class can equip it
  "equipGrantAbility" (OPTIONAL) - a list of abilities the user can use when this item is equipped
    * All items intended as weapons should probably grant some ability that is surfaced with an action like "fight" or "attack".  That way, we can specify all weapons using the existing ability system, which means that weapons need not just do damage.  we can have thigns like healing rods.  Also, this will set it up so if you have no weapons equiped, the "fight" option will automatically disappear
  
  "power" (OPTIONAL) - min and max power value
    * defaults to [0, 0]
    * intended for itmes that act as weapons when equipped.  power will only be used for the abilities listed under "equipGrantAbility"
    * abilities using "weaponAdvantage" or "weaponPower" strikes will use this value as a multiplier on the ability's base power
    * if different numbers specified, the applied multiplier will be randomly select from the range - allowing for weapons that do inconsistent damage
  "protection" (OPTIONAL) - reduces the damage of abilities using the "weaponAdvantage" strike parameter
    * defaults to 0
    * penalty surface against an attacker's abilitypower*itempower*typeEffectiveness when using the "weaponAdvantage" metric
    * intended for items that act as armor when equipped
  "typeEffectiveness" (OPTIONAL) - specifies a damage multiplier by type when equipped, used to increase (or decrease) vulnerability against various ability types
    * 100: no effect, <100: this element hurts people with this armor less, >100: this element hurts people with this armor more 
    * intended for items that act as armor when equipped
  "suppressEffects" (OPTIONAL)
    * when this item is equipped, it prevents these effects from being applied to the entity.  Can be used to make poison resist rings, etc.
    * when this item is triggered via battleAbility, these effects are immediately removed from the item's ability target(s)
  "max" (OPTIONAL) - the maximum number of this item you can hold at a time
    * defaults to 1
  "value" (OPTIONAL) - the base market cost of this item, in other items (for example currency)
    * THIS IS NOT USED BY THE BATTLE SYSTEM
    * but I thought i'd include it to demonstrate how this kind of thing might work, and how to make another category like currency interact with equippable items.