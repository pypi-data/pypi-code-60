"""Auto-generated file, do not edit by hand. VC metadata"""
from ..phonemetadata import NumberFormat, PhoneNumberDesc, PhoneMetadata

PHONE_METADATA_VC = PhoneMetadata(id='VC', country_code=None, international_prefix=None,
    general_desc=PhoneNumberDesc(national_number_pattern='9\\d\\d', possible_length=(3,)),
    toll_free=PhoneNumberDesc(national_number_pattern='9(?:11|99)', example_number='911', possible_length=(3,)),
    emergency=PhoneNumberDesc(national_number_pattern='9(?:11|99)', example_number='911', possible_length=(3,)),
    short_code=PhoneNumberDesc(national_number_pattern='9(?:11|99)', example_number='911', possible_length=(3,)),
    short_data=True)
