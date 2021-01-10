
role_name_min_length = 3
role_name_max_length = 30

new_role_schema = {
    'properties': {
        'name': {
            'type': 'string',
            'minLength': role_name_min_length,
            'maxLength': role_name_max_length
        }
    },
    'required': ['name']
}
