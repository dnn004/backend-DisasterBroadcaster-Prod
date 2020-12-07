from django.core.paginator import Paginator, InvalidPage

def paginate(queryset, page, page_end=None):
  total_listings = 5
  try:
    if page_end is not None:
      total_listings = int(page_end) * total_listings
    paginate = Paginator(queryset, total_listings)
    page = paginate.page(page)
  except InvalidPage:
    page = []
  return page