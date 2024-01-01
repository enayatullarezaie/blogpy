from django import template
from datetime import datetime


register = template.Library()


@register.filter
def letterCutter(value, args):
   return value[:args] 


@register.simple_tag
def current_time(format_str):
   return datetime.now().strftime(format_str)



