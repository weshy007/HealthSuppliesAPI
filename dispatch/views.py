from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import DispatchSerializer
from .models import Dispatch
from rest_framework import permissions
from .permissions import IsOwner

# Create your views here.
class DispatchListAPIView(ListCreateAPIView):
    serializer_class = DispatchSerializer
    queryset = Dispatch.objects.all()
    permission_classes=(permissions.IsAuthenticated,)
    
    
    def perform_create(self, serializer):
        return serializer.save(donor=self.request.user)
    
    def get_queryset(self):
        return self.queryset.filter(donor=self.request.user)
    
    
class DispatchDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = DispatchSerializer
    queryset = Dispatch.objects.all()
    permission_classes=(permissions.IsAuthenticated,IsOwner,)
    lookup_field="id"
    
    
    def perform_create(self, serializer):
        return serializer.save(donor=self.request.user)
    
    def get_queryset(self):
        return self.queryset.filter(donor=self.request.user)   

