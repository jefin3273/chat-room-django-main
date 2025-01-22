from django.shortcuts import redirect
from django.urls import reverse

class AuthRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
    # Skip middleware for admin urls
        if request.path.startswith('/admin/'):
            return self.get_response(request)
                    
        # Your existing middleware logic
        if not request.user.is_authenticated and not request.path.startswith('/login/') and not request.path.startswith('/register/'):
            return redirect('chat:login')
                
        return self.get_response(request)