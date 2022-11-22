import datetime
import re

from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
import csv
import codecs

from .models import Hospital
from .serializers import HospitalSerializer, FileUploadSerializer
from rest_framework import viewsets, filters


class CSVAdapter():
    def __init__(self, data):
        self.client_name = str(data.get('client_name'))
        self.client_org = str(data.get('client_org'))
        self._payment_number = int(data.get('№'))
        self._sum = data.get('sum')
        self._date = data.get('date')
        self._service = data.get('service')

    @property
    def sum(self):
        sum = float(self._sum.replace(",", "."))
        if isinstance(sum, float):
            return sum
        else:
            raise ValueError('This is not a number!')

    @property
    def service(self):
        is_word = re.match(r'[а-яА-Яa-zA-Z0-9]', self._service)
        if is_word:
            return self._service
        else:
            raise ValueError('Its not a word')

    @property
    def date(self):
        try:
            return datetime.datetime.strptime(self._date, '%d.%m.%Y')
        except ValueError:
            raise ValueError("Not valid format!")

    @property
    def payment_number(self):
        if isinstance(self._payment_number, int):
            return self._payment_number
        else:
            raise ValueError("Only integer!")


class HospitalViewSet(viewsets.ModelViewSet):
    serializer_class = HospitalSerializer
    queryset = Hospital.objects.all()
    filter_backends = [filters.OrderingFilter,filters.SearchFilter]
    ordering_fields = ['client_org', 'client_name']
    search_fields = ['client_name', 'client_org']


class UploadFileView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = FileUploadSerializer
    queryset = Hospital.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = serializer.validated_data['file']
        csvReader = csv.DictReader(codecs.iterdecode(file.file, 'utf-8'))
        for rows in csvReader:
            save_to_db(CSVAdapter(rows))
        return Response({"status": "success"},
                        status.HTTP_201_CREATED)


def save_to_db(data):
    obj = Hospital(
        client_name=data.client_name,
        client_org=data.client_org,
        number=data.payment_number,
        sum=data.sum,
        date=data.date,
        service=data.service
    )
    obj.save()
