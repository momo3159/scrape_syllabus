from os import wait
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import json
import sys


from const import majors, years, TOP_PAGE_URL, PATTERN, degree_map, major_map
from selenium_wrapper import initDriver, setWait, selectByValueWithWait, clickBtnWithWait


def makeJsonOfGradePerFacultyCourse(td_list, degree, major, year):
    return {
        "code": td_list[0].get_text(),
        "year": year,
        "period": td_list[1].get_text(),
        "degreeProgram": degree,
        "major": major,
        "courseName": td_list[2].get_text(),
        "instructors": list(filter(lambda s: s != '', PATTERN.split(td_list[3].get_text()))),
        "registerStudents": td_list[4].get_text(),
        "grade": {
            "distribution": [
                {"A": td_list[5].get_text() or None},
                {"B": td_list[6].get_text() or None},
                {"C": td_list[7].get_text() or None},
                {"D": td_list[8].get_text() or None},
                {"F": td_list[9].get_text() or None},
                {"others": td_list[10].get_text() or None},
                # <span><br/></span>
            ],
            "average": td_list[11].get_text() or None
        }
    }


def makeJsonOfGradePerGraduateCourse(td_list, degree, major, year):
    return {
        "code": td_list[0].get_text(),
        "year": year,
        "period": td_list[1].get_text(),
        "degreeProgram": degree,
        "major": major,
        "courseName": td_list[2].get_text(),
        "instructors": list(filter(lambda s: s != '', PATTERN.split(td_list[3].get_text()))),
        "registerStudents": td_list[4].get_text(),
        "grade": {
            "distribution": [
                {"A+": td_list[5].get_text() or None},
                {"A":  td_list[6].get_text() or None},
                {"B+": td_list[7].get_text() or None},
                {"B":  td_list[8].get_text() or None},
                {"C+": td_list[9].get_text() or None},
                {"C":  td_list[10].get_text() or None},
                {"F":  td_list[11].get_text() or None},
                {"others": td_list[12].get_text() or None},
                # <span><br/></span>
            ],
            "average": td_list[13].get_text() or None
        }
    }


if __name__ == "__main__":
    if len(sys.argv) != 2:
        exit(1)

    opts = Options()
    opts.headless = False
    driver = initDriver(opts)
    wait = setWait(driver, 20)

    driver.get(TOP_PAGE_URL)

    year = sys.argv[1]
    selectByValueWithWait(
        year, wait, lambda d: d.find_element_by_id("form1:kaikoNendolist"))

    for degree_value, major_values in majors.items():
        print(degree_map[degree_value])

        degree_programs_select = selectByValueWithWait(
            degree_value, wait, lambda d: d.find_element_by_name("form1:_id82"))

        for major_value in major_values:
            print(major_map[major_value])

            major_values_select = selectByValueWithWait(
                major_value, wait, lambda d: d.find_element_by_name("form1:_id86"))

            # search
            clickBtnWithWait(wait, lambda d: d.find_element_by_id(
                "form1:enterDodoZikko"))
            l = []
            while True:
                # 成績分布の取得
                html = driver.page_source.encode("utf-8")
                soup = BeautifulSoup(html, 'html.parser')
                table = soup.find("table", class_="data sortable")
                tr_list = table.find_all("tr")
                if len(tr_list) == 0:
                    continue

                for tr in tr_list:
                    td_list = tr.find_all("td")
                    if len(td_list) == 14:
                        l.append(
                            makeJsonOfGradePerFacultyCourse(
                                td_list,
                                degree_map[degree_value],
                                major_map[major_value],
                                year
                            )
                        )
                    if len(td_list) == 16:
                        l.append(
                            makeJsonOfGradePerGraduateCourse(
                                td_list,
                                degree_map[degree_value],
                                major_map[major_value],
                                year
                            )
                        )

                # 次のページのリンクの取得
                next_page_link = wait.until(lambda d: d.find_element(
                    By.XPATH, "//*[text()=\"次のページ\"]"))

                # （link.tag_name == 'a'ならば）ページ遷移
                if next_page_link.tag_name != 'a':
                    print(
                        f"{year}_{degree_map[degree_value]}_{ major_map[major_value]} finish")
                    break

                # Footerとリンクが被ってクリックできないのを防ぐため
                driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);")

                next_page_link.click()

            with open(f"./{year}_{degree_map[degree_value]}_{ major_map[major_value]}.json", encoding="utf-8", mode="w") as f:
                json.dump(l, f, ensure_ascii=False, indent=2)

            driver.execute_script(
                "window.scrollTo(document.body.scrollHeight, 0);")

    driver.quit()
