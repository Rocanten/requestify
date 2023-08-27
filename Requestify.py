import sublime
import sublime_plugin
import re, json
from urllib.request import urlopen

class RequestCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		view = sublime.active_window().active_view()
		content = view.substr(sublime.Region(0, 1000))
		regex = r'(?<=GET )(.*)(?=\n)'
		match = re.search(regex, content)
		if match:
			url = match.group()
			print(url)
			response = self.execute_get_request(url)
			view.insert(edit, view.size(), response)

	def execute_get_request(self, url):
		with urlopen(url) as response:
			body = response.read()
		body_decoded = body.decode('utf-8')
		return body_decoded