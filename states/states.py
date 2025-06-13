from aiogram.fsm.state import State,StatesGroup

class CreateRoomState(StatesGroup):
    room_name = State()

class RoomJoiningState(StatesGroup):
    room_id = State()
    fullname = State()
    gender = State()
    about_user = State()
    