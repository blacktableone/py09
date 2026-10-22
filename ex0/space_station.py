from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ValidationError


class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = True
    notes: Optional[str] = Field(default=None, max_length=200)


def main() -> None:
    print("Space Station Data Validation")
    print("=" * 40)

    # A valid station (the timestamp string is auto-converted to datetime)
    station = SpaceStation(
        station_id="ISS001",
        name="International Space Station",
        crew_size=6,
        power_level=85.5,
        oxygen_level=92.3,
        last_maintenance="2026-10-22T10:00:00",  # type: ignore[arg-type]
    )
    print("Valid station created:")
    print("Valid station created:")
    print(f"ID: {station.station_id}")
    print(f"Name: {station.name}")
    print(f"Crew: {station.crew_size} people")
    print(f"Power: {station.power_level}%")
    print(f"Oxygen: {station.oxygen_level}%")
    print(
        f"Status: "
        f"{'Operational' if station.is_operational else 'Offline'}"
    )

    print("\n")
    print("=" * 40)

    try:
        SpaceStation(
            station_id="BAD001",
            name="Overvrowded Station",
            crew_size=25,
            power_level=50.0,
            oxygen_level=50.0,
            last_maintenance=datetime.now(),
        )
    except ValidationError as error:
        print("Expected validation error:")
        print(error.errors()[0]["msg"])
        print("*" * 40)
        print(type(error))


if __name__ == "__main__":
    main()
