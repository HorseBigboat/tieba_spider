#!/usr/bin/env python3
#encoding:UTF-8

import time
import re
import requests
from bs4 import BeautifulSoup

start = time.clock()

def get_firsturl(number):						#获得帖子URL地址
	url = 'https://tieba.baidu.com/p/'+str(number)
	return url

def get_allurls(number,page):					#获取每一页的URL
	url = 'https://tieba.baidu.com/p/'+str(number)+'?pn='+str(page)
	return url

def get_bshtml(url,data=None):             		#抓取页面
	rep = requests.get(url)
	rep.encoding = 'UTF-8'
	bshtml = BeautifulSoup(rep.text,'html.parser')
	return bshtml

def get_pages(bs):								#获取总页数
	body = bs.body
	div = body.find('div',{'id':'thread_theme_5'})
	class_input = div.find('input')
	pages = class_input.get('max-page')
	return str(pages)

def get_title(bs):								#获取帖子标题
	head = bs.head
	title = head.title.string
	return title

def get_content(bs):							#获取帖子内容
	content = []

	body = bs.body
	div = body.find('div',{'id':'j_p_postlist'})
	pattern = re.compile(r'\>+\d+\u697c')
	stair = pattern.findall(str(div))
	staircc = div.find_all('cc')
	for stair_content in staircc:
		cc_div = stair_content.find('div')
		cc_div_contents = cc_div.contents
		for line in cc_div_contents:
			if str(type(line)) == '<class \'bs4.element.NavigableString\'>':
				content.append(line)
			elif str(type(line)) == '<class \'bs4.element.Tag\'>':
				content.append(str(line))

	return content



def save(content):                       #保存内容
	with open('/Users/madaen/Documents/tieba_spider/content.txt', 'w',encoding='UTF-8',errors='ignore') as f:
		for i in content:
			f.write(i)
			f.write('\n')

if __name__ == '__main__':					#main function
	tiezi = []
	i=1

	number = input('Enter the number of the page:')
	url = get_firsturl(number)

	bshtml = get_bshtml(url)
	title = get_title(bshtml)
	pages = get_pages(bshtml)
	tiezi.append(title)
	tiezi.append(url)
	tiezi.append('\n')

	print('data saving...')

	while i <= int(pages):
		url = get_allurls(number,i)
		bshtml = get_bshtml(url)
		content = get_content(bshtml)
		for tiezi_content in content:
			tiezi.append(tiezi_content)
		i = i+1

	save(tiezi)
	print('Data saved')

	end = time.clock()
	print('Running time: %f s' %(3*(end-start)))
