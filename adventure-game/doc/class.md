# Classes
  A class defines a type of combatant - used both for enemy types and defining the player's party members.

## Class Property Listing
* "description" - help text for the class
    * displayed when typing "help {enemyName}" or "help {partyMemberName}" on the battlefield action selection phase
* "innateStatus" (OPTIONAL) - status effects that will be present when this combatant starts battle.
    * most classes should innately have "alive" effect or equivalent
    * this can also be used to define classes that have innate life regen, or other effect based properties
    * a skeleton summon could be defined without being innately "alive" - and would enter the battlefield invisibly so that a necromancer could 'revive' it later
* "startingEquipment" (OPTIONAL) - a list of items that will be equipped by default on this class.  
    * This can be a simple way to set up party members to join the party with starting equipment
    * Especially on enemies, this equipment doesn't have to be actual user surfaced game items
    * For example, a way to implement the pokemon type system, would be to have all fire pokemon start with "fire_armor", water pokemon start with "water_armor", the armor would define all the fire/water type strengths and weaknesses, and then just not have an armor equip screen in the game, and no armor in the shops.
* "startingInventory" (OPTIONAL) - a list of items that will be granted to the team when this combatant is instantiated
    * For now items belong to the party, not an combatant
    * Any combatant assigned to the player party will give its items to the player's item pool.
    * Giving the main character's class starting items is a simple way to make the player start with "stuff"
    * Giving an enemy class items can be a way to include consumable choices on the enemy, for example if you want a boss that has 3 heal potions, or 2 full restores, etc.
* "skills" (OPTIONAL) - abilites that this class learns
    * "level" (OPTIONAL) - If an combatant with this class achieves these levels, the skill will automatically appear in their action lists
	   * if this is not specified, the ability will always be available
	* "maxLevel" (OPTIONAL) - an upper bound, after which this skill will no longer be known
	   * this can be used to create two seperate stages of an ability with the same visible name, that function differently
* "opponentSkills" (OPTIONAL) - abilities that anyone attacking this class will temporarily know
    * these can be used to create an undertale like experience where a player may intrinsically have the ability to "scream uselessly", but only when fighting a ghost
    * "level" (OPTIONAL) - the level this class needs to have achieved for the ability to appear for opponents
	   * if this is not specified, the ability will always be available
	* "maxLevel" (OPTIONAL) - an upper bound on this class's level, after which enemies will no longer see this skill
* "immunities" (OPTIONAL) - a list of effects or types that this class resists based on their level.
    * this can list either status effects, or ability types.  (i.e. a class can be immune to water skills, poison status, etc)
    * 100 implies complete immunity
    * 50 implies that this effect when applied by an ability won't take half the time
* "stats" - the base stats of the class
    * most stats are generally meant to be used as percentages, and should start at 100 and modify from there.  If you prefer menu design where the stats start at numbers like "5" or "20" instead of 100, i reccommend you leave the stats at 100, and we implement a display multiplier in the menus.  Otherwise tuning battle will be far harder to intuitively work with.  Don't make any stats negative.  Just... don't.  Stats are the core of the battle system, and making them weird will cause the bugs.  The bugs will weird and time-wastey.

    * "maxHealth" - the maximum hit points an combatant can have by level
    * "maxMana" (OPTIONAL) - the maximum mana points an combatant can have by level
	   * defaults to 0
    * "skillRoll" (OPTIONAL) - at the beginning of each battle round, a number will be rolled between zero and this, and certain skills will be dependent on that roll
	   * defaults to 0

    * "strength" (OPTIONAL) - expected to be used as a strikeWith for physical skills
    * "magic" (OPTIONAL) - expected to be used as a strikeWith for non-physical skills
    * "defend" (OPTIONAL) - expected to be used as a strikeAgainst for physical skills
    * "resist" (OPTIONAL) - expected to be used as a strikeAgainst for non-physical skills

      * I say "expected", because the battle system itself will never know anything about these 4 stats.  
	  * All 4 are optional and have no default.  it's merely a convention that they exist and that abilities use them. 
	  * You can have as few or as many combat stats as wanted - "strength, magic, defend, resist" is merely my implmentation of a pokemon/final fantasy style dual power spectrum.  All that matters, is that anything that abilities list as "strikeWith", or "strikeAgainst" be defined for each class as a stat (excluding special things like typeAdvantage)

    * "crit" - the percent chance of the combatant performing critical hits with abilities (only used for abilities with a critMultiplier)
    * "hit/evade" - when an ability is tagged "canMiss", the (caster's hit)-(target's evade) specifies the percent chance of an ability landing. 
      * for "all" target abilities, the average evade of all targets will be used
      * for "distribute" target abilities, each target will roll for contact seperately - some may hit and others may miss
    * "speed" - used to determine the ability execution order in battle.  All entities will attack in order of decreasing speed, including bonuses from items, effects, and the selected abilities.  If two entities resolve to the exact same speed on their abilities, one of them will be randomly selected to attack first
