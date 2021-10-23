[同志社大学の成績評価公開サイト](https://duet.doshisha.ac.jp/kokai/html/fi/fi020/FI02001G.html)から成績分布を取得するためのスクリプト.

## 環境構築

- Python 3
- Google Chrome（バージョン: 95.0.4638.54（Official Build） （arm64））
  - Chrome のバージョンは`chromedriver-binary==95.0.4638.17.0`に適合しているバージョンであれば OK

## 使い方

```bash
cd /path/to/scraping
source bin/activate
pip3 install -r requirements.txt
python3 main.py year # yearには取得したい年度を指定（ex. 2021）
```

## 取得データ例
- grade.distributionの各項目の単位は%
- 学部科目とそれ以外で, 分布が異なることに注意
```json
[
  {
    "code": "31302023-000",
    "year": "2021",
    "period": "春",
    "degreeProgram": "大学院科目",
    "major": "ビジネス研究科",
    "courseName": "Ｆｉｎａｎｃｅ",
    "instructors": ["LIU MING"],
    "registerStudents": "14",
    "grade": {
      "distribution": [
        {
          "A+": "42.9"
        },
        {
          "A": "21.4"
        },
        {
          "B+": "7.1"
        },
        {
          "B": "14.3"
        },
        {
          "C+": "14.3"
        },
        {
          "C": "0.0"
        },
        {
          "F": "0.0"
        },
        {
          "others": "0.0"
        }
      ],
      "average": "3.8"
    }
  }
]
```

```json
[
  {
    "code": "11610040-000",
    "year": "2021",
    "period": "春",
    "degreeProgram": "学部科目",
    "major": "理工学部",
    "courseName": "情報工学実験Ⅱ",
    "instructors": [
      "土屋　誠司",
      "加藤　恒夫",
      "渡部　広一",
      "桂井　麻里衣",
      "木村　共孝",
      "槇原　絵里奈"
    ],
    "registerStudents": "69",
    "grade": {
      "distribution": [
        {
          "A": "49.3"
        },
        {
          "B": "37.7"
        },
        {
          "C": "7.2"
        },
        {
          "D": "2.9"
        },
        {
          "F": "2.9"
        },
        {
          "others": "0.0"
        }
      ],
      "average": "3.3"
    }
  }
]
```
