from flask import jsonify
from services.loggers import LoggerService


def error(*messages):
    if isinstance(messages[0], list):
        LoggerService.instance().debug('Return to user: %s' % [msg for msg in messages[0]])
        return jsonify({
            'error': True,
            'messages': [msg for msg in messages[0]]
        })
    LoggerService.instance().debug('Return to user: %s' % [msg for msg in messages])
    return jsonify({
        'error': True,
        'messages': [msg for msg in messages]
    })


def success(message, **kwargs):
    LoggerService.instance().info('Return to user: %s' % message)
    default = {
        'error': False,
        'message': message
    }
    default.update(kwargs)
    return jsonify(default)
