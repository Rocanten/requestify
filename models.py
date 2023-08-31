from dataclasses import dataclass
from typing import List


@dataclass
class RequestParameter:
	key: str
	value: str

@dataclass
class FileBasicAuth:
	username: str
	password: str

@dataclass 
class Request:
	method: str
	url: str
	headers: List[RequestParameter]
	query_params: List[RequestParameter]
	form_data_params: List[RequestParameter]
	urlencoded_params: List[RequestParameter]
	json: dict


@dataclass
class HTTPFile:
	file_basic_auth: FileBasicAuth
	requests: List[Request]