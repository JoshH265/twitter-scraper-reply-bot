from bs4 import BeautifulSoup
import requests


with open("index.html") as fp:
    soup = BeautifulSoup(fp, 'html.parser')


soup = BeautifulSoup('<b class="boldest">Extremely bold</b>', 'html.parser')
tag = soup.b
type(tag)

print(tag)

#This will change the tag <b> to <blockquote>
tag.name = "blockquote"
print(tag)