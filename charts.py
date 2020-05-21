import altair as alt
import pandas as pd


def prepare_data(candidates, result):
    raw_df = pd.DataFrame(candidates[result,:], index=result)
    df = pd.DataFrame(columns = ['Group', 'Candidate', 'Value'])
    counter = 0
    for group in raw_df:
        for i,elem in zip(raw_df.index,raw_df[group]):
            df.loc[counter, 'Group'] = group
            df.loc[counter, 'Candidate'] = i
            df.loc[counter, 'Value'] = ('Відсутня' if elem == 0 else 'Наявна')
            counter += 1
    return df


def create_chart(candidates, result):
    df = prepare_data(candidates, result)
    chart = alt.Chart(df.sort_values(by=['Group']), height=len(result)*75).mark_rect().encode(
        x=alt.X('Group:N', title='Групи', sort=sorted(set(df['Group']))),
        y=alt.Y('Candidate:N', title='Кандидати'),
        color=alt.Color('Value:N',title='Наявність групи', scale=alt.Scale(scheme='category10'))
    )
    return chart


def create_genetic_chart(data):
    scales = alt.selection_interval(bind='scales')
    chart = alt.Chart(data, height=500, width=850).mark_line(point=True).encode(
        x=alt.X('IterationNumber:N', title='Кількість ітерацій'),
        y=alt.Y('Result',
            scale=alt.Scale(domain=[1,15]),
            title='Середня кількість кандидатів в комітеті', 
            sort=sorted(set(data['Result']), reverse=True)
            ),
        color=alt.Color('Algorithm:N',title='Алгоритм', scale=alt.Scale(scheme='category10')),
        tooltip=alt.Tooltip('Result', title='Значення ЦФ')
    ).add_selection(
        scales
    ).configure_point(
        size=80
    )
    return chart


def create_greedy_chart(data):
    scales = alt.selection_interval(bind='scales')
    chart = alt.Chart(data, height=500, width=850).mark_line(point=True).encode(
        x=alt.X('CandidatesNum:N', title='Кількість кандидатів'),
        y=alt.Y('Result',
            axis=alt.Axis(tickMinStep=0.2),
            title='Середня кількість кандидатів в комітеті', 
            sort=sorted(set(data['Result']), reverse=True)
           ),
        color=alt.Color('Algorithm:N',title='Алгоритм', scale=alt.Scale(scheme='category10')),
        tooltip=alt.Tooltip('Result', title='Значення ЦФ')
    ).add_selection(
        scales
    ).configure_point(
        size=80
    )
    return chart


def create_result_chart(data, title, domain):
    scales = alt.selection_interval(bind='scales')
    selection = alt.selection_multi(fields=['Algorithm'], bind='legend')
 
    chart = alt.Chart(data, height=500, width=850).mark_line(point=True).encode(
        x=alt.X('CandidatesNum:N', title='Кількість кандидатів'),
        y=alt.Y('Result',
            scale=alt.Scale(domain=domain),
            title=title, 
            sort=sorted(set(data['Result']), reverse=True)
           ),
        color=alt.Color('Algorithm:N',title='Алгоритм', scale=alt.Scale(scheme='category10')),
        opacity=alt.condition(selection, alt.value(1), alt.value(0.2)),
        tooltip=alt.Tooltip('Result', title=title)
    ).add_selection(
        scales, selection
    ).configure_point(
        size=80
    )


    return chart 
