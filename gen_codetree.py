#!/usr/bin/env python
#/*
# * CodeTree - Show codes as a tree
# * 
# * https://github.com/DomLin/CodeTree
# *
# * Copyright (c) 2013 Dom Lin
# *
# * Dual licensed under the MIT and GPL licenses:
# *   http://www.opensource.org/licenses/mit-license.php
# *   http://www.gnu.org/licenses/gpl.html
# *
# * Date: Mon Nov 11 14:45:26 CST 2013
# *
# */
import sys
import re
import cgi

usage = "Usage: python " + sys.argv[0] + " filename"
usage = usage + """

Each line of the file should be started with following symbol:
#.	: # is a number for a level
>>	: It's a file name
//	: It's a comment
::	: It's a condition

If you do not want to escape special significance in HTML, use %% symbol around the content.
For example: %%<a href="demo.html">demo.html</a>%%
If you want to display %%, you should use \%\% to disable the special function.
"""

def optionalEscape(html):
	text = ""
	i = 0;
	data = re.split('[%][%]', html.strip())
	while i < len(data):
		data[i] = data[i].replace("\\%\\%", "%%")
		if i % 2 == 0:
			text = text + cgi.escape(data[i])
		else:
			text = text + data[i]
		i = i + 1

	return text

def genTab(count):
	text = ""
	tab = 0
	while tab < count:
		text = text + "\t"
		tab = tab + 1
	return text


if len(sys.argv) <= 1:
	sys.exit(usage)
			 
print "Generating from " + sys.argv[1] + " to " + sys.argv[1] + ".html ..."
rfile = open(sys.argv[1], 'r')
wfile = open(sys.argv[1] + ".html", 'w')

head = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" 
	"http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
  <!-- Automatically generated by gen_codetree.py -->
  <meta http-equiv="content-type" content="text/html; charset=UTF-8">
  <meta charset="UTF-8">
"""
head = head + "  <meta name=\"description\" content=\"" + sys.argv[1] + ".html - Automatically generated by gen_codetree.py\">"
head = head + """
  <link rel="stylesheet" href="codetree/codetree.css" type="text/css" />
  <script type="text/javascript" src="codetree/jquery-1.6.1.min.js"></script>
  <script type="text/javascript" src="codetree/jquery.treeview.codetree.js"></script>
  <script>
  $(document).ready(function(){
	$("#code").treeview({
		animated: "fast",
		control: "#treecontrol"
	});
  });
  </script>
"""
head = head + "  <title>" + sys.argv[1] + "</title>" + """
</head>
<body>
<div id="treecontrol">
	<a href="?#">Collapse All</a> |
	<a href="?#">Expand All</a> |
	<a href="?#">Show All Info</a> |
	<a href="?#">Hide All Info</a> |
	<a href="?#">Un-check All</a>
