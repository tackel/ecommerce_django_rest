from rest_framework import generics


# con esta clase que se importa en el general_view y ahorras ponerle a cada clase el get_queryset
# por que obtiene el model mediante el get_serializer() y e la vista todos heredarian de GeneralListApiView
class GeneralListApiView(generics.ListAPIView):
    serializer_class = None

    def get_queryset(self):
        model = self.get_serializer().Meta.model
        return model.objects.filter(state = True)