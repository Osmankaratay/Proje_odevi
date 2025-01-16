from googleapiclient.discovery import build
from google.oauth2 import service_account
import numpy as np
import pandas as pd
from time import sleep
# use turkish UTF-8
import locale
locale.setlocale(locale.LC_ALL, 'tr_TR.UTF-8')

API_KEY = "AIzaSyBgfgTk6DfMkSGsCvOJr7RlOX1eE3YWDMg"

SPREADSHEETS_ID = "16Q-lSq-tW2A3j_wbicM5cLPYx45A_ErCGAlr0RGjZP4"

def authorize_google_sheets():
    """
    Authorizes and returns a Google Sheets API service instance.
    This function uses a service account to authenticate and authorize access to the Google Sheets API.
    It reads the service account credentials from a file named "keys.json" and uses the specified scope
    to create the credentials object. The function then builds and returns a Google Sheets API service instance.
    Returns:
        googleapiclient.discovery.Resource: An authorized Google Sheets API service instance.
    """
    Scope = ['https://www.googleapis.com/auth/spreadsheets']
    creds = None
    creds = service_account.Credentials.from_service_account_file("keys.json", scopes=Scope)
    sheets = build('sheets', 'v4', credentials=creds)

    return sheets
sheets = authorize_google_sheets()
def load_spreadsheet_ranges():
    """
    Loads specific ranges from a Google Sheets spreadsheet and returns their values.
    The function retrieves data from the following ranges in the spreadsheet:
    - Signal: 'Kontrol sayfası'!C4
    - Date: 'Kontrol sayfası'!D4
    - Members: 'Kontrol sayfası'!E4
    - Play: 'Kontrol sayfası'!F4
    - Banned: 'Kontrol sayfası'!G4
    It converts the retrieved data into pandas DataFrames and extracts the first cell value from each DataFrame.
    Returns:
        tuple: A tuple containing the values from the specified ranges in the following order:
            - signal (str): Value from 'Kontrol sayfası'!C4
            - Range_date (str): Value from 'Kontrol sayfası'!D4
            - Range_members (str): Value from 'Kontrol sayfası'!E4
            - Range_play (str): Value from 'Kontrol sayfası'!F4
            - Range_banned (str): Value from 'Kontrol sayfası'!G4
    """
    Range_of_signal = "'Kontrol sayfası'!C4"
    Range_of_Range_of_Date = "'Kontrol sayfası'!D4"
    Range_of_Range_of_Members = "'Kontrol sayfası'!E4"
    Range_of_Range_of_Play = "'Kontrol sayfası'!F4"
    Range_of_Banned = "'Kontrol sayfası'!G4"

    _signal = sheets.spreadsheets().values().get(spreadsheetId=SPREADSHEETS_ID, range=Range_of_signal).execute()
    _Range_date = sheets.spreadsheets().values().get(spreadsheetId=SPREADSHEETS_ID, range=Range_of_Range_of_Date).execute()
    _Range_members = sheets.spreadsheets().values().get(spreadsheetId=SPREADSHEETS_ID, range=Range_of_Range_of_Members).execute()
    _Range_play = sheets.spreadsheets().values().get(spreadsheetId=SPREADSHEETS_ID, range=Range_of_Range_of_Play).execute()
    _Range_banned = sheets.spreadsheets().values().get(spreadsheetId=SPREADSHEETS_ID, range=Range_of_Banned).execute()

    _signal_df = pd.DataFrame(_signal.get("values", []))
    _Range_date_df = pd.DataFrame(_Range_date.get("values", []))
    _Range_members_df = pd.DataFrame(_Range_members.get("values", []))
    _Range_play_df = pd.DataFrame(_Range_play.get("values", []))
    _Range_banned_df = pd.DataFrame(_Range_banned.get("values", []))

    signal = _signal_df.iloc[0,0]
    Range_date = _Range_date_df.iloc[0,0]
    Range_members = _Range_members_df.iloc[0,0]
    Range_play = _Range_play_df.iloc[0,0]
    Range_banned = _Range_banned_df.iloc[0,0]

    return signal, Range_date, Range_members, Range_play, Range_banned

