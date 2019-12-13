import requests 
from bs4 import BeautifulSoup 
import os,shutil
from os import path
import urllib.request
print('start')
def get_all(URL,yr,month):
	print(URL)
	if not path.exists(yr):
		os.mkdir(yr)
	os.chdir(yr)
	if not path.exists(month):
		os.mkdir(month)
	os.chdir(month)
	r = requests.get(URL)
	print(r.status_code)
	soup = BeautifulSoup(r.content, 'html5lib') 
	print('sent')
	table = soup.find('div', attrs = {'class':'small-7 medium-8 large-8 columns'})
	#print(table.findAll('div', attrs = {'class':'row collapse'})) 
	for row in table.findAll('div', attrs = {'class':'row collapse'}):
		link=row.a['href']
		date,author=row.find('div',attrs = {'id':'comic-author'}).text.split('\n')[1:3]
		temp_r=requests.get("http://explosm.net"+link)
		temp_soup=BeautifulSoup(temp_r.content, 'html5lib') 
		img = temp_soup.find('img', attrs = {'id':'main-comic'})['src']
		print(img[2:])
		urllib.request.urlretrieve('http:'+img,date+'-'+author.split()[1]+'.png')
	os.chdir('../..')
	print('done')


def get_random(URL):
	if not path.exists('random'):
		os.mkdir('random')
	os.chdir('random')
	r=requests.get(URL)
	soup = BeautifulSoup(r.content, 'html5lib') 
	
	list=soup.find('div', attrs = {'class':'rcg-panels'}).findAll('img')
	i=1
	for img in list:
		urllib.request.urlretrieve(img['src'],'frame'+str(i)+'.png')
		i+=1
	
def get_latest(URL,N):
	count=0
	if not path.exists('latest'):
		os.mkdir('latest')
	os.chdir('latest')
	r=requests.get(URL)
	soup = BeautifulSoup(r.content, 'html5lib') 
	for year in soup.findAll('dd',attrs={'class':'accordion-navigation'}):
		content=year.find('ul',attrs={'class':'no-bullet'})
		for link in reversed(content.findAll('li')):
			r=requests.get('http://explosm.net'+link.a['href'])
			soup=BeautifulSoup(r.content, 'html5lib') 
			table = soup.find('div', attrs = {'class':'small-7 medium-8 large-8 columns'})
			for row in table.findAll('div', attrs = {'class':'row collapse'}):
				link=row.a['href']
				date,author=row.find('div',attrs = {'id':'comic-author'}).text.split('\n')[1:3]
				temp_r=requests.get("http://explosm.net"+link)
				temp_soup=BeautifulSoup(temp_r.content, 'html5lib') 
				img = temp_soup.find('img', attrs = {'id':'main-comic'})['src']
				print(img[2:])
				urllib.request.urlretrieve('http:'+img,date+'-'+author.split()[1]+'.png')
				count+=1
				if count==N:
					return


			
f=open('input.txt')
s=f.readlines()
print(s)
if s[0]=='random' or s[0]=='random\n':
	get_random('http://explosm.net/rcg')
elif s[0].split()[0]=='latest':
	N=int(s[1][:-1])
	get_latest('http://explosm.net/comics/archive/',N)
else:
	start,end,authors=s[0:3]
	start_month,start_yr=start.split()
	end_month,end_yr=end.split()
	list_author=authors.split()
	f.close()

	months=['january','february','march','april','may','june','july','august','september','october','november','december']
	for yr in range(int(start_yr),int(end_yr)+1):
		if path.exists(yr):
			shutil.rmtree(yr)
		start=0
		end=12
		if yr==int(start_yr):
			start=months.index(start_month)
		if yr==int(end_yr):
			end=months.index(end_month)+1
		for month in range(start,end):
			str_month=str(month)
			if month<10:str_month='0'+str_month
			for author in list_author:
				get_all('http://explosm.net/comics/archive/'+str(yr)+'/'+str_month+'/'+author.lower(),str(yr),months[month])
