from pydantic import BaseModel
from typing import List, Optional

class Dependent(BaseModel):
    firstName: str
    lastName: Optional[str]
    dateOfBirth: Optional[str]
    age: int
    upcomingBirthday: Optional[str]
    cityOfResidence: Optional[str]
    email: Optional[str]
    phoneNumber: Optional[str]
    nationality: Optional[str]
    mainInterests: List[str]
    socialMediaLinks: Optional[List[str]]
    loyaltyPrograms: Optional[List[str]]
    passions: List[str]
    lifestyle: List[str]
    travelDocuments: Optional[List[str]]
    typeOfTravel: Optional[List[str]]
    travelSpan: Optional[List[str]]
    travelBucketList: Optional[List[str]]
    specialRequirements: Optional[List[str]]

class Customer(BaseModel):
    id: str
    firstName: str
    lastName: str
    dateOfBirth: Optional[str]
    age: int
    upcomingBirthday: Optional[str]
    cityOfResidence: Optional[str]
    email: Optional[str]
    phoneNumber: Optional[str]
    nationality: Optional[str]
    mainInterests: List[str]
    socialMediaLinks: Optional[List[str]]
    loyaltyPrograms: Optional[List[str]]
    passions: List[str]
    lifestyle: List[str]
    travelDocuments: Optional[List[str]]
    typeOfTravel: List[str]
    travelSpan: List[str]
    travelBucketList: List[str]
    specialRequirements: Optional[List[str]]
    dependents: List[Dependent]

class GroupInput(BaseModel):
    id: str
    groupName: str
    userName: Optional[str]
    password: Optional[str]
    customers: List[Customer]
    augmentedData: Optional[str]
