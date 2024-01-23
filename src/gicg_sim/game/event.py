from enum import Enum

class EventType(Enum):
    GAME_START = "GAME_START"
    ROUND_START = "ROUND_START"
    CHARACTER_TURN_START = "CHARACTER_TURN_START"
    CHARACTER_TURN_END = "CHARACTER_TURN_END"
    ROUND_END = "ROUND_END"
    GAME_END = "GAME_END"
    

class Event:
    def __init__(self, event_type: EventType, **kwargs):
        self.event_type = event_type
        self.kwargs = kwargs
        

class EventRound(Event):
    def __init__(self, event_type: EventType, round_num: int, **kwargs):
        super().__init__(event_type, round_num=round_num, **kwargs)
        self.round_num = round_num
        

class EventCharacterTurn(Event):
    def __init__(self, event_type: EventType, character_id: int, **kwargs):
        super().__init__(event_type, character_id=character_id, **kwargs)
        self.character_id = character_id