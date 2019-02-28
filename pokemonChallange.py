import pokebase
import inspect

cache = {} #Global cache

def get_API_ClassNameOfInstance(api_instance_object): #Given api_object, return api_object class name.
    if not isinstance(api_instance_object, pokebase.NamedAPIResource): #all api object in Pokebase interface are NamedAPIResource Objects.
        return "NOT API INSTANCE!"
    return repr(api_instance_object).split()[0][1:]

def api_isinstance(obj, api_name_of_class): #Given any object and the name of the should be object's class
    obj_api_class_name = get_API_ClassNameOfInstance(obj)
    return obj_api_class_name == api_name_of_class #Returns if the object is instance of the api class


def cacheHandler(function): #My implementation of memozation and my very own cache handler.
	global cache #Given a function
	def cached_function(*args):
		if not function in cache: #If function was never called before, create function own cache inside the global cache.
			cache[function] = {}
		if args in cache[function]: # If thoes arguments are inside the function cache, return already calculated answer.
			return cache[function][args]
		result = function(*args) #Fetch function result for thoes arguments.
		cache[function][args] = result #Save result in the function cache for thoes arguments
		return result #Return result
	return cached_function #Return function

@cacheHandler
def pokebase_API_caller_cached(api_call_command,input_command): # wrapper function for any pokebase api calling to fetch api objects. The idea is to also cache thoes calls.
    try:
        answer = getattr(pokebase,api_call_command)(input_command)
    except ValueError:
        answer = f"Error Invalid Command/Input,in : {api_call_command}({input_command})"
    return answer #Returns the api object that had been requested. 
    

@cacheHandler
def type_Against_type_strengthResult(Type_Attacker,Type_Attacked): #Given the attacking type and the type of the attacked
    if not api_isinstance(Type_Attacker,"type"): #Checks the given "type" is actual an api type.
        return "ERROR in Type_Attacker"
    if not api_isinstance(Type_Attacked,"type"):
        return "ERROR in Type_Attacked"
    answer = 1 #As in default the answer is 1 , normal damage. Then checks if the Type_Attacked is in relataion to different damages.
    for i in Type_Attacker.damage_relations.no_damage_to:
        if i["name"] == Type_Attacked.name:
            answer = 0 #Type_Attacker gives no damage to Type_Attacked
    for i in Type_Attacker.damage_relations.half_damage_to:
        if i["name"] == Type_Attacked.name:
            answer = 0.5 #Type_Attacker gives half damage to Type_Attacked
    for i in Type_Attacker.damage_relations.double_damage_to:
        if i["name"] == Type_Attacked.name:
            answer = 2 #Type_Attacker gives double damage to Type_Attacked
    return answer #Returns caclulated strength .


@cacheHandler
def moveName_Against_pokemonName_strengthResult(moveName,pokemonName): #Given the name of the move and the name of the pokemon that been attacked.
    moveObj = pokebase_API_caller_cached("move",moveName) #Calling and fetching move api object. By given move's name.
    pokemonObj = pokebase_API_caller_cached("pokemon",pokemonName) #Calling and fetching pokemon api object. By given pokemon's name.
    if not api_isinstance(moveObj,"move"): #Checks if there is a move by that name in the api.
        return "ERROR in move, Invalid move."
    if not api_isinstance(pokemonObj,"pokemon"): #Checks if there is a pokemon by that name in the api.
        return "ERROR in pokemon, Invalid pokemon."
    moveType = moveObj.type
    pokemonTypes = pokemonObj.types
    answer = 1
    for i in pokemonTypes:
        answer *= type_Against_type_strengthResult(moveType,i.type)
    return answer #Returns the calculated multiplier strength.



print("""WELCOME TO POKEMON FIGHT CLUB!!!!!
In here you will able to fight with and against your favorite pokemons!
here are the basic rule to the system:
1.The game will start when the user will enter "START GAME"
2.After "START" you will enter the Arena
3.At the Arena you can have infinte times of rounds so to finish/stop the Arena enter at the end of the last round "FINISH"
4.You will be asked at the end of each round if the player wants to continue.
5.At the end of The Arena ,you can exit the game by entering "EXIT GAME" .""") #Openning text and game instructions.

stateOfGame = "FALSE GAME" #By game on hold, starts when the player is ready.
while stateOfGame != "START GAME":
    stateOfGame = input("Want to start the game? Enter 'START GAME':")

while stateOfGame == "START GAME": #Game loop, starts at 'START GAME'.
    print("Starting The Arena on Default!!!")
    print("Welcome to THE ARENA!!!!")
    stateOfRound = "YES"
    counterRounds = 1 #Counting number of rounds
    RoundsWon = 0 #Counting number of won mathces
    while stateOfRound != "NO": #Starts New Round by default.
        print(f"ROUND NO.{counterRounds}:")
        print("Example for input: [name_of_move] -> [name_of_pokemon] ...[name_of_pokemon_n]")
        print("Input :")
        inputString = input() #Getting player input to the round.
        nameOfMove ,listOfPokemonsNames = inputString.split(" -> ")
        listOfPokemonsNames = listOfPokemonsNames.split()
        MatchResult = 1
        for i in listOfPokemonsNames:
            tempMultiplier = moveName_Against_pokemonName_strengthResult(nameOfMove,i)
            if isinstance(tempMultiplier,str): #If tempMultiplier is a string, not an integer/result, it is returns an error.
                print("Error in Input")#Prints to the player that he used an incorrect input.
                print(tempMultiplier)
                MatchResult = 0 #Match result is 0 since there is nothing to calculate in error.
                break #Break to exit searching for new matches in input.
            print(f"Match: {nameOfMove} vs {i} : {tempMultiplier}")
            MatchResult *= tempMultiplier
        print(f"Output (Round result):\nx{MatchResult}")
        if MatchResult != 0: #If match wasn't lost or had an error in input, adds to the counter of won rounds.
            RoundsWon += 1
        counterRounds += 1
        stateOfRound = input("To Continue the Arena enter 'YES' else enter 'NO':")
    print(f"Number of Rounds that you WON! :{RoundsWon}")
    endGame = input("Want to Exit? Enter 'EXIT GAME'") #If the player wants to exit the game.
    if endGame == "EXIT GAME":
        stateOfGame = endGame
print("Thanks for playing POKEMON FIGHT CLUB!!!!!!")
