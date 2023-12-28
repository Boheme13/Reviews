import os
import math


def main():
    paths = os.listdir()
    paths.sort()

    output_path = "index.md"

    # clear the output file
    with open(output_path, 'w') as output:
        output.write("""## Reviews\n[回到主页](https://boheme13.github.io/Fiction.git.io/)<br><br>\n\n""")

    urls = []
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
    with open(output_path, 'a+') as output:
        for url in urls:
            filedata = ""
            with open(url[2], 'r') as markdown:
                filedata = markdown.read()
                # str1 = "[回到上一页](https://boheme130.github.io/Reviews/)  &nbsp;&nbsp;  [回到主页](https://boheme130.github.io/Fiction.git.io/)"
                str1 = "[回到上一页](https://boheme130.github.io/Reviews/)  &nbsp;&nbsp;  [回到主页](https://boheme130.github.io/Fiction.git.io/)"
                filedata = filedata.replace(str1, "[回到上一页](https://boheme13.github.io/Reviews/)  &nbsp;&nbsp;")
            with open(url[2], 'w') as file:
                file.write(filedata)
            if (url[2].find('.JPG') != -1 or url[2].find('.jpg') != -1):
                continue
            with open(url[2], 'r') as markdown:
                lines = markdown.readlines()
                book, output_str, keys = "", "", ""
                find_book, find_rate, find_key, add_img = False, False, False, False
                count = 0
                img_url = ""
                for line in lines:
                    line = line.rstrip()
                    if (line.find("avatar") != -1 or line.find("img") != -1) and not add_img:
                        index1, index2 = line.find('('), line.find(')')
                        img_url = line[index1+1:index2]
                    if line.find("作品") != -1 and not find_book:
                        index = line.find('<')
                        book = line[3:index]
                        find_book = True
                        output_str = f"[{book}]({url[1]}) "
                    if line.find("评分") != -1 and line.find('/') != -1 and not find_rate:
                        index = line.find('/')
                        count = float(line[3:index]) - 4.7
                        find_rate = True
                        if count < -0.1:
                            continue
                        count = int((count + 0.001) / 0.1) + 1
                        # print(book, count)
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
                if add_img and img_url != "":
                    output.write("\n <br><br> \n")
                    output.write(f"![avatar]({img_url})<br>\n")
                    # output.write("\n <br> \n")
                output.write("\n\n")
                     

if __name__ == "__main__":
    main()