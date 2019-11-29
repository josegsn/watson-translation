from configuration import * 

user_input = input("Introduce sentence to translate")
    
def get_languages():
    """
    Function generating a dictionary with all the languages available

    Args:
        None

    Returns:
        languages_dict (dict): with language code (e.g. 'en') as key and name (e.g. 'English') as value
    """
    
    languages_dict = dict()
    response_list = language_translator.list_identifiable_languages().get_result()['languages']
    
    for item in response_list:
        languages_dict[item['language']] = item['name']
    return languages_dict



def id_language(txt):
    """
    Function identifying the language of a text string

    Args:
        txt (str): string of text to be translated

    Returns:
        If the user agrees with the identified language:
        identified_language (str): a string with the identified language
    """
    
    print('\n Identifying language... \n')
    
    response_dict = language_translator.identify(txt).get_result()
    
    identified_language = response_dict['languages'][0]['language']
    
    language_name = get_languages()[identified_language]
    print(f"We believe your sentence is in {language_name}")
    
    agreement = input("Happy to proceed? (Y/N)")
    
    if agreement.upper() in ('YES','Y'):
        return identified_language
    else:
        print('Ok, sorry for that. Cancelling translating process')

identified_language = id_language(user_input)    
        
def find_available_model(language):
    """
    Function identifying the available langage model for the language identified

    Args:
        language (str): code for the language identified

    Returns:
        available_languages_list (list): list of languages to translate to
    """
    
    models = language_translator.list_models().get_result()
    models_list = []
    for model in models['models']:
        models_list.append(model['model_id'])

    available_models_list = list(filter(lambda m: m.startswith(language), models_list))
    available_languages_list = list(map(lambda x: x.split('-')[1],available_models_list))

    return available_languages_list

available_languages_list = find_available_model(identified_language)

def build_model(language, language_list):
    """
    Function building a model string to use in the translate function

    Args:
        language (str): code for the language identified
        language_list(list): list of languages to translate to

    Returns:
        model (str): model to be used in the translate function
    """
    languages_dict = get_languages()
    languages_dict_reversed = dict(map(reversed, languages_dict.items()))

    available_languages_text = """Pick one of the following available languages to translate to:\n\n"""
    
    for item in available_languages_list:
        try:
            available_languages_text += f"{languages_dict[item]}\n"
        except:
            continue

    selected_language = input(available_languages_text).lower().capitalize()
    model = f"{language}-{languages_dict_reversed[selected_language]}"
    return model

model = build_model(identified_language, available_languages_list)   

def translate():
    """
    Fuction that delivers the translation

    Args:
        user_input (str): text to be translated
        model(str): translation model

    Returns:
        translation (str): translated text
    """
    
    translation = language_translator.translate(
    text=user_input,
    model_id=model).get_result()
    translation = translation['translations'][0]['translation']
    return translation
