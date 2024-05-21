import fire
import structlog
import sys
import os
from dotenv import load_dotenv
from ms_active_directory import ADDomain, AD_ATTRIBUTE_GET_ALL_NON_VIRTUAL_ATTRS

load_dotenv()
AD_DOMAIN = os.environ.get('AD_DOMAIN')
AD_USERNAME = os.environ.get('AD_USERNAME')
AD_PASSWORD = os.environ.get('AD_PASSWORD')

logger: structlog.stdlib.BoundLogger = structlog.get_logger()


def lookup(attribute: str, value: str):
    """Lookup a user's information by the value of some attribute."""

    # check that the environment variables are set
    if not AD_DOMAIN:
        logger.error('AD_DOMAIN environment variable is not set.')
        sys.exit(1)
    
    if not AD_USERNAME:
        logger.error('AD_USERNAME environment variable is not set.')
        sys.exit(1)

    if not AD_PASSWORD:
        logger.error('AD_PASSWORD environment variable is not set.')
        sys.exit(1)
    
    domain = ADDomain(AD_DOMAIN)
    session = domain.create_session_as_user(AD_USERNAME, AD_PASSWORD)

    logger.debug('Looking up user by attribute and value', attribute=attribute, value=value)
    users = session.find_users_by_attribute(
        attribute_name=attribute,
        attribute_value=value,
        attributes_to_lookup=['manager']
        )
    
    if not users:
        logger.error('Found no users for query.', attribute=attribute, value=value)
        sys.exit(1)
    elif len(users) > 1:
        logger.warning('Found %d users; using the first user.', len(users))
        user = users[0]
    else:
        user = users[0]
    
    for k, v in sorted(user.all_attributes.items(), key=(lambda k: k)):
        logger.info(f'"{k}": "{v}"')


if __name__ == '__main__':
    fire.Fire(lookup)