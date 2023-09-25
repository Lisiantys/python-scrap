from bs4 import BeautifulSoup

with open('home.html', 'r') as html_file:
    content = html_file.read()
    # print(content) affiche toute la page html
    
    soup = BeautifulSoup(content, 'lxml')
    # print(soup.prettify())
    # courses_html_tags = soup.find_all('h5')
    # # print(courses_html_tags) affiche les h5 avec les balises
    # for course in courses_html_tags:
    #     print(course.text) affiche le text des h5
    course_cards = soup.find_all('div', class_="card")
    for course in course_cards:
        # print(course.h5)
        course_name = course.h5.text
        course_price = course.a.text.split()[-1]

        print(f'{course_name} costs {course_price}')

        # Fin 24:48 https://www.youtube.com/watch?v=XVv6mJpFOb0