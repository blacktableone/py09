from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, ValidationError, model_validator


class CrewRanks(str, Enum):
    CADET = "cadet",
    OFFICER = "officer",
    LIEUTENANT = "lieutenant",
    CAPTAIN = "captain",
    COMMANDER = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: CrewRanks
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = True


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = "planned"
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode='after')
    def Mission_Validation_Rules(self) -> "SpaceMission":
        # R1: the mission ID must start with "M"
        if not self.mission_id.startswith('M'):
            raise ValueError('Mission ID must start with "M"')

        # R2: Must have at least one Commander or Captain
        leaders = [
            member
            for member in self.crew
            if member.rank in (CrewRanks.COMMANDER, CrewRanks.CAPTAIN)
        ]
        if not leaders:
            raise ValueError(
                'Must have at least one Commander or Captain'
            )

        # R3: Long missions (> 365 days) need 50% experienced crew (5+ years)
        if self.duration_days > 365:
            experienced = [
                member
                for member in self.crew
                if member.years_experience >= 5
            ]
            if len(experienced) / len(self.crew) < 0.5:
                raise ValueError(
                    'Long missions (> 365 days) need 50%'
                    'experienced crew (5+ years)'
                )

        # R4: All crew members must be active
        if not all(member.is_active for member in self.crew):
            raise ValueError('All crew members must be active')

        return self


def main() -> None:
    print("Space Mission Crew Validation")
    print("=" * 41)

    # A valid mission with a commander and enough experienced crew
    mission = SpaceMission(
        mission_id="M2024_MARS",
        mission_name="Mars Colony Establishment",
        destination="Mars",
        launch_date=datetime(2024, 6, 1),
        duration_days=900,
        crew=[
            CrewMember(
                member_id="C001",
                name="Sarah Connor",
                rank=CrewRanks.COMMANDER,
                age=45,
                specialization="Mission Command",
                years_experience=20,
            ),
            CrewMember(
                member_id="C002",
                name="John Smith",
                rank=CrewRanks.LIEUTENANT,
                age=38,
                specialization="Navigation",
                years_experience=10,
            ),
            CrewMember(
                member_id="C003",
                name="Alice Johnson",
                rank=CrewRanks.OFFICER,
                age=29,
                specialization="Engineering",
                years_experience=3,
            ),
        ],
        budget_millions=2500.0,
    )
    print("Valid mission created:")
    print(f"Mission: {mission.mission_name}")
    print(f"ID: {mission.mission_id}")
    print(f"Destination: {mission.destination}")
    print(f"Duration: {mission.duration_days} days")
    print(f"Budget: ${mission.budget_millions}M")
    print(f"Crew size: {len(mission.crew)}")
    print("Crew members:")
    for member in mission.crew:
        print(
            f"- {member.name} ({member.rank.value}) - "
            f"{member.specialization}"
        )

    print("\n")
    print("=" * 41)
    print("Expected validation error:")

    # An invalid mission: nobody is a Commander or Captain
    try:
        SpaceMission(
            mission_id="M2024_MOON",
            mission_name="Lunar Survey",
            destination="Moon",
            launch_date=datetime(2024, 9, 1),
            duration_days=30,
            crew=[
                CrewMember(
                    member_id="C010",
                    name="Bob Miller",
                    rank=CrewRanks.LIEUTENANT,
                    age=40,
                    specialization="Navigation",
                    years_experience=12,
                ),
                CrewMember(
                    member_id="C011",
                    name="Eve Adams",
                    rank=CrewRanks.CADET,
                    age=22,
                    specialization="Robotics",
                    years_experience=1,
                ),
            ],
            budget_millions=300.0,
        )
    except ValidationError as error:
        message = error.errors()[0]["msg"]
        print(message.removeprefix("Value error, "))


if __name__ == "__main__":
    main()
