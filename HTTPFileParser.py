import re, json
from typing import List

import sublime
from .models import *


class HTTPFileParser:
	def parse_view(self, view: sublime.View):

		file_text = view.substr(sublime.Region(0, view.size()))

		file_scope_string = self.get_file_scope_string(file_text)
		request_strings = self.get_reuqests_strings(file_text)

		file_basic_auth = self.parse_file_scope_basic_auth(file_scope_string)

		requests: List[Request] = []
		for request_string in request_strings:
			request = self.parse_reuqest_string(request_string)
			requests.append(request)

		httpFile: HTTPFile = HTTPFile(requests=requests, 
			file_basic_auth=file_basic_auth)
		print(httpFile)



	def get_file_scope_string(self, view_content: str) -> str:
		return re.match(r"^(?!###)[\s\S]*?(?=###)", view_content).group()


	def get_reuqests_strings(self, view_content: str) -> List[str]:
		p = re.compile(r'(?<=###).*?(?=###)', re.S | re.I)
		return p.findall(view_content)

	def parse_reuqest_string(self, request_string: str) -> Request:
		method = self.parse_request_method(request_string)
		url = self.parse_request_url(request_string)
		headers = self.parse_request_params(request_string, 'headers')
		query_params = self.parse_request_params(request_string, 'query')
		form_data_params = self.parse_request_params(request_string, 'form-data')
		urlencoded_params = self.parse_request_params(request_string, 'x-www-form-urlencoded')
		json = self.parse_request_json(request_string)
		return Request(
			method=method,
			url=url,
			headers=headers,
			query_params=query_params,
			form_data_params=form_data_params,
			urlencoded_params=urlencoded_params,
			json=json,
		)


	def parse_request_method(self, request_string: str) -> str:
		p = re.compile(r'(GET|POST|PATCH|PUT|DELETE)', re.S | re.I)
		return p.search(request_string).group()

	def parse_request_url(self, request_string: str) -> str:
		p = re.compile(r'(http:\/\/|https:\/\/)[-a-zA-Z0-9@:%._\/+~#=]{1,256}', re.S | re.I)
		return p.search(request_string).group()

	def parse_request_params(self, request_string: str, type: str) -> List[RequestParameter]:
		params_string = self.get_string_section(request_string, type)
		if params_string is None:
			return None
		p_parameters = re.compile(r'(?<=:).+|.+(?=:)', re.I)
		parameters: List[str] = p_parameters.findall(params_string)
		result: List[RequestParameter] = []
		i = 0
		while i < len(parameters):
			requestParameter = RequestParameter(key=parameters[i], value=parameters[i+1])
			result.append(requestParameter)
			i += 2
		return result

	def parse_request_json(self, request_string: str) -> dict:
		json_section_string = self.get_string_section(request_string, 'json_body')
		if json_section_string is None:
			return None
		p = re.compile(r'{.*}', re.S | re.I)
		json_string = p.search(json_section_string).group()
		json_string = json_string.replace("\n", "")
		json_string = json_string.encode('unicode_escape')
		return json.loads(json_string)

	def parse_file_scope_basic_auth(self, file_scope_string: str) -> FileBasicAuth:
		p_only_basic = re.compile(r'(?<=basic).*(?=basic)', re.S | re.I)
		basic_string = p_only_basic.search(file_scope_string).group()
		p_username = re.compile(r'(?<=username:\s)\w*', re.S | re.I)
		p_password = re.compile(r'(?<=password:\s)\w*', re.S | re.I)
		username = p_username.search(basic_string).group()
		password = p_password.search(basic_string).group()
		return FileBasicAuth(username=username, password=password)

	def get_string_section(self, request_string: str, type: str) -> str:
		p_section_string = re.compile(f'(?<={type})(.*(?=\njson_body)|.*(?=\nquery)|.*(?=\nform-data)|.*(?=\nx-www-form-urlencoded)|.*\n$|.*}}$)', re.S | re.I)
		try:
			return p_section_string.search(request_string).group()
		except AttributeError as e:
			print(f'Token with type {type} not found')
			return None
		