from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_core_sdk.events import SlotSet
import sqlite3

class DbQueryingMethods:
    def create_connection(db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
        except sqlite3.Error as e:
            print(e)
        return conn

    def select_by_slot_delivery(conn, slot_value):

        cur = conn.cursor()
        cur.execute(f'''SELECT state from delivery_state WHERE delivery_num="{slot_value}"''')

        rows = cur.fetchall()

        if len(list(rows))<1:
            return "There is no such delivery number."
        else:
            for row in rows:
                message = "Your delivery state is: " + row[0]
        return(message)

    def select_by_slot_city(conn, slot_value):

        cur = conn.cursor()
        cur.execute(f'''SELECT store_location from store_table WHERE city="{slot_value}"''')

        rows = cur.fetchall()

        if len(list(rows))<1:
            return "There are no offline stores."
        else:
            for row in rows:
                message = "The offline stores is in : " + row[0]
        return(message)

    def select_by_slot_mancontact(conn, slot_value):

        cur = conn.cursor()
        cur.execute(f'''SELECT contact from man_table WHERE name="{slot_value}"''')

        rows = cur.fetchall()

        if len(list(rows))<1:
            return "There is no such person."
        else:
            for row in rows:
                message = "His contact way is : " + row[0]
        return(message)

class QueryDeliveryDetails(Action):
    def name(self) -> Text:
        return "action_display_delivery"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        conn = DbQueryingMethods.create_connection(db_file = "sysphonedb/delivery.db")

        slot_value = tracker.get_slot("delivery_num")
        get_query_results = DbQueryingMethods.select_by_slot_delivery(conn=conn,slot_value=slot_value)
        dispatcher.utter_message(text=str(get_query_results))

        return

class QueryCityDetails(Action):
    def name(self) -> Text:
        return "action_provide_city"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        conn = DbQueryingMethods.create_connection(db_file = "sysphonedb/store.db")

        slot_value = tracker.get_slot("city_name")
        get_query_results = DbQueryingMethods.select_by_slot_city(conn=conn,slot_value=slot_value)
        dispatcher.utter_message(text=str(get_query_results))

        return

class QueryManContactDetails(Action):
    def name(self) -> Text:
        return "action_display_man_contact"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        conn = DbQueryingMethods.create_connection(db_file = "sysphonedb/man.db")

        slot_value = tracker.get_slot("personnel_name")
        get_query_results = DbQueryingMethods.select_by_slot_mancontact(conn=conn,slot_value=slot_value)
        dispatcher.utter_message(text=str(get_query_results))

        return

class ActionDisplayModel(Action):

    def name(self) -> Text:
        return "action_display_model"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        model_name = tracker.get_slot("model_name")
        message1 = "OK, Your phone model is {}".format(model_name)
        message2 = "What is your specific problem?"
        dispatcher.utter_message(message1+'\n'+message2)

        return []

class ActionDisplayContact(Action):

    def name(self) -> Text:
        return "action_display_contact"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        contact_way = tracker.get_slot("contact_way")
        message1 = "OK, your contact is {}".format(contact_way)
        message2 = "We will arrange door-to-door service for you as soon as possible.\nDo you have any questions?"
        dispatcher.utter_message(message1+'\n'+message2)

        return []

class ActionDisplayMan(Action):

    def name(self) -> Text:
        return "action_display_manhelp"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        message1 = "We have the following maintenance personnel, please select:"
        message2 = "Frank\tBob\tStark\tLeijun"
        dispatcher.utter_message(message1+'\n'+message2)

        return []
