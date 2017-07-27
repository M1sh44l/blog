from django import template
from urllib.parse import quote

register = template.Library()

@register.filter
# function needs to be the same name as file name (urlify.py)
def urlify(value):
	return quote(value)