* "experience" (OPTIONAL) - the experience points awarded to the party when one of these enemies is defeated.
    * after battle, all experience will be combined from the enemy team, and distributed across the party evenly between all entities with the "gainExperienceIf" effect specified in the battle.json
    * if you want dead party members not to recieve experience, specify this field with the "alive" effect
    * if you do want dead party members to recieve experience, leave this field as an empty string
    * if you want to be crazy, you could do shit like only people with some "meditation" effect get experience after battle or some shit like that.
* "spoils" (OPTIONAL) - a dictionary of rewards this enemy adds to the pool of battle spoils when defeated
    * each item listed can specify and amount and drop chance based on the level of the defeated combatant
    * if for example, something has an amount of 3, and a drop rate of 50, that would imply killing an combatant of this class makes the battle system will roll 50% odds for the item 3 times in a row.
* "effectChains" (OPTIONAL) - a dictionary of effect lists that will be automatically applied to this class if the key effect is applied
    * for example, to implement pokemon style "sunnyDay", a fire pokemon and grass pokemon might define these chains:
	   * "effectChains" : { "sunnyDayEffect" : [ "firePowerBuff" ] }
	   * "effectChains" : { "sunnyDayEffect" : [ "replaceSolarBeamWith1TurnSolarbeam" ]
* "ai" (OPTIONAL-ISH) - a specific ai model that entities of this class will use
	* Either an ai or an aiStack must be defined
* "aiStack" (OPTIONAL-ISH) - a collection of condition blocked ais entities of this class will use
	* Either an ai or an aiStack must be defined
	* each key will be a python evaluatable condition string
	* each value will be an ai
	* For example [ "true" : "attacker", "most_hurt_party_member[health] < 50" : "healer" ] would mean the character would generally use an "attacker" ai, but would switch to a "healer" ai for any round where the most hurt party member on their team had less than 50% health
	* the following global variables will be exposed
	    * "battle_duration" - how long the battle has gone on in rounds
        * "shsw_duration" - how much longer the battle is predicted to take in rounds
		* "party", "enemy" - returns objects with data on the two teams relative to the combatant in question
			* "shsw_result"
			* "sah_party_overpower_estimate"
	* the following combatant access variables will be supplied for python keys:
		* "me" - the caster
		* "agro_source" - the combatant on the field that has harmed us the most
		* "strongest_combatant" - the combatant in play with the most potential to deal absolute distributed damage
		* "strongest_enemy" - the enemy combatant with the most potential to deal absolute distributed damage
		* "strongest_party_member" - the friendly party member (including self) with the most potential to deal absolute distributed damage
		* "strongest_ally" - the friendly party member (not including self) with the most potential to deal absolute distributed damage
		* "weakest_combatant" - ... with the least potential to deal absolute distributed damage
		* "weakest_enemy" - ... with the least potential to deal absolute distributed damage
		* "weakest_party_member" - ... with the least potential to deal absolute distributed damage
		* "weakest_ally" - ... with the least potential to deal absolute distributed damage
		* "healthiest_combatant" - ... with the highest current percent health
		* "healthiest_enemy" - ... with the highest current percent health
		* "healthiest_party_member" - ... with the highest current percent health
		* "healthiest_ally" - ... with the highest current percent health
		* "must_hurt_combatant" - ... with the lowest current percent health
		* "must_hurt_enemy" - ... with the lowest current percent health
		* "must_hurt_party_member" - ... with the lowest current percent health
		* "must_hurt_ally" - ... with the lowest current percent health
	* the following properties will be checkable on those supplied variables:
		* "name" - the active name of the combatant
		* "class" - the string id of the combatant's class
		* [stat] - all current post-bonus stats will be checkable here
		* [effect] - returns the number of stacked instances of an effect of this type
		* "health" - current health points
		* "mana" - current mana points
		* "pattern_index" - the stage in the ai's attack pattern (returns 0 if no pattern ai is used)
		