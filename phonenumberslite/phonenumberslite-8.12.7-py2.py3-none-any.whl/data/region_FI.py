"""Auto-generated file, do not edit by hand. FI metadata"""
from ..phonemetadata import NumberFormat, PhoneNumberDesc, PhoneMetadata

PHONE_METADATA_FI = PhoneMetadata(id='FI', country_code=358, international_prefix='00|99(?:[01469]|5(?:[14]1|3[23]|5[59]|77|88|9[09]))',
    general_desc=PhoneNumberDesc(national_number_pattern='[1-35689]\\d{4}|7\\d{10,11}|(?:[124-7]\\d|3[0-46-9])\\d{8}|[1-9]\\d{5,8}', possible_length=(5, 6, 7, 8, 9, 10, 11, 12)),
    fixed_line=PhoneNumberDesc(national_number_pattern='(?:1[3-79][1-8]|[235689][1-8]\\d)\\d{2,6}', example_number='131234567', possible_length=(5, 6, 7, 8, 9)),
    mobile=PhoneNumberDesc(national_number_pattern='(?:4[0-8]|50)\\d{4,8}', example_number='412345678', possible_length=(6, 7, 8, 9, 10)),
    toll_free=PhoneNumberDesc(national_number_pattern='800\\d{4,6}', example_number='800123456', possible_length=(7, 8, 9)),
    premium_rate=PhoneNumberDesc(national_number_pattern='[67]00\\d{5,6}', example_number='600123456', possible_length=(8, 9)),
    uan=PhoneNumberDesc(national_number_pattern='20\\d{4,8}|60[12]\\d{5,6}|7(?:099\\d{4,5}|5[03-9]\\d{3,7})|20[2-59]\\d\\d|(?:606|7(?:0[78]|1|3\\d))\\d{7}|(?:10|29|3[09]|70[1-5]\\d)\\d{4,8}', example_number='10112345', possible_length=(5, 6, 7, 8, 9, 10, 11, 12)),
    no_international_dialling=PhoneNumberDesc(national_number_pattern='20(?:2[023]|9[89])\\d{1,6}|(?:60[12]\\d|7099)\\d{4,5}|(?:606|7(?:0[78]|1|3\\d))\\d{7}|(?:[1-3]00|7(?:0[1-5]\\d\\d|5[03-9]))\\d{3,7}', possible_length=(5, 6, 7, 8, 9, 10, 11, 12)),
    preferred_international_prefix='00',
    national_prefix='0',
    national_prefix_for_parsing='0',
    number_format=[NumberFormat(pattern='(\\d{5})', format='\\1', leading_digits_pattern=['75[12]'], national_prefix_formatting_rule='0\\1'),
        NumberFormat(pattern='(\\d)(\\d{4,9})', format='\\1 \\2', leading_digits_pattern=['[2568][1-8]|3(?:0[1-9]|[1-9])|9'], national_prefix_formatting_rule='0\\1'),
        NumberFormat(pattern='(\\d{6})', format='\\1', leading_digits_pattern=['11']),
        NumberFormat(pattern='(\\d{3})(\\d{3,7})', format='\\1 \\2', leading_digits_pattern=['[12]00|[368]|70[07-9]'], national_prefix_formatting_rule='0\\1'),
        NumberFormat(pattern='(\\d{2})(\\d{4,8})', format='\\1 \\2', leading_digits_pattern=['[1245]|7[135]'], national_prefix_formatting_rule='0\\1'),
        NumberFormat(pattern='(\\d{2})(\\d{6,10})', format='\\1 \\2', leading_digits_pattern=['7'], national_prefix_formatting_rule='0\\1')],
    intl_number_format=[NumberFormat(pattern='(\\d)(\\d{4,9})', format='\\1 \\2', leading_digits_pattern=['[2568][1-8]|3(?:0[1-9]|[1-9])|9']),
        NumberFormat(pattern='(\\d{3})(\\d{3,7})', format='\\1 \\2', leading_digits_pattern=['[12]00|[368]|70[07-9]']),
        NumberFormat(pattern='(\\d{2})(\\d{4,8})', format='\\1 \\2', leading_digits_pattern=['[1245]|7[135]']),
        NumberFormat(pattern='(\\d{2})(\\d{6,10})', format='\\1 \\2', leading_digits_pattern=['7'])],
    main_country_for_code=True,
    leading_digits='1[03-79]|[2-9]',
    mobile_number_portable_region=True)