def extract_spreadsheet_values(Range_date, Range_members, Range_play, Range_banned):
    """
    Extracts values from specified ranges in a Google Sheets spreadsheet and returns them as DataFrames and lists.
    Args:
        Range_date (str): The range string for the date values in the spreadsheet.
        Range_members (str): The range string for the member values in the spreadsheet.
        Range_play (str): The range string for the play values in the spreadsheet.
        Range_banned (str): The range string for the banned values in the spreadsheet.
    Returns:
        tuple: A tuple containing:
            - play_dates (pd.DataFrame): DataFrame containing the play dates.
            - play_members (list): List of play members.
            - play (pd.DataFrame): DataFrame containing the play data.
            - banned (pd.DataFrame): DataFrame containing the banned data.
    """
    Range_of_member = f"'Üye Listesi'!{Range_members}"
    Range_of_Play = f"'Oyunlar, Oyuncular, Teknik Ekip'!{Range_play}"
    Range_of_Date = f"'Görev Listesi 24-25'!{Range_date}"
    Range_of_Banned = f"'Kontrol sayfası'!{Range_banned}"

    # Fetch data from Google Sheets
    _play_date = sheets.spreadsheets().values().get(spreadsheetId=SPREADSHEETS_ID, range=Range_of_Date).execute()
    _play_member = sheets.spreadsheets().values().get(spreadsheetId=SPREADSHEETS_ID, range=Range_of_member).execute()
    _play_ = sheets.spreadsheets().values().get(spreadsheetId=SPREADSHEETS_ID, range=Range_of_Play).execute()
    _banned = sheets.spreadsheets().values().get(spreadsheetId=SPREADSHEETS_ID, range=Range_of_Banned).execute()

    # Extract values from the fetched data
    __play_date__ = _play_date.get("values", [])
    __play_member__ = _play_member.get("values", [])
    __play__ = _play_.get("values", [])
    __banned__ = _banned.get("values", [])

    # Create DataFrames and lists from the extracted values
    play_dates = pd.DataFrame(__play_date__)
    play_members = [member for sublist in __play_member__ for member in sublist if member]
    play = pd.DataFrame(__play__)
    banned = pd.DataFrame(__banned__)

    return play_dates, play_members, play, banned

def translate_to_turkish_characters(text):
    """
    Translates the given text to Turkish characters by replacing lowercase Turkish characters
    with their uppercase equivalents.

    Args:
        text (str): The input string to be translated.

    Returns:
        str: The translated string with Turkish characters in uppercase.
    """
    translation_table = str.maketrans("iıçşğüö", "İIÇŞĞÜÖ")
    return text.translate(translation_table)

class Play:
    """
    A class to represent a play.
    Attributes
    ----------
    name : str
        The name of the play.
    actors : list
        A list of actors in the play.
    lights : str
        The lighting setup for the play.
    sound : str
        The sound setup for the play.
    responsible : str
        The person responsible for the play.
    Methods
    -------
    expert_level(person_name, level):
        Class method to set the expertise level of a person.
    called():
        Prints a message indicating the play is called.
    __str__():
        Returns a string representation of the play.
    """
    experts = {}

    def __init__(self, name, actors, lights, sound, responsible):
        self.name = name
        self.actors = actors
        self.lights = lights
        self.sound = sound
        self.responsible = responsible

    @classmethod
    def expert_level(cls, person_name, level):
        cls.experts[person_name] = level

    def called(self):
        print(f"{self.name} is called")

    def __str__(self):
        return f"{self.name} is a play"
    
def create_play(play):
    """
    Processes a DataFrame containing play information and extracts relevant details.
    Args:
        play (pd.DataFrame): A DataFrame where each row represents a part of the play with columns for play name, actors, lights, sound, and responsible persons.
    Returns:
        tuple: A tuple containing the following elements:
            - play_name (list): A list of play names.
            - play_actor (list): A list of lists, where each inner list contains the actors for each part of the play.
            - play_lights (list): A list of lists, where each inner list contains the lighting details for each part of the play.
            - play_sound (list): A list of lists, where each inner list contains the sound details for each part of the play.
            - play_responsible (list): A list of lists, where each inner list contains the responsible persons for each part of the play.
    """
    play_name = [play.iloc[i, 0].strip().lower() for i in range(len(play)) if play.iloc[i, 0]]
    play_actor, play_lights, play_sound, play_responsible = [], [], [], []

    for i in range(len(play)):
        if play.iloc[i, 0]:
            actor = [play.iloc[i, j].strip().lower() for j in range(1, 10) if play.iloc[i, j]]
            play_actor.append(actor)

            light = [l.strip().lower() for l in play.iloc[i, 10].split("/") if l]
            play_lights.append(light)

            sound = [s.strip().lower() for s in play.iloc[i, 11].split("/") if s]
            play_sound.append(sound)

            responsible = [r.strip().lower() for r in play.iloc[i, 12].split("+") if r]
            play_responsible.append(responsible)
        else:
            actor = [play.iloc[i, j].strip().lower() for j in range(1, 9) if play.iloc[i, j]]
            play_actor[-1].extend(actor)

    return play_name, play_actor, play_lights, play_sound, play_responsible

