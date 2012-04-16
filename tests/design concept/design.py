"""Idea this is not even a .py file, maybe generic language (json) and can be transported between languages"""

blog = (
	{
		"name": "blog",
		"format": "C"*20,
		"unique": True,
	},
)

author = (
	{
		"name": "author",
		"format": "C"*50,
	},
)

post= (
	{
		"name": "title",
		"format": "C"*50,
	},
	{
		"name": "content",
		"format": "C"*1000,
		"nullable", True,
		"blankable", True,
	},
	{
		"name": "blog",
		"relation": "blog",
	},
	{
		"name": "author",
		"relation": "author",
	},
)