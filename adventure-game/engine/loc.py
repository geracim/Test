import re

class dictionary:
    strings = None
    static = None
    dynamic = None

def setup( strings_source, static_source, dynamic_source ):
    dictionary.strings = strings_source
    dictionary.static = static_source
    dictionary.dynamic = dynamic_source

# takes an input string and runs it through the staticData strings for replacing
def translate( input_string, local_data=None ):
    if input_string in dictionary.strings:
        result = dictionary.strings[input_string]

        # if result is not a string, assume its a list of strings and join them into a newline delimited string
        if not isinstance( result, str ):
            result = '\n'.join(result)
    else:
        result = input_string

    # Um, regular expressions are a whole mess of bullshit, but this means:
    # "find all things inside {} and give me a list of them"
    substitutions = re.findall('\{([^}]+)\}', result)
    if substitutions:
        for matchKey in substitutions:
            # split the contained string within the braces into an array of keys
            replaceKeyComponents = matchKey.split('.')
            node = None
            # check if the first key is an attribute of either the staticData or dynamicData classes
            firstKey = replaceKeyComponents[0]
            if local_data and firstKey in local_data:
                node = local_data[firstKey]
            elif hasattr(dictionary.dynamic, firstKey):
                node = getattr(dictionary.dynamic, firstKey)
            elif hasattr(dictionary.static, firstKey):
                node = getattr(dictionary.static, firstKey)

            if node:
                # remove the first item from the list
                replaceKeyComponents.pop(0)
                # walk the json object using the keys
                for key in replaceKeyComponents:
                    if key in node:
                        node = node[key]
                    else:
                        node = None
                        break
            if node:
                # replace the string
                result = result.replace( "{" + matchKey + "}", str(node) )
    return result