def creating_Play_objects(play_name, play_actor, play_lights, play_sound, play_responsible):
    """
    Creates a list of Play objects from the provided attributes.

    Args:
        play_name (list): A list of names for the plays.
        play_actor (list): A list of actors for the plays.
        play_lights (list): A list of lighting setups for the plays.
        play_sound (list): A list of sound setups for the plays.
        play_responsible (list): A list of responsible persons for the plays.

    Returns:
        list: A list of Play objects created from the provided attributes.
    """
    return [Play(play_name[i], play_actor[i], play_lights[i], play_sound[i], play_responsible[i]) for i in range(len(play_name))]

class _banned():
    """
    A class to represent a banned entity with unavailable dates.
    Attributes:
    -----------
    name : str
        The name of the banned entity.
    unavaiable_dates : list
        A list containing a single string of comma-separated dates or date ranges.
    _unavaiable_dates : list
        A list of individual unavailable dates.
    Methods:
    --------
    unzip_dates():
        Processes the unavaiable_dates attribute to populate the _unavaiable_dates list with individual dates.
    __str__():
        Returns a string representation of the banned entity and its unavailable dates.
    """
    def __init__(self, name, unavaiable_dates=""):
        self.name = name
        self.unavaiable_dates = [unavaiable_dates]
        
        self._unavaiable_dates = []
        self.unzip_dates()

    def unzip_dates(self):
        date_list = self.unavaiable_dates[0].split(",")
        for date in date_list:
            if "-" in date:
                start, end = map(int, date.split("-"))
                self._unavaiable_dates.extend(range(start, end + 1))
            else:
                try:
                    self._unavaiable_dates.append(int(date))
                except ValueError:
                    print(f"Invalid date input: {date}")
        return self._unavaiable_dates
    
    def __str__(self):
        return f"{self.name} is banned on {self._unavaiable_dates}."
    
def creating_banned_objects(banned):
    """
    Creates a list of banned objects from a DataFrame.

    Args:
        banned (pd.DataFrame): A DataFrame containing banned items. The first column should contain the primary
                               identifier for the banned item. The second column, if present, should contain
                               additional information about the banned item.

    Returns:
        list: A list of banned objects created using the _banned function. Each object is created using the
              primary identifier from the first column and additional information from the second column if available.
    """
    return [_banned(banned.iloc[i, 0], banned.iloc[i, 1] if banned.shape[1] > 1 else "") for i in range(len(banned))]

def play_date(play_dates, plays, play_member, ban_list):
    """
    Assigns roles to members for each play date and generates a new database and count dataframe.
    Parameters:
    play_dates (pd.DataFrame): DataFrame containing play dates and related information.
    plays (list): List of play objects, each containing name, actors, lights, sound, and responsible members.
    play_member (list): List of members available for assignment.
    ban_list (list): List of members who are banned from certain roles.
    Returns:
    tuple: A tuple containing:
        - new_db (pd.DataFrame): DataFrame with assigned roles for each play date.
        - count_df (pd.DataFrame): DataFrame with counts of roles assigned to each member.
    """
    new_db = pd.DataFrame(columns=["Light", "Sound", "Cafe"])
    p_member = [member.lower() for member in play_member]
    count_dict = {member.strip(): {"play": 0, "light": 0, "sound": 0, "cafe": 0} for member in p_member}

    for row in range(len(play_dates)):
        available_experts = [member.strip() for member in p_member]
        temp = 0
        while row + 1 < len(play_dates) and play_dates.iloc[row, 1] == play_dates.iloc[row + 1, 1]:
            for play in plays:
                if play.name == play_dates.iloc[row, 0]:
                    for actor in play.actors:
                        if actor.strip() in available_experts:
                            available_experts.remove(actor.strip())
            row += 1
            temp += 1
        row -= temp

        is_find = False
        for play in plays:
            if play.name == play_dates.iloc[row, 0].lower():
                for actor in play.actors:
                    if actor.strip() in count_dict:
                        count_dict[actor.strip()]["play"] += 1
                lighter = assign_role("light", play.lights, count_dict, ban_list, play_dates.iloc[row])
                sounder = assign_role("sound", play.sound, count_dict, ban_list, play_dates.iloc[row])
                cafe = assign_cafe(available_experts, ban_list, count_dict, len(play.responsible), play_dates.iloc[row])

                new_db = write_to_spreadsheet(lighter, sounder, cafe, new_db)
                is_find = True
                break

        if not is_find:
            cafe = assign_cafe(available_experts, ban_list, count_dict, 1, play_dates.iloc[row])
            new_db = write_to_spreadsheet("Play not found", "Play not found", cafe, new_db)

        #create dataframe from dictionary
        count_df = pd.DataFrame.from_dict(count_dict, orient="index")
        count_df = count_df.reset_index()
        count_df = count_df.rename(columns={"index": "Expert", "play": "Play", "light": "Light", "sound": "Sound", "cafe": "Cafe"})
        count_df = count_df.sort_values(by=["Play", "Light", "Sound", "Cafe"], ascending=False)
        count_df = count_df.reset_index(drop=True)

    return new_db, count_df

