def rate_limit(limit: int, key=None):
    """
    Декоратор для настройки ограничения скорости и ключа в различных функциях.

    :param limit:
    :param key:
    :return:
    """

    def decorator(func):
        setattr(func, 'throttling_rate_limit', limit)
        if key:
            setattr(func, 'throttling_key', key)
        return func

    return decorator
