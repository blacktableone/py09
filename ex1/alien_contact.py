from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, ValidationError, model_validator


class ContactType(str, Enum):
    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: Optional[str] = Field(default=None, max_length=500)
    is_verified: bool = False

    @model_validator(mode='after')
    def check_business_rules(self) -> "AlienContact":
        """Cross-field rules that run after all fields are validated."""
        # R1: Contact ID must start with "AC" (Alien Contact)
        if not self.contact_id.startswith("AC"):
            raise ValueError('Contact ID must start with "AC"')
        # R2: Physical contact reports must be verified
        if (
            self.contact_type == ContactType.PHYSICAL
            and not self.is_verified
        ):
            raise ValueError('Physical contact reports must be verified')
        # R3: Telepathic contact requires at least 3 witnesses
        if (
            self.contact_type == ContactType.TELEPATHIC
            and self.witness_count < 3
        ):
            raise ValueError(
                'Telepathic contact requires at least 3 witnesses'
            )
        # R4: Strong signals (> 7.0) should include received messages
        if (
            self.signal_strength > 7.0
            and not self.message_received
        ):
            raise ValueError(
                'Strong signals (> 7.0) should include received messages'
            )

        # A model_validator in "after" mode must return the model itself
        return self


def main() -> None:
    print("Alien Contact Log Validation")
    print("=" * 38)

    # A valid report (the timestamp string is converted to datetime)
    contact = AlienContact(
        contact_id="AC_2024_001",
        timestamp=datetime(2024, 5, 17, 23, 45),
        location="Area 51, Nevada",
        contact_type=ContactType.RADIO,
        signal_strength=8.5,
        duration_minutes=45,
        witness_count=5,
        message_received="Greetings from Zeta Reticuli",
    )
    print("Valid contact report:")
    print(f"ID: {contact.contact_id}")
    print(f"Type: {contact.contact_type.value}")
    print(f"Location: {contact.location}")
    print(f"Signal: {contact.signal_strength}/10")
    print(f"Duration: {contact.duration_minutes} minutes")
    print(f"Witnesses: {contact.witness_count}")
    print(f"Message: '{contact.message_received}'")

    print("\n")
    print("=" * 38)
    print("Expected validation error:")

    # An invalid report: telepathic contact with only 1 witness
    try:
        AlienContact(
            contact_id="AC_2024_002",
            timestamp=datetime.now(),
            location="Rotterdam",
            contact_type=ContactType.TELEPATHIC,
            signal_strength=3.0,
            duration_minutes=10,
            witness_count=1,
        )
    except ValidationError as error:
        message = error.errors()[0]["msg"]
        print(message.removeprefix("Value error, "))


if __name__ == "__main__":
    main()