def write_to_spreadsheet(lighter, sounder, cafe, new_db):
    """
    Appends a new row to the given DataFrame with the provided data.

    Args:
        lighter (str): The value to be added in the "Light" column.
        sounder (str): The value to be added in the "Sound" column.
        cafe (list of str): A list of strings to be joined and added in the "Cafe" column.
        new_db (pd.DataFrame): The DataFrame to which the new row will be appended.

    Returns:
        pd.DataFrame: The updated DataFrame with the new row appended.
    """
    new_row = pd.DataFrame([{"Light": lighter, "Sound": sounder, "Cafe": " & ".join(cafe)}])
    new_db = pd.concat([new_db, new_row], ignore_index=True)
    return new_db

def assign_role(role, available_experts, count_dict, ban_list, play_date):
    """
    Assigns a role to an expert from the available experts list.
    Parameters:
    role (str): The role to be assigned.
    available_experts (list): List of available experts.
    count_dict (dict): Dictionary containing the count of roles assigned to each expert.
    ban_list (list): List of experts who are banned.
    play_date (str): The date of the play.
    Returns:
    list: A list containing the assigned expert or a message indicating no expert is available.
    """
    assigned_roles = []
    is_find = False
    
    available_experts = extract_banned(available_experts, ban_list, play_date)
    for _ in available_experts:
        try:
            if count_dict[_]["cafe"] + count_dict[_]["play"] + count_dict[_]["light"] + count_dict[_]["sound"] >= 15:
                available_experts.remove(_)
        except:
            pass
    i = 0
    while not is_find:
        i += 1
        try:
            if available_experts ==["-"]:
                assigned_roles.append("No need for expert")
                break
            else:
                choosen = np.random.choice(available_experts)
                count_dict[choosen][role] += 1

                assigned_roles.append(choosen)
                available_experts.remove(choosen)
                break
        except:
            assigned_roles.append("No expert available")
            break
    return assigned_roles

def assign_cafe(available_experts, ban_list, count_dict, count, play_date):
    """
    Assigns experts to a cafe task based on availability and constraints.
    Parameters:
    available_experts (list): List of experts available for assignment.
    ban_list (list): List of experts who are banned from being assigned on the given play_date.
    count_dict (dict): Dictionary containing the count of tasks each expert has been assigned to.
    count (int): Number of experts needed for the cafe task.
    play_date (str): The date for which the assignment is being made.
    Returns:
    list: List of experts assigned to the cafe task. If no experts are available, "No expert available" is added to the list.
    """
    cafe = []
    is_find = False
    
    available_experts = extract_banned(available_experts, ban_list, play_date)

    for _ in available_experts:
        try:
            if count_dict[_]["cafe"] + count_dict[_]["play"] + count_dict[_]["light"] + count_dict[_]["sound"] >= 7:
                available_experts.remove(_)
        except:
            pass

    while not is_find:
        try:
            choosen = np.random.choice(available_experts)
            count_dict[choosen]["cafe"] += 1
            
            cafe.append(choosen)
            available_experts.remove(choosen)
        except:
            cafe.append("No expert available")
            break

        if len(cafe) == count:
            break
    return cafe

