 
from django.conf import settings
from django.template import Library
import os 
from django.utils.safestring import mark_safe
register = Library()

base_directory  = settings.STATICFILES_DIRS[0]


@register.simple_tag
def css_href(directory=""):
	links_css = ""
	completed_directory  = base_directory +"/css/" + directory
	for elem in os.listdir(completed_directory):
		links_css +="<link href={0} rel='stylesheet'>".format("/static/css/" + elem) 
		links_css += "\n"
	return mark_safe(links_css)

@register.simple_tag
def js_src(directory=""):
	links_js = ""
	completed_directory  = base_directory +"/js/" + directory
	for elem in os.listdir(completed_directory):
		links_js +="<script type='text/javascript' src='{0}'></script>".format("/static/js/" + elem)
		links_js += "\n"
	return mark_safe(links_js)
