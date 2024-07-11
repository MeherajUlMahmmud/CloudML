class CacheKeyMixin:
    def get_cache_key(self, request, view_name):
        # Create a unique cache key based on user and query parameters
        user_id = request.user.id if request.user.is_authenticated else 'anonymous'
        params = request.query_params.urlencode()
        return f'{view_name}_{user_id}_{params}'
