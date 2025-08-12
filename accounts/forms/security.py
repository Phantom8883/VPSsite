from django.core.cache import cache

MAX_ATTEMPTS = 5
BLOCK_TIME = 300  # 5 минут

def is_blocked(identifier):
    key = f"login_attempts:{identifier}"
    attempts = cache.get(key, 0)
    return attempts >= MAX_ATTEMPTS

def register_attempt(identifier):
    key = f"login_attempts:{identifier}"
    attempts = cache.get(key, 0)
    cache.set(key, attempts + 1, timeout=BLOCK_TIME)

def reset_attempts(identifier):
    cache.delete(f"login_attempts:{identifier}")

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
