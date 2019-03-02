import math

from rest_framework import serializers


class AppBaseSerializer(serializers.Serializer):
    success = serializers.SerializerMethodField(method_name='is_success')
    full_messages = serializers.SerializerMethodField()

    def get_full_messages(self, data):
        return []

    def get_full_messages(self, data):
        if type(data) == list:
            return data
        elif type(data) == str:
            return [data]


class SuccessSerializer(AppBaseSerializer):

    def is_success(self, data):
        return True


class ErrorSerializer(serializers.Serializer):

    def is_success(self, data):
        return False


class PageMetaSerializer():
    def __init__(self, request, paginator):
        if not hasattr(paginator, 'count'):
            return
        self.data = {}
        self.data['total_items_count'] = paginator.count
        self.data['offset'] = paginator.offset
        self.data['requested_page_size'] = paginator.limit
        self.data['current_page_number'] = int(request.query_params.get('page', 1))

        self.data['prev_page_number'] = 1
        self.data['total_pages_count'] = math.ceil(self.data['total_items_count'] / self.data['requested_page_size'])

        if self.data['current_page_number'] < self.data['total_pages_count']:
            self.data['has_next_page'] = True
            self.data['next_page_number'] = self.data['current_page_number'] + 1
        else:
            self.data['has_next_page'] = False
            self.data['next_page_number'] = 1

        if self.data['current_page_number'] > 1:
            self.data['prev_page_number'] = self.data['current_page_number'] - 1
        else:
            self.data['has_prev_page'] = False
            self.data['prev_page_number'] = 1

        self.data['next_page_url'] = '%s?page=%d&page_size=%d' % (
            request.path, self.data['next_page_number'], self.data['requested_page_size'])
        self.data['prev_page_url'] = '%s?page=%d&page_size=%d' % (
            request.path, self.data['prev_page_number'], self.data['requested_page_size'])

        # self.paginator.default_limit

        # self.paginator.offset_query_param
        # self.paginator.limit_query_param

    def get_data(self):
        return self.data
