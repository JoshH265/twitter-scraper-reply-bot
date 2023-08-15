from bs4 import BeautifulSoup
import requests

url = "https://www.newegg.com/global/uk-en/gigabyte-geforce-rtx-4080-gv-n4080eagle-oc-16gd/p/N82E16814932562"

result = requests.get(url)
print(result.text)


doc = BeautifulSoup(result.text, "html.parser")

print(doc.prettify())


prices = doc.find_all(string="£")
print(prices)

parent = prices[0].parent 
print(parent)
strong = parent.find("strong")
print(strong.string)



