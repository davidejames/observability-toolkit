#┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅#
# SPDX-FileCopyrightText: © 2024 David E. James
# SPDX-License-Identifier: MIT
# SPDX-FileType: SOURCE
#┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈#

import logging


def _ensure_callable(var, default=None):
    if callable(var):
        return var

    if var is not None:
        return lambda *args, **kwargs: var

    if callable(default) and not inspect.isclass(default):
        return default

    return lambda *args, **kwargs: default


def _apply(item, func):
    if isinstance(item, list):
        for _item in item:
            func(_item)
    else:
        func(item)



def _get_logging_subscribers(logging_config=None, logger=None):
    _logging_config = logging_config or LoggingDefaults.LOG_CONFIG
    _default_logger = LoggingDefaults.LOGGER
    _default_level  = LoggingDefaults.LOG_LEVEL
    _default_msg_t  = LoggingDefaults.LOG_MSG_T

    subscriptions = dict()

    for key, cfg in _logging_config.items():
        logger_f = _ensure_callable(cfg.get('logger'), _default_logger)
        level_f  = _ensure_callable(cfg.get('level '), _default_level )
        msg_t_f  = _ensure_callable(cfg.get('msg_t' ), _default_msg_t )

        def _log(event, obj, context, *args, **kwargs):
            logger = logger_f(event=event, obj=obj, context=context)
            level  = level_f( event=event, obj=obj, context=context)
            msg_t  = msg_t_f( event=event, obj=obj, context=context)

            msg = msg_t.format(event=event.name, **context)
            logger.log(level, msg, extra=kwargs)

        subscriptions[key] = _log

    return subscriptions



class PubSubManager:
    def __init__(self, enum_obj, subscriptions=None, *, logger=None):
        self.event_list = list(enum_obj)
        self.subs = {e:[] for e in self.event_list}

        self.logger = logger or logging.getLogger(__name__)

        self.subscribe_all(subscriptions)


    def subscribe(self, event, subscriber, *, on_success=None, on_error=None):
        BAD_TYPE_MSG = '{s} is invalid subscription for {e}'
        SUCCESS_MSG  = '{s} subscribed to {e}'

        on_success = _ensure_callable(on_success)
        on_error   = _ensure_callable(on_error)
        success = True

        def _sub(sub):
            nonlocal success
            if not callable(sub):
                _msg = BAD_TYPE_MSG.format(s=sub, e=event)
                self.logger.warning(_msg)
                on_error(event, sub, _msg)
                success = False
            else:
                self.subs[event].append(sub)
                _msg = SUCCESS_MSG.format(s=sub, e=event)
                self.logger.info(_msg)
                on_success(event, sub, _msg)

        _apply(subscriber, _sub)

        return success


    def unsubscribe(self, event, subscriber, *, on_success=None, on_error=None):
        on_success = _ensure_callable(on_success)
        on_error   = _ensure_callable(on_error)
        success = True

        def _unsubscribe(sub):
            nonlocal success
            _subs = self.subs[event]
            if sub not in _subs:
                _msg = f'"{s}" is not a subscriber'
                self.logger.warning(_msg)
                on_error(event, sub, _msg)
                success = False
            else:
                _subs.remove(sub)
                _msg = f'removed {sub}'
                self.logger.info(_msg)
                on_success(event, sub, _msg)

        _apply(subscriber, _unsubscribe)

        return success


    def subscribe_all(self, subscriptions, *, on_success=None, on_error=None):
        if subscriptions is None:
            return

        if not isinstance(subscriptions, dict):
            raise ValueError('subscriptions must be a dictionary')

        success = True

        #┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈ ┈
        for event in self.subs.keys():
            _sub = subscriptions.get(event)
            if _sub is None:
                continue

            _success = self.subscribe(event, _sub,
                                      on_success=on_success,
                                      on_error=on_error
                                    )

            success = success and _success

        return success


    async def async_publish(self, event, context=None, on_error=None, *args, **kwargs):
        _subs = subscriptions.get(event)
        if _subs is None:
            return

        success = True
        for _sub in _subs:
            try:
                await _acall_f(_sub, event, context, *args, **kwargs)
            except Exception as e:
                success = False
                if on_error is not None:
                    on_error(event, context, *args, **kwargs)
                self.logger.exception(f'publish error: {event}, {context}, {_sub}')


        return errors


    def publish(self, event, context=None, on_error=None, *args, **kwargs):
        _subs = self.subs.get(event)
        if _subs is None:
            return

        success = True
        for _sub in _subs:
            try:
                _sub(event, context, *args, **kwargs)
            except Exception as e:
                success = False
                if on_error is not None:
                    on_error(event, context, *args, **kwargs)
                self.logger.exception(f'publish error: {event}, {context}, {_sub}')

        return success


