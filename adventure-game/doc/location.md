# Locations
  locations constitute a state that the user can occupy, which can populate instances, enemies, travel options, etc

## Location Property Listing
* "description" - text displayed while on the base level scene of this area
* "travel" (OPTIONAL) - a dictionary of possible locations that the user can move to
	* Each travel object specifies a necessary game_flag.  Without this flag, the location will be hidden from the Travel menu.
	* If no travel options are specified, or if all of them are blocked by unmarked flags, the Travel menu will not appear in game for this location
* "encounter_rate" (OPTIONAL) - The percent chance of triggering an encounter when entering this area
	* Requires encounter_types to be specified
* "encounter_types" (OPTIONAL) - A dictionary of available encounters in this are
	* each encounter type must specify the weighted chance of this encounter being selected
* "instances" (OPTIONAL) - A dictionary of instances available in this area, either as direct choices, or randomized in an explore menu
	* More information on instances listed below in the 'Instance Property Listing' section
* "npc" (CURRENTLY UNUSED)
* "npc_options" (CURRENTLY UNUSED)

## Instance Property Listing
* "canSelectDirectly" (OPTIONAL) - true/false bool specifying whether this instance will appear directly in the location base menu
	* defaults to false
	* do not set to true if a non-zero exploreWeight is specified, or it will cause undefined behavior
* "exploreWeight" (OPTIONAL) - the weighted likelihood of doing this instance when selecting the "Explore" menu
	* defaults to zero
	* zero means this will not show up in the Explore menu
	* the Explore menu will only appear if at least one non-completed instance in the are has a weight
	* do not specify a non-zero explore weight to instances with true canSelectDirectly, or it will cause undefined behavior
* "unlockFlag" (OPTIONAL) - a flag stored in the dynamicData profile / saved game which needs to be set for this instance to show up
	* if no completionFlag is specified, this instance will be always be available unless it's completed
* "completionFlag" (OPTIONAL) - a flag stored in the dynamicData profile / saved game indicating this instance is done
	* if no completionFlag is specified, this instance will be playable an infinite number of times
	* once the instance calls a MarkCompleted node, this instance will dissapear from locations, or as explore possibilities
* "nodes" - an ordered list of narrative elements, executed (by default) in order, first to last, after which the instance ends
	* "type" - each element must list a type, describing what happens at this step.  the following types are supported:
		* "Choice" - the user will be presented with a menu of options
			* each choice will automatically advance to the next node
			* options can list an "action", which will execute any python code desired in the context of the instance
			* options can list a "condition", which will evaluate any python code desired in the context of the instance
				* if a condition is specified and the condition not met, this option will not be presented to the player as a choice
		* "Display" - adds a block of specified "text" for the user to read
			* this text, and all other displayed text will technically not be shown until the next "Choice" node
			* if a "Display" node doesn't have any choices after it, it will be shown on the root location when the instance finishes
		* "MarkCompleted" - logs the instance's completion flag to the player profile
			* This will prevent this instance from being playable again
			* You may skip over this node, if you only want an instance to be finished under certain conditions
		* "Done" - ends the instance, skipping all future nodes
		* "Quit" - shuts down the game

## Instance Node Choice Functions
  Both the "action" and "condition" options on Choice options will execute short blocks of python.
  The following functions are available internally, to help with scripting:
  
* self.skip( count )
	* skips over a certain number of the next nodes.  This is used in choose-your-own-adventure-book style
	* you can specify negative numbers to return to earlier nodes
	* all choices advance by 1 automatically, 
	* Ex `{ "action" : "self.skip(1)" }` - skips over the next node and runs the one after it instead
	* Ex `{ "action" : "self.skip(0)" }` - goes to the next node like normal
	* Ex `{ "action" : "self.skip(-1)" }` - repeats the same choice twice
* self.setTemp( index, value ) - sets a true/false value for this specific instance with a numeric id
	* these temps will be forgotten after the instance is done, so this is a safe way to add complexity to just one instance without effecting the player's save file, or game as a whole
	* intended to be used in "action" blocks
	* Ex `{ "action" : "self.setTemp(0, True)" }`
* self.getTemp( index ) - returns true/false depending on how this temp has been previously set
	* defaults to false if the index has not been used
	* intended to be used in "condition" blocks
	* Ex `{ "condition" : "self.getTemp(0)" }`
* self.setFlag( id, value ) & self.getFlag( id ) - similar to above, but manipulates the flags on the user's save game
	* these are the same flags used by the completionFlag and the travel blocks, so this can be a way for an instance to turn other parts of the game on and off
	* Ex `{ "action" : "self.setFlag('killedKing', True)" }`
	* Ex `{ "condition" : "self.getFlag('killedKing')" }`
* self.setNumber( id, value ) & self.getNumber( id ) - effect numbers on the player's profile and saved game
	* Ex `{ "action" : "self.setNumber('beardAwesomness', 22)" }`
	* Ex `{ "condition" : "self.getNumber('beardAwesomness') > 10" }`
* self.setString( id, value ) & self.getString( id ) - effect strings on the player's profile and saved game
	* Ex `{ "action" : "self.setString('nickName', 'Biff')" }`
	* Ex `{ "condition" : "self.getString('nickName') == 'Biff'" }`
