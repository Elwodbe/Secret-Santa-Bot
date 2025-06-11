from aiogram.fsm.state import State,StatesGroup

class CreateRoomState(StatesGroup):
    room_name = State()