</div>
"""

foot = """
<div>Modified from <a href="http://jquery.com/" target="_blank">jQuery</a> plugin <a href="http://bassistance.de/jquery-plugins/jquery-plugin-treeview/" target="_blank">Treeview</a> by <a target="_blank" href="https://github.com/DomLin/CodeTree">Dom_Lin</a></div>
</body>
</html>
"""

level = []
elem = []
newLevel = ""
currLevel = ""
tabCount = 0
lineID = long(0)
for line in rfile:
	lineID = lineID + 1;
	# function
	data = re.split('^[-]?[0-9]+[.]', line.strip())
	sys.stdout.write(".")
	if len(data) > 1:
		filePath = re.split('^[>][>]', data[1].strip())
		commentData = re.split('^[/][/]', data[1].strip())
		condition = re.split('^[:][:]', data[1].strip())
		newLevel = re.search('^[-]?[0-9]+[.]', line.strip()).group(0)[:-1]
		if len(level) == 0:
			head = head + "<ul id=\"code\" class=\"codetree\">" + "\n" + "\t<li>" + "\n"
			elem.append("</ul>")
			elem.append("</li>")
			if len(filePath) > 1:
				head = head + "\t\t<span class=\"fileHead\" id=\"" + str(lineID) + "\" title=\"L: " + newLevel + ", ID: " + str(lineID) + "\">" + optionalEscape(filePath[1].strip()) + "</span>" + "\n"
			elif len(commentData) > 1:
				spaceCount = 0
				space = ""
				while commentData[1][spaceCount] == " ":
					spaceCount = spaceCount + 1
					space = space + "&nbsp;"
				head = head + "\t\t<span class=\"commentHead\" id=\"" + str(lineID) + "\" title=\"L: " + newLevel + ", ID: " + str(lineID) + "\">//" + space + optionalEscape(commentData[1].strip()) + "</span>" + "\n"
			elif len(condition) > 1:
				head = head + "\t\t<input type=\"checkbox\"/>" + "\n"
				head = head + "\t\t<span class=\"condition\" id=\"" + str(lineID) + "\" title=\"L: " + newLevel + ", ID: " + str(lineID) + "\">" + optionalEscape(condition[1].strip()) + "</span>" + "\n"
			else:
				head = head + "\t\t<input type=\"checkbox\"/>" + "\n"
				head = head + "\t\t<span class=\"funcName\" id=\"" + str(lineID) + "\" title=\"L: " + newLevel + ", ID: " + str(lineID) + "\">" + optionalEscape(data[1].strip()) + "</span>" + "\n"
			level.append(newLevel)
			currLevel = newLevel
		else:
			try:
				level.index(newLevel)
				# already have the level
				if long(currLevel) == long(newLevel):
					# same level
					head = head + genTab(tabCount-1) + "</li>" + "\n"
					head = head + genTab(tabCount-1) + "<li>" + "\n"
					if len(filePath) > 1:
						head = head + genTab(tabCount) + "<span class=\"fileHead\" id=\"" + str(lineID) + "\" title=\"L: " + newLevel + ", ID: " + str(lineID) + "\">" + optionalEscape(filePath[1].strip()) + "</span>" + "\n"
					elif len(commentData) > 1:
						spaceCount = 0
						space = ""
						while commentData[1][spaceCount] == " ":
							spaceCount = spaceCount + 1
							space = space + "&nbsp;"
						head = head + genTab(tabCount) + "<span class=\"commentHead\" id=\"" + str(lineID) + "\" title=\"L: " + newLevel + ", ID: " + str(lineID) + "\">//" + space + optionalEscape(commentData[1].strip()) + "</span>" + "\n"
					elif len(condition) > 1:
						head = head + genTab(tabCount) + "<input type=\"checkbox\"/>" + "\n"
						head = head + genTab(tabCount) + "<span class=\"condition\" id=\"" + str(lineID) + "\" title=\"L: " + newLevel + ", ID: " + str(lineID) + "\">" + optionalEscape(condition[1].strip()) + "</span>" + "\n"
					else:
						head = head + genTab(tabCount) + "<input type=\"checkbox\"/>" + "\n"
						head = head + genTab(tabCount) + "<span class=\"funcName\" id=\"" + str(lineID) + "\" title=\"L: " + newLevel + ", ID: " + str(lineID) + "\">" + optionalEscape(data[1].strip()) + "</span>" + "\n"
				elif long(currLevel) > long(newLevel):
					# decrease level
					while level[len(level)-1] != newLevel:
						level.pop()
						tabCount = len(level) * 2
						head = head + genTab(tabCount+1) + elem.pop() + "\n"
						head = head + genTab(tabCount) + elem.pop() + "\n"
					head = head + genTab(tabCount-1) + "</li>" + "\n"
					head = head + genTab(tabCount-1) + "<li>" + "\n"
					if len(filePath) > 1:
						head = head + genTab(tabCount) + "<span class=\"fileHead\" id=\"" + str(lineID) + "\" title=\"L: " + newLevel + ", ID: " + str(lineID) + "\">" + optionalEscape(filePath[1].strip()) + "</span>" + "\n"
					elif len(commentData) > 1:
						spaceCount = 0
						space = ""
						while commentData[1][spaceCount] == " ":
							spaceCount = spaceCount + 1
							space = space + "&nbsp;"
						head = head + genTab(tabCount) + "<span class=\"commentHead\" id=\"" + str(lineID) + "\" title=\"L: " + newLevel + ", ID: " + str(lineID) + "\">//" + space + optionalEscape(commentData[1].strip()) + "</span>" + "\n"
					elif len(condition) > 1:
						head = head + genTab(tabCount) + "<input type=\"checkbox\"/>" + "\n"
						head = head + genTab(tabCount) + "<span class=\"condition\" id=\"" + str(lineID) + "\" title=\"L: " + newLevel + ", ID: " + str(lineID) + "\">" + optionalEscape(condition[1].strip()) + "</span>" + "\n"
					else:
						head = head + genTab(tabCount) + "<input type=\"checkbox\"/>" + "\n"
						head = head + genTab(tabCount) + "<span class=\"funcName\" id=\"" + str(lineID) + "\" title=\"L: " + newLevel + ", ID: " + str(lineID) + "\">" + optionalEscape(data[1].strip()) + "</span>" + "\n"
					currLevel = newLevel
			except:
				# increase level
				tabCount = len(level) * 2
				head = head + genTab(tabCount) + "<ul>" + "\n"
				elem.append("</ul>")
				head = head + genTab(tabCount) + "\t<li>" + "\n"
				elem.append("</li>")
				if len(filePath) > 1:
					head = head + genTab(tabCount) + "\t\t<span class=\"fileHead\" id=\"" + str(lineID) + "\" title=\"L: " + newLevel + ", ID: " + str(lineID) + "\">" + optionalEscape(filePath[1].strip()) + "</span>" + "\n"
				elif len(commentData) > 1:
					spaceCount = 0
					space = ""
					while commentData[1][spaceCount] == " ":
						spaceCount = spaceCount + 1
						space = space + "&nbsp;"
					head = head + genTab(tabCount) + "\t\t<span class=\"commentHead\" id=\"" + str(lineID) + "\" title=\"L: " + newLevel + ", ID: " + str(lineID) + "\">//" + space + optionalEscape(commentData[1].strip()) + "</span>" + "\n"
				elif len(condition) > 1:
					head = head + genTab(tabCount) + "\t\t<input type=\"checkbox\"/>" + "\n"
					head = head + genTab(tabCount) + "\t\t<span class=\"condition\" id=\"" + str(lineID) + "\" title=\"L: " + newLevel + ", ID: " + str(lineID) + "\">" + optionalEscape(condition[1].strip()) + "</span>" + "\n"
				else:
					head = head + genTab(tabCount) + "\t\t<input type=\"checkbox\"/>" + "\n"
					head = head + genTab(tabCount) + "\t\t<span class=\"funcName\" id=\"" + str(lineID) + "\" title=\"L: " + newLevel + ", ID: " + str(lineID) + "\">" + optionalEscape(data[1].strip()) + "</span>" + "\n"
				level.append(newLevel)
				currLevel = newLevel
		tabCount = len(level) * 2

	if len(level) > 0:
		# file
		data = re.split('^[>][>]', line.strip())
		if len(data) > 1:
			head = head + genTab(tabCount) + "<span class=\"newline\"></span>" + "\n"
			head = head + genTab(tabCount) + "<span class=\"file\">" + optionalEscape(data[1].strip()) + "</span>" + "\n"

		# comment
		data = re.split('^[/][/]', line.strip())
		if len(data) > 1:
			if len(data[1]) > 1:
				spaceCount = 0
				space = ""
				while data[1][spaceCount] == " ":
					spaceCount = spaceCount + 1
					space = space + "&nbsp;"
			head = head + genTab(tabCount) + "<span class=\"newline\"></span>" + "\n"
			head = head + genTab(tabCount) + "<span class=\"comment\">//" + space + optionalEscape(data[1].strip()) + "</span>" + "\n"

while len(level):
	level.pop()
	tabCount = len(level) * 2
	head = head + genTab(tabCount+1) + elem.pop() + "\n"
	head = head + genTab(tabCount) + elem.pop() + "\n"

rfile.close()
wfile.write(head + foot)
wfile.close()

print ""
print "Done."
