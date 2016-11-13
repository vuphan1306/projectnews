"""Paginator."""
from tastypie.paginator import Paginator


class NoLimitPaginator(Paginator):
    """Remove paginator."""

    def get_slice(self, limit, offset):
        """Get slice elements list."""
        # Always get the first page
        return super(NoLimitPaginator, self).get_slice(0, 0)


class PageNumberPaginator(Paginator):
    """Page number paginator."""

    def page(self):
        """Page items."""
        output = super(PageNumberPaginator, self).page()
        output['page_number'] = int(self.offset / self.limit) + 1
        return output
