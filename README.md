# ỨNG DỤNG FUZZING TRONG KIỂM THỬ WEB
## _được thực hiện bởi LittleHawk03 nhóm 4_

[![G|LittleHawk03](https://camo.githubusercontent.com/36f18d672255d9642f3e5ec4886605d43e5000a0c0495536f0d00208720278d3/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f7079636861726d2d3134333f7374796c653d666f722d7468652d6261646765266c6f676f3d7079636861726d266c6f676f436f6c6f723d626c61636b26636f6c6f723d626c61636b266c6162656c436f6c6f723d677265656e)](https://www.youtube.com/watch?v=dQw4w9WgXcQ)

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

Dillinger is a cloud-enabled, mobile-ready, offline-storage compatible,
AngularJS-powered HTML5 Markdown editor.

- Type some Markdown on the left
- See HTML in the right
- ✨Magic ✨

## Features

- kiểm thử lỗi sql injection thông qua phương pháp error base
- kiểm thử lỗi Cross-site Scripting (XSS) 
- kiển thử lỗi File Inclusion
- Crawler url từ một web site theo cấp độ 


## Tech requirement

những yêu cầu cấu hình :

- [Python] - yêu cầu từ phiên bản python 3.x
- [Pip] - yêu cầu trình quản lý gói pip
- [git] - có thể có hoặc không để clone dư án về

## Installation

requires [python](https://www.python.org/downloads/) v10+ to run.

clone data from github : 

```sh
git clone https://github.com/LittleHawk03/Fuzzing_Project.git
```

Install the dependencies and devDependencies and start to run.

```sh
pip install -r requirement.txt
```

## How to runs

Để chạy tool scan vào thư mục project chứa file fuzzing.py chạy lệnh sau.

```sh
python fuzzing.py [-h] [-u TARGET] [-c] [-s] [-x] [-f] [-a] [-ps] [-px]
```

| Plag | option | funtion |
| ------ | ---- | ----------- |
|-h| --help |show this help message and exit|
| -u | --url  |  target url for scanning |
|-c | --crawler |the option for auto crawler from a url|
|-s| --sql     |auto detect a sql injection from a url|
|-x| --xss|   auto detect a sxx vulnerable from a url|
|-f| --file|  auto detect a file inclusion from a url|
|-a| --auto|  auto crawler and scanner all url after crawler url form a website|
|-ps| --payloadsqli|    show all payload of sql injection|
|-px| --payloadxss|     show all payload of xss vulnerable|
  
# Chức năng 1 : Cào (Crawler) URL từ một website mục tiêu.
lệnh chạy chứ năng crawler:
-
```sh
python fuzzing.py -u [TARGET URL] -c
```

example :
-
```sh
python fuzzing.py -u http://testphp.vulnweb.com/categories.php -c
```

![video](picture/video_1.gif)

Logic và sound code [crawler](https://github.com/LittleHawk03/Fuzzing_Project/blob/main/WebConfig/crawler.py): 
-
![image](picture/img_1.png)

Code và thực nghiệm :
-

- **_mục tiêu :_** lấy đươc các url có trong các thẻ href của mục tiêu (các url cho trước)
- **_Các bước thực hiện :_**
   - **Bước 1 :** lấy url của mục tiêu, khởi tạo đối tượng Crawler 
  ![image](picture/img_5.png)
   - **Bước 2 :** thực hiện quá trình crawler (các url sau khi được phân tích sẽ được lưu vào list visited_link)
    ![image](picture/img_6.png)
   
      sử dụng đệ quy để cào sâu (deep_crawler) theo level = 1,2,...
  
   ![image](picture/img_7.png)

   - **bước 3 :** thu kết quả
  
   ![image](picture/img_8.png)

- **_kết quả :_**
 
  - kết quả được trả về là một list các url thu được trong quá trình cào
    ![image](picture/img_9.png)
  - _hạn chế :_ thời gian thực thi trương trình tốn nhiều thời gian 
## Chức năng 2 : Dò quét lỗ hổng SQL INJECTION.

lệnh chạy chứ năng san sql ịnection:

```sh
python fuzzing.py -u [TARGET URL] -s 
```

```sh
python fuzzing.py -u [TARGET URL] --sql 
```

example :

```sh
python fuzzing.py -u http://testphp.vulnweb.com/categories.php -s
```
```sh
python fuzzing.py -u http://testphp.vulnweb.com/categories.php --sql
```

Logic và sound code [sql ịnection](https://github.com/LittleHawk03/Fuzzing_Project/tree/main/SQLi):

![image](picture/img_2.png)


code và thực nghiệm :
-

- **_Mục tiêu :_** tìm và phân tích được lỗ hổng sql injection trong một website bằng cách chén các dữ liệu không hợp lệ vào url hoặc form
- **_Các bước thực hiện :_**

    - **Bước 1:** quá trình sinh payload và lưu vào một list (được lưu ở file [sqli.txt](SQLi/sql.txt))
    
      ![image](picture/img_10.png)

    - **Bước 2:** Phân tích url tách lấy phần query để tiến hành thêm payload (để hiểu rõ hơn đọc comment code tại file [scanSqlErrorBase.py](SQLi/scanSqlErrorBase.py))

      ![image](picture/img_11.png)

    - **Bước 3:** Gửi yêu cầu đến máy chủ lấy mã html về phân tích 
  
      ![image](picture/img_12.png)

    - **Bước 4:** Dùng dữ liệu có sẵn nhận dạng lỗ hổng 

      ![image](picture/img_13.png)

    - **Bước 5:** Lấy kết quả nếu trong mã html trả về có tồn tại các lỗi được thông báo từ database thì sẽ là có thể có lỗ hổng sql injection
    
      ![image](picture/img_14.png)

    - **Bước 6:** kiểm tra các thẻ form trong url đó có bị sql injection không (đọc phần comment trong file [scanSqlErrorBase.py](SQLi/scanSqlErrorBase.py))
        
      ![image](picture/img_15.png)

- **_Kết Quả :_** trả về list các url có thể có lỗ hổng sql injection
    
    ![image](picture/img_16.png)



## Chức năng 3 : Dò quét lỗ hổng Cross-Site Scripting (XSS).

lệnh chạy chứ năng scan Cross-Site Scriptingn:

```sh
python fuzzing.py -u [TARGET URL] -x 
```

```sh
python fuzzing.py -u [TARGET URL] --xss
```

example :

```sh
python fuzzing.py -u http://testphp.vulnweb.com/categories.php -x
```
```sh
python fuzzing.py -u http://testphp.vulnweb.com/categories.php --xss
```

Logic và sound code [xss](https://github.com/LittleHawk03/Fuzzing_Project/tree/main/XSS):


![image](picture/img_3.png)

## Chức năng 4 : Dò quét lỗ hổng File Inclusion.

lệnh chạy chứ năng scan File Inclusionn:

```sh
python fuzzing.py -u [TARGET URL] -f 
```

```sh
python fuzzing.py -u [TARGET URL] --file
```

example :

```sh
python fuzzing.py -u http://testphp.vulnweb.com/categories.php -f
```
```sh
python fuzzing.py -u http://testphp.vulnweb.com/categories.php --file
```

Logic và sound code [file inclusion](https://github.com/LittleHawk03/Fuzzing_Project/tree/main/FileInclusion):

![image](picture/img_4.png)

   [dill]: <https://github.com/joemccann/dillinger>
   [git-repo-url]: <https://github.com/joemccann/dillinger.git>
   [john gruber]: <http://daringfireball.net>
   [df1]: <http://daringfireball.net/projects/markdown/>
   [markdown-it]: <https://github.com/markdown-it/markdown-it>
   [Ace Editor]: <http://ace.ajax.org>
   [node.js]: <http://nodejs.org>
   [Twitter Bootstrap]: <http://twitter.github.com/bootstrap/>
   [jQuery]: <http://jquery.com>
   [@tjholowaychuk]: <http://twitter.com/tjholowaychuk>
   [express]: <http://expressjs.com>
   [AngularJS]: <http://angularjs.org>
   [Gulp]: <http://gulpjs.com>

   [PlDb]: <https://github.com/joemccann/dillinger/tree/master/plugins/dropbox/README.md>
   [PlGh]: <https://github.com/joemccann/dillinger/tree/master/plugins/github/README.md>
   [PlGd]: <https://github.com/joemccann/dillinger/tree/master/plugins/googledrive/README.md>
   [PlOd]: <https://github.com/joemccann/dillinger/tree/master/plugins/onedrive/README.md>
   [PlMe]: <https://github.com/joemccann/dillinger/tree/master/plugins/medium/README.md>
   [PlGa]: <https://github.com/RahulHP/dillinger/blob/master/plugins/googleanalytics/README.md>