def extract_banned(expert_list, ban_list, play_date):
    """
    Extracts the list of available experts by removing those who are banned on the given play date.
    Args:
        expert_list (list): A list of expert names.
        ban_list (list): A list of objects where each object has a 'name' attribute and an '_unavaiable_dates' attribute.
        play_date (str): The date of the play in the format 'YYYY-MM-DD'.
    Returns:
        list: A list of available experts who are not banned on the given play date.
    """
    banned_list = [ban_list[i].name for i in range(len(ban_list)) if ( int(play_date[1].split()[0])) in ban_list[i]._unavaiable_dates]
    available_experts = expert_list.copy()

    i = len(banned_list)
    while i > 0:
        for expert in available_experts:
            for banned_expert in banned_list:
                if expert == banned_expert.lower():
                    available_experts.remove(expert)
                    i -= 1
                    break
            i -= 1
    return available_experts

def flatten_list(value):
    """
    Flattens a list or numpy array into a comma-separated string.

    Args:
        value (list or np.ndarray): The list or numpy array to flatten.

    Returns:
        str: A comma-separated string of the elements if the input is a list or numpy array.
        Otherwise, returns the input value unchanged.
    """
    if isinstance(value, (list, np.ndarray)):
        return ', '.join(map(str, value))
    return value

def send_to_spreadsheet(new_db, spreadsheet_id, range_):
    """
    Sends the provided DataFrame to a Google Sheets spreadsheet.

    This function takes a pandas DataFrame, fills any NaN values with empty strings,
    flattens any lists within the DataFrame, converts it to a list of lists, and then
    updates the specified range in the Google Sheets spreadsheet with the DataFrame's values.

    Args:
        new_db (pd.DataFrame): The DataFrame to be sent to the spreadsheet.
        spreadsheet_id (str): The ID of the Google Sheets spreadsheet.
        range_ (str): The A1 notation of the range to update in the spreadsheet.

    Returns:
        None
    """
    new_db = new_db.fillna("")
    new_db = new_db.map(flatten_list)
    new_db = new_db.values.tolist()
    body = {
        'values': new_db
    }
    sheets.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=range_, valueInputOption="USER_ENTERED", body=body).execute()

def begin_process(signal, Range_date, Range_members, Range_play, Range_banned):
    """
    Initiates the process of extracting, creating, and sending play data to a spreadsheet.
    Parameters:
    signal (bool): A flag to start the process.
    Range_date (str): The range in the spreadsheet for play dates.
    Range_members (str): The range in the spreadsheet for play members.
    Range_play (str): The range in the spreadsheet for play details.
    Range_banned (str): The range in the spreadsheet for banned members.
    Returns:
    None
    """


    while signal:
        play_dates, play_members, play, banned_df = extract_spreadsheet_values(Range_date, Range_members, Range_play, Range_banned)

        play_name, play_actor, play_lights, play_sound, play_responsible = create_play(play)
        plays = creating_Play_objects(play_name, play_actor, play_lights, play_sound, play_responsible)

        banned = creating_banned_objects(banned_df)

        new_db, count_df = play_date(play_dates, plays, play_members, banned)

        send_to_spreadsheet(new_db, SPREADSHEETS_ID, "'Görev Listesi 24-25'!D119")
        
        #şu anlık bakımda
        #send_to_spreadsheet(count_df, SPREADSHEETS_ID, "'Görev Listesi 24-25'!G119")
        break

def main():
    """
    Main function to load spreadsheet ranges and process signals in a loop.
    This function performs the following steps:
    1. Loads the spreadsheet ranges for signal, date range, members range, play range, and banned range.
    2. Enters an infinite loop where it checks if the signal is on.
    3. If the signal is on, it begins processing with the loaded ranges.
    4. If the signal is off, it prints a message indicating that the signal is off.
    5. Sleeps for 3600 seconds (1 hour) before repeating the loop.
    Note:
        This function assumes the existence of the following helper functions:
        - load_spreadsheet_ranges(): Loads and returns the necessary spreadsheet ranges.
        - begin_process(signal, Range_date, Range_members, Range_play, Range_banned): Processes the signal with the given ranges.
    """

    signal, Range_date, Range_members, Range_play, Range_banned = load_spreadsheet_ranges()

    while True:
        if signal:
            begin_process(signal, Range_date, Range_members, Range_play, Range_banned)
        else:
            print("Signal is off")
        sleep(3600)

main()
