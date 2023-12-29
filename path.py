import os
import math
import json

class Book:
    def __init__(self, path, title, skip, rating=-1, keywords="", author="", img_url=""):
        self.path = path
        self.title = title
        self.skip = skip
        self.rating = rating
        self.keywords = keywords
        self.author = author
        self.img_url = img_url
    
    def display_info(self):
        info = f"title: {self.title}\n rating: {self.rating}\n keywords: {self.keywords}\n img_url: {self.img_url} \n{self.path}"
        print(info)

def word_to_number(word):
    sum = 0
    orignal_len, l = len(word), len(word)
    while l:
        sum += ord(word[orignal_len - l]) * (10 ** l)
        l -= 1
    return sum


def main():
    paths = os.listdir()
    paths.sort()

    output_path = "index.md"

    # clear the output file
    with open(output_path, 'w') as output:
        output.write("""## Reviews\n[回到主页](https://boheme13.github.io/Reviews/)   &nbsp;&nbsp;  [按评分排序](https://boheme13.github.io/Reviews/Sorting)  <br><br>\n\n""")

    urls, books = [], []
    for path in paths:
        if path.find(".") != -1:
            continue
        path = path.strip()
        urls.append([path, f"https://boheme13.github.io/Reviews/{path}/", f"./{path}/index.md"])
        subs = os.listdir(f"./{path}")
        if len(subs) > 1:
            for sub in subs:
                if sub == "index.md":
                    continue
                sub = sub.strip()
                if sub.find('.JPG') != -1 or sub.find('.jpg') != -1:
                    continue
                urls.append([sub, f"https://boheme13.github.io/Reviews/{path}/{sub}/", f"./{path}/{sub}/index.md"])
    print(urls[0])
    with open(output_path, 'a+') as output:
        for url in urls:
            filedata = ""
            # with open(url[2], 'r') as markdown:
            #     filedata = markdown.read()
            #     # str1 = "[回到上一页](https://boheme130.github.io/Reviews/)  &nbsp;&nbsp;  [回到主页](https://boheme130.github.io/Fiction.git.io/)"
            #     str1 = "[回到上一页](https://boheme130.github.io/Reviews/)  &nbsp;&nbsp;  [回到主页](https://boheme130.github.io/Fiction.git.io/)"
            #     filedata = filedata.replace(str1, "[回到上一页](https://boheme13.github.io/Reviews/)  &nbsp;&nbsp;")
            # with open(url[2], 'w') as file:
            #     file.write(filedata)
            if (url[2].find('.JPG') != -1 or url[2].find('.jpg') != -1 or url[2].find('.png') != -1):
                continue
            with open(url[2], 'r') as markdown:
                lines = markdown.readlines()
                book, output_str, keys = "", "", ""
                find_book, find_rate, find_key, add_img, find_author = False, False, False, False, False
                count, rating = 0, -1
                author = ""
                img_url, find_img = "", False
                for line in lines:
                    line = line.rstrip()
                    if (line.find("avatar") != -1 or line.find("img") != -1) and not add_img and not find_img:
                        index1, index2 = line.find('('), line.find(')')
                        img_url = line[index1+1:index2]
                        find_img = True
                    if line.find("作品") != -1 and not find_book:
                        index = line.find('<')
                        book = line[3:index]
                        find_book = True
                        output_str = f"[{book}]({url[1]}) "
                    if line.find("作者") != -1 and not find_author:
                        index = line.find('<')
                        author = line[3:index]
                        find_author = True
                    if line.find("评分") != -1 and line.find('/') != -1 and not find_rate:
                        index = line.find('/')
                        rating = round(float(line[3:index]), 2)
                        count = float(line[3:index]) - 4.0
                        find_rate = True
                        if count < -0.1:
                            continue
                        count = int((count + 0.001) / 0.1) + 1
                        print(count)
                        # print(book, count)
                        if count >= 7:
                            count = 3
                        elif count >= 4:
                            count = 2
                        elif count >= 1:
                            count = 1
                        
                        if count >= 2:
                            add_img = True
                        for i in range(min(count, 3)):
                            output_str += "⭐️"
                        # output.write(f"{output_str}<br>\n")
                    if line.find("关键词") != -1 and not find_key:
                        while line.find("<br>") != -1:
                            line = line.replace("<br>", "")
                        keys = line
                        find_key = True
                # if not find_rate:
                output.write(f"{output_str}<br>\n")
                if find_key:
                    output.write(f"{keys}")
                if img_url != "" and img_url[0:2] == "./":
                    img_url = f"./{url[0]}/{img_url[2::]}"
                if add_img and img_url != "":
                    output.write("\n <br><br> \n")
                    output.write(f"![avatar]({img_url})<br>\n")
                    # output.write("\n <br> \n")
                output.write("\n\n")
                books.append(Book(path=url[1], title=book, skip=False, rating=rating, keywords=keys, author=author, img_url=img_url))
    # print(books[2].display_info())
    




    output_path = "./Sorting/index.md"
    # clear the output file
    with open(output_path, 'w') as output:
        output.write("""## Reviews\n[回到主页](https://boheme13.github.io/Reviews/)<br><br>\n\n""")



    books = [book for book in books if book.path != 'https://boheme13.github.io/Reviews/Sorting/']
    books.sort(key=lambda book: (book.rating, -word_to_number(book.title)), reverse=True)

    print(books[1].display_info())
    
    with open(output_path, 'a+') as output:
        for book in books:
            rating = "" if book.rating == -1 else f"Rating: {book.rating}"
            output_str = f"[{book.title}]({book.path}) {rating}"
            output.write(f"{output_str}<br>\n")
            if book.keywords != "":
                output.write(f"{book.keywords}")
            if book.rating >= 4.2 and book.img_url != "":
                output.write("\n <br><br> \n")
                if book.img_url[0:2] == "./":
                    output.write(f"![img](../{book.img_url})<br>\n")
                else:
                    output.write(f"![img]({book.img_url})<br>\n")
            output.write("\n\n")

    books_data = []
    for book in books:
        img_url = book.img_url
        if img_url != "" and img_url[0:2] == "./":
            img_url = f"https://boheme13.github.io/Reviews/{img_url}"
        books_data.append({
            'path': book.path, 
            'title': book.title, 
            'skip': book.skip, 
            'rating': book.rating, 
            'keywords': book.keywords, 
            'author': book.author, 
            'img_url': img_url
        })
    json_data = json.dumps(books_data, indent=2, ensure_ascii=False)

    file_path = './books.json'
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json_file.write(json_data)



                     

if __name__ == "__main__":
    main()