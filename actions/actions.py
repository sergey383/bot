from typing import Dict, Text, Any, List, Union, Optional

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, ConversationPaused, EventType
from rasa_sdk.types import DomainDict

from fuzzywuzzy import process


class ValidateElicitationForm(FormValidationAction):   

    def name(self) -> Text:
        return "validate_elicitation_form"
    
    async def required_slots(
        self,
        domain_slots: List[Text],
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> List[Text]:
        updated_slots = domain_slots.copy()
        if tracker.slots.get("not_appreciated") is True:
            updated_slots.remove("importance")
        if tracker.slots.get("not_appreciated") is False:
            updated_slots.remove("problem")
            updated_slots.remove("desired_outcome")
        return updated_slots

    # validate user answers
    @staticmethod
    def answers_db() -> Dict[str, List]:
        return {
            "job_function": [
                "manager",
                "ceo",
                "cfo",
                "cto",
                "developer",
                "project manager",
                "product manager",
                "janitor",
                "full stack developer",
                "machine learning engineer",
                "serve meals",
                "student",
                "software engineer",
                "lead engineer",
                "ai engineer"
            ],
            "region": [
                "us east",
                "us west",
                "asia pacific",
                "europe",
                "middle east",
                "south africa",
                "canada"
            ]
        }

    def create_validation_function(name_of_slot):

        def validate_slot(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
        ) -> Dict[Text, Any]:

            if value.lower() in self.answers_db()[name_of_slot]:
                return {name_of_slot: value}
            else:
                # find the closest answer by some measure (edit distance for now, semantic over time) 
                choices = self.answers_db()[name_of_slot]
                answer = process.extractOne(value.lower(), choices)

                if answer[1] < 45:
                    return {name_of_slot: "other"}
                else:
                    return {name_of_slot: answer[0]}

        return validate_slot

    validate_job_function = create_validation_function(name_of_slot="job_function")
    validate_region = create_validation_function(name_of_slot="region")

class DataPointInform(Action):
    
    def name(self) -> Text:

        return "data_point_inform"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[EventType]:
        data_point = tracker.latest_message['intent'].get('name')
        dispatcher.utter_message(response="utter_"+data_point)
        if 'not' in data_point:
            return [SlotSet(data_point.replace("not_",""), tracker.latest_message.get("text")), SlotSet("not_appreciated", True)]
        else:
            return [SlotSet(data_point, tracker.latest_message.get("text")), SlotSet("not_appreciated", False)] 

class DataPointReVisit(Action):
    
    def name(self) -> Text:

        return "data_point_revisit"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[EventType]:
        return [SlotSet("appreciated", None), SlotSet("importance", None), SlotSet("problem", None),  SlotSet("desired_outcome", None), SlotSet("not_appreciated", None)]

class PauseConversation(Action):

    def name(self) -> Text:

        return "pause_conversation"

    def run(self, dispatcher, tracker, domain):

        return [ConversationPaused()]
