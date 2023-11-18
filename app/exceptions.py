from fastapi import  HTTPException,status


class BookingException(HTTPException): 
    status_code = 500 # <-- задаем значения по умолчанию
    detail = ""
    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)

class UserAlreadyExistsException(BookingException):
    status_code=status.HTTP_409_CONFLICT
    detail="user already exists"


class IncorrectEmailOfPassword(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="incorrect email or password"

class TokenExpiredException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="token is not valid"

class TokenAbsentException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="token is a absente"

class IncorrectTokenFormatException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="incorrect token format"

class UserIsNotPresentException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED

class RoomCannotBeBooked(BookingException):
    status_code=status.HTTP_409_CONFLICT
    detail='room cannt be booked'

class IsToLongPeriodToBooked(BookingException):
    status_code=status.HTTP_400_BAD_REQUEST
    detail="you cannot booked room more then 1 mounth"
    
class ErrorOrderOfDates(BookingException):
    status_code=status.HTTP_400_BAD_REQUEST
    detail="Incorrect order of dates"
    