# Request file syntax

## Introduction
This file contains basic syntax description for request files. These files contain information about a collection of http requests.

## Rationale
The aim of this document is to standardize structure and syntax of .http files. This will provide good basis for further development and will also be a great assistance for those who will use Requestify plugin.

## Specification
### What is HTTP file?
HTTP file is a text file that contains information about a collection of requests to one or multiple web servers. 

	basic
	username: username-value
	password: password-value
	###
    Method Request-URI
    Header-field: Header-value
	###
    Method Request-URI
    Header-field: Header-value
    ###

### Method + url line
To specify request, the respective line should start with method. Only `GET`, `POST`, `PATCH`, `PUT`, `DELETE` are supported at this moment

	Method Request-URI

Request-URI should start with protocol(`https` or `http`). If nothing is provided, `https` should be used

### Headers
If string `headers` is presented on first line of parameters, all below parameters(until `###` or new line or new parameters group type) are sent as headers

	headers
	Header-field: Header-value

### Specifying query parameters
If string `query` is presented on first line of parameters, all below parameters(until `###` or new line or new parameters group type) are sent in query

	query
	key: value

These parameters are the same that are contained in Request-URI

### Specifying x-www-form-urlencoded parameters
If string `x-www-form-urlencoded` is presented on first line of parameters, all below parameters(until `###` or new line or new parameters group type) are sent url encoded

	x-www-form-urlencoded
	key: value

### Specifying form-data parameters
If string `form-data` is presented on first line of parameters, all below parameters(until `###` or new line or new parameters group type) are sent as form
 
	form-data
	key: value

### Specifying raw json body
For providing json body, `json` keyword is used

	json
	key: value

### Basic authentication
Basic authentication can be file-scope and request-scope. If file-scope basic authentication is provided, it should be applied for all request in current file.
Request-scope basic authentication overrides file-scope.
To provide file-scope basic authentication the syntax below should be used.

	basic
	username: username-value
	password: password-value

File-scope basic authentication lines should be placed before first `###` keyword.

To provide request-scope basic authentication the syntax below should be used.

	Authorization: Basic username password


### Requests separation
To separate requests from each other `###` keyword should be used. `###` should be also placed before first request and after the last one.

### Comments
HTTP file may contain comments. Both, `#` and `//` are supported for one line comments.
Multiline comments are not supported at this moment