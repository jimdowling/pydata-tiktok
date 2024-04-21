from mimesis import Generic
from mimesis.locales import Locale
import random
from typing import List, Dict


def generate_users(num_users: int) -> List[Dict[str, str]]:
    """
    Generate a list of dictionaries, each representing a user with various attributes.

    The function creates fake user data including user ID, gender, age, and country
    using the mimesis library. The user ID is generated based on a specified mask.

    Args:
        num_users (int): The number of user profiles to generate.

    Returns:
        List[Dict[str, str]]: A list of dictionaries, each containing details of a user.
    """
    generic = Generic(locale=Locale.EN)
    users = []  # List to store generated user data

    for _ in range(num_users):
        # Generate each user's details
        user = {
            'user_id': generic.person.identifier(mask='@@###@'),  # Unique user identifier
            'gender': generic.person.gender(),  # Randomly generated gender
            'age': random.randint(12, 90),  # Randomly generated age between 12 and 90
            'country': generic.address.country()  # Randomly generated country name
        }
        users.append(user)  # Add the user to the list

    return users
