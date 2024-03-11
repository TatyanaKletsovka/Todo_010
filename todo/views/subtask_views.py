from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import (
    get_object_or_404,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework import status

from todo.models.subtask_models import SubTask
from todo.serializers.subtask_serializers import (
    SubTaskInfoSerializer,
    ListSubTasksSerializer
)
from todo.success_messages import (
    SUBTASK_CREATED_MESSAGE,
    SUBTASK_UPDATED_MESSAGE,
    SUBTASK_DELETED_MESSAGE,
)


class SubTasksListGenericView(ListCreateAPIView):
    serializer_class = ListSubTasksSerializer

    def get_queryset(self):
        queryset = SubTask.objects.select_related('creator')
        username = self.request.query_params.get('username')

        if username:
            queryset = queryset.filter(
                creator__username=username
            )
        return queryset

    def get(self, request: Request, *args, **kwargs):
        data = self.get_queryset()

        if data.exists():
            serializer = self.serializer_class(
                instance=data,
                many=True
            )

            return Response(
                status=status.HTTP_200_OK,
                data=serializer.data
            )

        return Response(
            status=status.HTTP_204_NO_CONTENT,
            data=[]
        )

    def post(self, request: Request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            status=status.HTTP_201_CREATED,
            data={
                "message": SUBTASK_CREATED_MESSAGE,
                "data": serializer.data
            }
        )


class SubTaskDetailGenericView(RetrieveUpdateDestroyAPIView):
    serializer_class = SubTaskInfoSerializer

    def get_object(self):
        subtask_id = self.kwargs.get("subtask_id")

        subtask = get_object_or_404(SubTask, id=subtask_id)

        return subtask

    def get(self, request: Request, *args, **kwargs):
        subtask = self.get_object()

        serializer = self.serializer_class(subtask)

        return Response(
            status=status.HTTP_200_OK,
            data=serializer.data
        )

    def put(self, request: Request, *args, **kwargs):
        subtask = self.get_object()

        serializer = self.serializer_class(subtask, data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(
                status=status.HTTP_200_OK,
                data={
                    "message": SUBTASK_UPDATED_MESSAGE,
                    "data": serializer.data
                }
            )
        else:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data=serializer.errors
            )

    def delete(self, request, *args, **kwargs):
        subtask = self.get_object()

        subtask.delete()

        return Response(
            status=status.HTTP_200_OK,
            data=SUBTASK_DELETED_MESSAGE
        )
