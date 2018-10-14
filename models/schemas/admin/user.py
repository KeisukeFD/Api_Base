
username_min_length = 3
username_max_length = 50
email_pattern = '^[\w\.\+-\]+@[\w\.-]+\.\w{2,6}$'
password_min_length = 12

new_user_schema = {
    'properties': {
        'username': {
            'type': 'string',
            'minLength': username_min_length,
            'maxLength': username_max_length
        },
        'email': {
            'type': 'string',
            'pattern': email_pattern
        },
        'password': {
            'type': 'string',
            'minLength': password_min_length
        },
        'roles': {
            'type': 'array',
            'items': {
                'type': 'integer'
            },
            'uniqueItems': True
        }
    },
    'required': ['username', 'email', 'password']
}

edit_user_schema = {
    'properties': {
        'username': {
            'type': 'string',
            'minLength': username_min_length,
            'maxLength': username_max_length
        },
        'email': {
            'type': 'string',
            'pattern': email_pattern
        },
        'password': {
            'type': 'string',
            'minLength': password_min_length
        },
    },
}

user_roles_schema = {
    'properties': {
        'roles': {
            'type': 'array',
            'items': {
                'type': 'integer'
            },
            'uniqueItems': True
        }
    },
}



