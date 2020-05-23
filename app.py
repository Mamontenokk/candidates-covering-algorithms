import streamlit as st
import numpy as np 
import pandas as pd 
import time
from math import ceil
from functions import generate_input, read_file
from algorithms import *
from charts import *


@st.cache
def get_data(num_of_candidates, subgroups):
    return generate_input(num_of_candidates, subgroups)


def show_main_page():
    st.title('Задача про покриття множини')

    input_type = st.radio('Оберіть вид вводу даних', ('Завантаження даних з файлу', 'Генерація даних'))
    if input_type == 'Завантаження даних з файлу':
        file = st.file_uploader('Завантажте файл:')
        candidates = read_file(file)

    elif input_type == 'Генерація даних':
        st.subheader('Оберіть параметри')
        num_of_candidates = st.slider('Кількість кандидатів:', 2, 100, 10)
        num_of_groups = st.slider('Кількість груп:', 1, 10, 5)

        subgroups = [3]*num_of_groups
        st.subheader('Оберіть кількість підгруп в кожній групі')
        for group in range(num_of_groups):
            subgroups[group] = st.slider(f'Кількість підгруп в групі {group+1}', 2, 6, 3)

        candidates = get_data(num_of_candidates, subgroups)

    if isinstance(candidates, bool):
        st.header('Перевірте обрані параметри, будь ласка')
    else:
        if st.button('Показати дані'):
            st.dataframe(pd.DataFrame(candidates))

        algorithms = st.multiselect('Оберіть алгоритм', ('Жадібний алгоритм #1','Жадібний алгоритм #2','Жадібний алгоритм #3','Генетичний алгоритм #1','Генетичний алгоритм #2'))

        if 'Генетичний алгоритм #1' in algorithms or 'Генетичний алгоритм #2' in algorithms:
            st.subheader('Оберіть параметри для генетичного алгоритму')
            population_size = st.slider('Розмір популяції:', 0, 100, 10)
            alpha = st.slider('Альфа:', 0.0, 1.0, 0.5)
            iter_num = st.slider('Кількість ітерацій:', 1, 100, 20)

        if st.button('Розв\'язати задачу!'):
            st.header('Відповідь')
            for algorithm in algorithms:
                args = [candidates]

                if algorithm == 'Жадібний алгоритм #1':
                    fn = first_greedy_algorithm
                    args.append([0])
                elif algorithm  == 'Жадібний алгоритм #2':
                    fn = second_greedy_algorithm
                elif algorithm  == 'Жадібний алгоритм #3':
                    fn = third_greedy_algorithm
                elif algorithm  == 'Генетичний алгоритм #1' or algorithm  == 'Генетичний алгоритм #2':
                    args.append(population_size)
                    args.append(alpha)
                    args.append(iter_num)
                    if algorithm  == 'Генетичний алгоритм #1':
                        fn = first_genetic_algorithm
                    else:
                        fn = second_genetic_algorithm

                result = fn(*args)
                st.subheader(f'Метод розв\'язання - {algorithm}')
                st.write(f'Значення цільової функції: {len(result)}')
                st.write(f'Комітет складається з наступних кандидатів: {str(result)}')
                st.altair_chart(create_chart(candidates, result), use_container_width=True)
        


def show_research_page():

    st.title('Експериментальне дослідження алгоритмів')

    algorithms = {
        1: '1-й жадібний алгоритм',
        2: '2-й жадібний алгоритм',
        3: '3-й жадібний алгоритм',
        4: '1-й генетичний алгоритм',
        5: '2-й генетичний алгоритм',
    }
    greedy_df = pd.read_csv('data/greedy.csv')
    greedy_df['Algorithm'] = greedy_df['Algorithm'].map(algorithms)
    genetic_df = pd.read_csv('data/genetic.csv')
    genetic_df['Algorithm'] = genetic_df['Algorithm'].map(algorithms)
    results_df = pd.read_csv('data/total.csv')
    results_df['Algorithm'] = results_df['Algorithm'].map(algorithms)
    time_df = pd.read_csv('data/time.csv')
    time_df['Algorithm'] = time_df['Algorithm'].map(algorithms)

    st.subheader('Порівняння генетичних алгоритмів')
    alpha = st.slider('Альфа :', 0.05, 0.3, 0.15, 0.05)
    population_size = st.slider('Розмір популяції:', 5, 50, 25, 5)
    candidates_num = st.slider('Кількість кандидатів:', 5, 50, 25, 5)
    st.altair_chart(create_genetic_chart(genetic_df[(genetic_df['Alpha']==alpha) & (genetic_df['PopulationSize']==population_size) & (genetic_df['CandidatesNum'] == candidates_num)]))
    
    st.subheader('\nПорівняння жадібних алгоритмів')
    st.altair_chart(create_greedy_chart(greedy_df))

    st.subheader('\nПорівняння всіх алгоритмів за значенням ЦФ')
    group_count = st.slider('Кількість груп:', 2, 7, 4)
    subgroups_count = st.slider('Кількість підгруп в кожній групі:', 2, 6, 3)
    st.altair_chart(create_result_chart(results_df[(results_df['GroupsNumber']==group_count) & (results_df['GroupMembers']==subgroups_count)],'Середня кількість кандидатів в комітеті', [1,180],'Algorithm','CandidatesNum','Result'))
    
    st.subheader('\nПорівняння всіх алгоритмів за часом виконання')
    group_count_time = st.slider('Кількість груп: ', 2, 7, 5)
    subgroups_count_time = st.slider('Кількість підгруп в кожній групі: ', 2, 6, 4)
    st.altair_chart(create_result_chart(time_df[(time_df['GroupsNumber']==group_count_time) & (time_df['GroupMembers']==subgroups_count_time)],'Час виконання алгоритму', [0,8],'Algorithm','CandidatesNum','Result'))
    

