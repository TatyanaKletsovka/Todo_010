from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import (
    get_object_or_404,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework import status

from todo.models.task_models import Task
from todo.serializers.task_serializers import AllTasksSerializer, TaskInfoSerializer
from todo.success_messages import TASK_CREATED_MESSAGE, TASK_UPDATED_MESSAGE, TASK_DELETED_MESSAGE


class TasksListGenericView(ListCreateAPIView):
    serializer_class = AllTasksSerializer

    def get_queryset(self):
        queryset = Task.objects.select_related('category')
        category = self.request.query_params.get("category")

        if category:
            queryset = queryset.filter(
                category__name=category
            )

        return queryset

    def get(self, request: Request, *args, **kwargs):
        filtered_data = self.get_queryset()

        if filtered_data.exists():
            serializer = self.serializer_class(
                instance=filtered_data,
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
                "message": TASK_CREATED_MESSAGE,
                "data": serializer.data
            }
        )


class TaskDetailGenericView(RetrieveUpdateDestroyAPIView):
    serializer_class = TaskInfoSerializer

    def get_object(self):
        task_id = self.kwargs.get("task_id")

        task = get_object_or_404(Task, id=task_id)

        return task

    def get(self, request: Request, *args, **kwargs):
        task = self.get_object()

        serializer = self.serializer_class(task)

        return Response(
            status=status.HTTP_200_OK,
            data=serializer.data
        )

    def put(self, request: Request, *args, **kwargs):
        task = self.get_object()

        serializer = self.serializer_class(task, data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(
                status=status.HTTP_200_OK,
                data={
                    "message": TASK_UPDATED_MESSAGE,
                    "data": serializer.data
                }
            )
        else:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data=serializer.errors
            )

    def delete(self, request, *args, **kwargs):
        task = self.get_object()

        task.delete()

        return Response(
            status=status.HTTP_200_OK,
            data=TASK_DELETED_MESSAGE
        )
