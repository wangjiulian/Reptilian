from bs4 import BeautifulSoup
import bs4

html_doc = """

<html><head><title>The Dormouse's story</title></head>
<body>



<p class="title"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a>
and<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>

"""

# soup = BeautifulSoup(html_doc,'html.parser')
# soup = BeautifulSoup(open('index.html'))

# soup = BeautifulSoup('<b class="boldest">Extremely bold</b>','html.parser')
#
# tag = soup.b
# tag.string.replace_with('21121')
# print(tag.string)

markup = '<b><!--Hey, buddy. Want to buy a used parser?--></b>'
soup = BeautifulSoup(markup,'html.parser')
comment = soup.b.string
if type(soup.b.string) == bs4.element.Comment:
    print(soup.b.string)