def show_manual_research_page():
    st.title('Мануальне дослідження з довільними параметрами')

    st.header('Оберіть параметри для генерування задач')
    num_of_tasks = st.slider('Кількість задач для кожного набору параметрів:', 1, 5, 3)
    st.subheader('Оберіть кількість кандидатів для задач')
    num_of_candidates_start = st.slider('Від:', 5, 15, 10, 5)
    num_of_candidates_stop = st.slider('До:', 20, 45, 30, 5)
    num_of_candidates_step = st.slider('Крок:', 5, 15, 10, 5)

    st.subheader('Оберіть додаткові параметри для кожної задачі')
    num_of_groups = st.slider('Кількість груп в кожній задачі:', 1, 6, 3)
    subgroups = [3]*num_of_groups
    st.subheader('Оберіть кількість підгруп в кожній групі')
    for group in range(num_of_groups):
        subgroups[group] = st.slider(f'Кількість підгруп в групі {group+1}', 2, 6, 3)

    tasks = []
    for num in range(num_of_candidates_start, num_of_candidates_stop+1, num_of_candidates_step):
        for task_num in range(num_of_tasks):
            tasks.append(get_data(num, subgroups))

    if isinstance(tasks, bool):
        st.header('Перевірте обрані параметри, будь ласка')
    else:
        algorithms = st.multiselect('Оберіть алгоритм', ('Жадібний алгоритм #1','Жадібний алгоритм #2','Жадібний алгоритм #3','Генетичний алгоритм #1','Генетичний алгоритм #2'))

        if 'Генетичний алгоритм #1' in algorithms or 'Генетичний алгоритм #2' in algorithms:
            st.subheader('Оберіть параметри для генетичного алгоритму')
            population_size = st.slider('Розмір популяції:', 0, 100, 10)
            alpha = st.slider('Альфа:', 0.0, 1.0, 0.5)
            iter_num = st.slider('Кількість ітерацій:', 1, 100, 20)

        if st.button('Показати результати експерименту'):
            results = pd.DataFrame(columns=['Номер задачі','Алгоритм',  'Кількість кандидатів', 'Розв\'язок', 'Значення ЦФ', 'Час виконання'])
            st.header('Відповідь')
            counter = 0
            for algorithm in algorithms:
                for i,candidates in enumerate(tasks):

                    args = [candidates]

                    if algorithm == 'Жадібний алгоритм #1':
                        fn = first_greedy_algorithm
                        args.append([0])
                    elif algorithm  == 'Жадібний алгоритм #2':
                        fn = second_greedy_algorithm
                        args.append([0])
                    elif algorithm  == 'Жадібний алгоритм #3':
                        fn = third_greedy_algorithm
                    elif algorithm  == 'Генетичний алгоритм #1' or algorithm  == 'Генетичний алгоритм #2':
                        args.append(population_size)
                        args.append(alpha)
                        args.append(iter_num)
                        if algorithm  == 'Генетичний алгоритм #1':
                            fn = first_genetic_algorithm
                        else:
                            fn = second_genetic_algorithm
                    results.loc[counter, 'Номер задачі'] = i
                    results.loc[counter, 'Алгоритм'] = algorithm
                    results.loc[counter, 'Кількість кандидатів'] = candidates.shape[0]
                    start = time.time()
                    result = fn(*args)
                    end = time.time()
                    results.loc[counter, 'Розв\'язок'] = result
                    results.loc[counter, 'Значення ЦФ'] = len(result)
                    results.loc[counter, 'Час виконання'] = end-start
                    counter += 1

            results = results.astype({'Значення ЦФ': 'float64', 'Кількість кандидатів': 'int32', 'Час виконання': 'float64'})
            grouped_results = results.groupby(['Алгоритм', 'Кількість кандидатів']).mean().reset_index()

            st.subheader('Значення ЦФ в залежності від кількості кандидатів')
            st.altair_chart(create_result_chart(grouped_results,'Значення ЦФ', [1,num_of_candidates_stop/2], 'Алгоритм', 'Кількість кандидатів', 'Значення ЦФ'))
            st.subheader('Час виконання алгоритму в залежності від кількості кандидатів')
            st.altair_chart(create_result_chart(grouped_results,'Час виконання', [0,ceil(results['Час виконання'].max())], 'Алгоритм', 'Кількість кандидатів', 'Час виконання'))
            st.subheader('Таблиця з розв\'язками усіх задачі')
            st.table(results)


if __name__ == '__main__':

    st.sidebar.title("Оберіть сторінку:")
    pages = ['Розв\'язок задачі', 'Міні-дослідження алгоритмів з довільними параметрами', 'Дослідження алгоритмів']
    page = st.sidebar.radio("Навігація", options=pages)

    if page == 'Розв\'язок задачі':
        show_main_page()

    elif page == 'Міні-дослідження алгоритмів з довільними параметрами':
        show_manual_research_page()

    elif page == 'Дослідження алгоритмів':
        show_research_page()

    