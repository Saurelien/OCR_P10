from rest_framework.pagination import PageNumberPagination

class CustomPageNumberPagination(PageNumberPagination):
    def get_next_link(self):
        if not self.next_page_number:
            return None
        return f"/api/project/?page={self.next_page_number}"

    def get_previous_link(self):
        if not self.previous_page_number:
            return None
        return f"/api/project/?page={self.previous_page_number}"


