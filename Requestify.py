import sublime
import sublime_plugin
import re, json
from urllib.request import urlopen

class RequestCommand(sublime_plugin.TextCommand):
	def __init__(self, view):
		self.test = 'not set'
		super().__init__(view)
	def run(self, edit):

		print(self.test)

		if self.test == 'not set':
			self.test = 'is set'
		view = sublime.active_window().active_view()
		content = view.substr(sublime.Region(0, 1000))
		regex = r'(?<=GET )(.*)(?=\n)'
		if match := re.search(regex, content):
			url = match.group()
			print(url)
			response = self.execute_get_request(url)
			view.insert(edit, view.size(), response)

	def execute_get_request(self, url):
		with urlopen(url) as response:
			body = response.read()
		return body.decode('utf-8')