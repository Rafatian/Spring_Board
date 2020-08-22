import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import plotly_express as px
#import dash_auth


#VALID_USERNAME_PASSWORD_PAIRS = [
    #['Fundamental of DS', 'Project']
#]

sleep_data = pd.read_csv('sleep_clean_data.csv')
month_values_1= list(sleep_data.year_month.unique())
month_values_1.append('2019-02')

exercise_data = pd.read_csv('clean_exercise.csv')
month_values_2= list(exercise_data.year_month.unique())
month_values_2.append('2019-02')
duration_2= [0,20,40,60,80,100,160]
exercise_dict={'exercise_type=Custom':'Custom','exercise_type=Elliptical':'Elliptical','exercise_type=Running':'Running','exercise_type=Cycling':'Cycling','exercise_type=Hiking':'Hiking','exercise_type=Waling':'Waling','activity_hour_start':'starting hour of acitivity'}


step_data = pd.read_csv('step_count_clean_agg.csv')
climb_data= pd.read_csv('floor_clean.csv')
duration= list(range(0,61,5))
floor=list(np.sort(climb_data.floor.unique()))
floor.append(20)
step_data2= step_data.groupby('Date')['count','calorie','distance','Duration_in_min'].agg({'count': np.sum,\
                        'calorie': np.sum,'distance': np.sum, 'Duration_in_min': np.sum})
step_data2.reset_index(inplace=True)
label_dict={'count':'Total Step Count','calorie':'Total Calories Burned','distance':'Total Distance Travelled In Meters','Duration_in_min':'Total Walking Time In Minutes',\
    'walk_time_hour':'starting hour of Walking'}


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


app.config.suppress_callback_exceptions = True

#auth = dash_auth.BasicAuth(
    #app,
    #VALID_USERNAME_PASSWORD_PAIRS
#)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


index_page = html.Div([
    dcc.Link('Go Sleep Data Analysis', href='/sleep'),
    html.Br(),
    dcc.Link('Go to Excercise Data Analysis', href='/exercise'),
    html.Br(),
    dcc.Link('Go to Step and Floor Data Analysis', href='/step'),
    html.Br(),
    dcc.Link('Go to Conclusion', href='/conclusion'),
])

page_1_layout = html.Div(children=[
    html.H1(children='Health Data Analysis'),

    html.H2(children='''
        Sleep Data Analysis:
    '''),

        html.Label('Week-Days'),
            dcc.Checklist(
                id='day-filter_1',
                options=[
            {'label': 'Monday', 'value': 'Monday'},
            {'label': 'Tuesday', 'value': 'Tuesday'},
            {'label': 'Wednesday', 'value': 'Wednesday'},
            {'label': 'Thursday', 'value': 'Thursday'},
            {'label': 'Friday', 'value': 'Friday'},
            {'label': 'Saturday', 'value': 'Saturday'},
            {'label': 'Sunday', 'value': 'Sunday'}
        ],
        values=['Monday', 'Tuesday', 'Wednesday', 'Thursday','Friday','Saturday','Sunday'],
        style={'columnCount':4,'width': '30%'}
    ),
            
            dcc.RadioItems(
                id='category_1',
                options=[{'label': 'Sleep time', 'value': 'sleep_start_hour'},
                         {'label': 'Wake-up time', 'value': 'sleep_wakeup_hour'}],
                value='sleep_start_hour',
                labelStyle={'display': 'inline-block'},
                style= {'position': 'relative','bottom': '-10px'}
            ),
        
             html.Div([
                dcc.Graph(id='my-div-1'),
                dcc.Graph(id='my-div-12')],
                style= {'columnCount': 2,'position': 'relative','bottom': '-10px'}),
    
                  



     html.Div(
        dcc.RangeSlider(
        id='dates_1',    
        min=0,
        max=len(month_values_1)-1,
        value=[0, len(month_values_1)-1],
        
        marks={
        
        i: {'label': j} for i,j in enumerate(month_values_1)}),
        style={'width':'80%', 'position': 'relative','left': '180px'})


        
        
        
 
        

])


@app.callback(
    [Output('my-div-1', 'figure'),
    Output('my-div-12', 'figure')],
    [Input('category_1', 'value'),
    Input('day-filter_1', 'values'),
    Input('dates_1', 'value')]
)
def update_output_div(sleep,week,date):
    
     df= sleep_data.loc[(sleep_data['year_month']>=month_values_1[date[0]]) & (sleep_data['year_month']<month_values_1[date[1]]) & (sleep_data.week_day.isin(week)),[sleep,'sleep_duration_in_hour']]
     

     name = "Sleep Time" if sleep == 'sleep_start_hour' else 'Wake up Time'
      

    

     return (px.box(df, x=sleep, y='sleep_duration_in_hour', notched=False,labels={sleep:name,'sleep_duration_in_hour':'Amount Slept In Hours'},points='all'),
     px.histogram(df, x='sleep_duration_in_hour',labels={sleep:name,'sleep_duration_in_hour':'Amount Slept In Hours'}))


page_2_layout = html.Div(children=[
    html.H1(children='Health Data Analysis'),

    html.H2(children='''
        Exercise Data Analysis:
    '''),

        html.Label('Week-Days'),
            dcc.Checklist(
                id='day-filter_2',
                options=[
            {'label': 'Monday', 'value': 'Monday'},
            {'label': 'Tuesday', 'value': 'Tuesday'},
            {'label': 'Wednesday', 'value': 'Wednesday'},
            {'label': 'Thursday', 'value': 'Thursday'},
            {'label': 'Friday', 'value': 'Friday'},
            {'label': 'Saturday', 'value': 'Saturday'},
            {'label': 'Sunday', 'value': 'Sunday'}
        ],
        values=['Monday', 'Tuesday', 'Wednesday', 'Thursday','Friday','Saturday','Sunday'],
        style={'columnCount':4,'width': '30%'}
    ),
            
            
             html.Label('Activity Duration'),

             html.Div(
                dcc.RangeSlider(
                id='dur_1',    
                min=0,
                max=6,
                value=[0, 6],
        
                marks={
        
                0:'0', 1:'20',2:'40',3:'60',4:'80',5:'100',6:'160'}),
                style={'width':'30%','position': 'relative','left':'100px'}),
        
        
             html.Div([
                dcc.Graph(id='my-div-2')],
                style= {'position': 'relative','bottom': '-20px'}),


             html.Div(
                dcc.RangeSlider(
                id='dates_2',    
                min=0,
                max=len(month_values_2)-1,
                value=[0, len(month_values_2)-1],
        
                marks={
        
                i: {'label': str(j)} for i,j in enumerate(month_values_2)}),
                style={'width':'80%', 'position': 'relative','left': '180px','bottom': '-20px'}),


                dcc.RadioItems(
                id='category_2',
                options=[{'label': 'Daily Exercise Duraion', 'value': 'Duraion_in_min'},
                         {'label': 'Dialy Calorie Burn', 'value': 'calorie'}],
                value='Duraion_in_min',
                labelStyle={'display': 'inline-block'},
                style= {'position': 'relative','bottom': '-50px'}
            ),

             html.Div([   
                dcc.Graph(id='my-div-22')],
                style= {'position': 'relative','bottom': '-50px'}),
    
                  



     


        
        
        
 
        

])


@app.callback(
    [Output('my-div-2', 'figure'),
    Output('my-div-22', 'figure')],
    [Input('category_2', 'value'),
    Input('day-filter_2', 'values'),
    Input('dates_2', 'value'),
    Input('dur_1', 'value')]
)
def update_output_div(type,week,date,dur):
    
     df= exercise_data.loc[(exercise_data['year_month']>=month_values_2[date[0]]) & (exercise_data['year_month']<month_values_2[date[1]])\
          & (exercise_data.week_day.isin(week)) & (exercise_data['Duration_in_min']>=duration_2[dur[0]]) & (exercise_data['Duration_in_min']<=duration_2[dur[1]])]
     
     df1= exercise_data.loc[(exercise_data['year_month']>=month_values_2[date[0]]) & (exercise_data['year_month']<month_values_2[date[1]]) & (exercise_data.week_day.isin(week))]
     
     df2=df1.groupby('Date')['Duration_in_min','calorie'].agg({'Duration_in_min': np.sum,\
                        'calorie': np.sum, 'year_month':np.max})
     df2.reset_index(inplace=True)

     name = "calorie" if type == 'calorie' else 'Duration_in_min'
     name2=  'Duration_in_min' if name=='calorie' else 'calorie'
     

    

     return (px.scatter(df, x='Date', y='activity_hour_start',color='exercise_type',hover_name='Duration_in_min',labels=exercise_dict,title='Activities Start Time and Date'),
            px.scatter(df2, x="Date", y=name,size=name2,color=name,marginal_y='box',labels={'Duration_in_min':'Total Workout Per Day','calorie':'Total Calories Burned Per Day'}))



page_3_layout =   html.Div(children=[
    html.H1(children='Health Data Analysis'),

    html.H2(children='''
        Step and Floor Data Analysis:
    '''),

    
            
             html.Label('Walking Duration'),

             html.Div(
                dcc.RangeSlider(
                id='dur',    
                min=0,
                max=len(duration)-1,
                value=[0, len(duration)-1],
        
                marks={
        
                i: {'label': str(j)} for i,j in enumerate(duration)}),
                style={'width':'40%','position': 'relative','left':'100px'}),

                dcc.RadioItems(
                id='category',
                options=[{'label': 'Total Step Count', 'value': 'count'},
                         {'label': 'Total Calories Burned', 'value': 'calorie'},
                         {'label': 'Total Distance Travelled', 'value': 'distance'},
                         {'label': 'Total Walking Time', 'value': 'Duration_in_min'}],
                value='count',
                labelStyle={'display': 'inline-block'},
                style= {'position': 'relative','bottom': '-10px','left':'1000px'}
            ),
        
        
              html.Div([
                dcc.Graph(id='my-div'),
                dcc.Graph(id='my-div2')],
                style= {'columnCount': 2,'position': 'relative','bottom': '-10px'}),

             

             html.Div([   
                dcc.Graph(id='my-div3')],
                style= {'position': 'relative','bottom': '-50px'}),


             html.Label('Steps Climbed:',style={'position': 'absolute','left': '60px','bottom': '-545px'}),
             
             html.Div(
                dcc.RangeSlider(
                id='steps',    
                min=0,
                max=len(floor)-1,
                value=[0, len(floor)-1],
        
                marks={
        
                i: {'label': str(j)} for i,j in enumerate(floor)}),
                style={'width':'80%', 'position': 'relative','left': '180px','bottom': '-40px'}),
    
                  

       

])


@app.callback(
    [Output('my-div', 'figure'),
    Output('my-div2', 'figure'),
    Output('my-div3', 'figure')],
    [Input('category', 'value'),
    Input('steps', 'value'),
    Input('dur', 'value')]
)
def update_output_div(Yval,floors,minute):
    
     df= step_data[(step_data['Duration_in_min']>=duration[minute[0]]) & (step_data['Duration_in_min']<duration[minute[1]])]
     df2=step_data2.copy()
     
     df3= climb_data.loc[(climb_data['floor']>=floor[floors[0]]) & (climb_data['floor']<floor[floors[1]])]
     
     

     title_1 = label_dict[Yval]
     
     

    

     return (px.scatter(df, x='Date', y='walk_time_hour',color='Duration_in_min',labels=label_dict,title='Walking Start Time and Date'),
            px.scatter(df2, x="Date", y=Yval,marginal_y='box',labels=label_dict,title=title_1),
            px.scatter(df3, x="Date", y='climb_time_hour',color='floor',labels={'climb_time_hour':'Hour'},title='Hour and Number of Floors Climbed Per Day'))


page_4_layout =   html.Div(children=[
    html.H1(children='Health Data Analysis'),

    html.H2(children='''
        Preprocessing:
    '''),
    
    html.Div('''Column selection of the data was done based on the amount of data availabe in each column and if the information provided could have been
    interpereted and showed useful information. In the preprocessing of sleep data nothing valuable was found in the quality column in the sleep data.
    Date conversion was done for all data except for the sleep data. The change in time zones from UTC -400 to UTC -500 happens because of daylight saving
    since it happens on March 11th and November 4th.'''),
    html.Br(),
    html.H2('Sleep Analysis:'),
    html.Div('''Looking at how the individual sleeps during weekdays and weekends shows that wakeup time for this individual is pretty consistent. The individual wakes up mostly around
    4 to 6 am in the morning even on Sundays and Saturdays. There is no specific weekday that he wakes up later in the morning. The amount of sleep that the individual has is around 8 to
    9 hours per day and the individual tends to sleep around 20 to 23 pm. Nothing specific was observed regarding Trend in seasons'''),
    html.Br(),
    html.H2('Exercise Analysis:'),
    html.Div('''The few instances of work out captured around early 2017 was ignored in my analysis. Running activities having a duration more than 20 min mostly happens between 7 to 8
    am in the morning or in the afternoon around 14 to 16 pm. During week days Running happens mostly in the morning.
    Cycling activity during the week is mostly done between 15 to 18. During weekends between January to March, most of the cycling happended before 10 am after November mostly happend 
    between 14 to 18. There are lots of instances of hiking during the week and weekend and it is consistent through out year 2018. Generally less workout activity happens between hours 8 to 14
    which might be an indication of daytime job.
    Cycling is one of the activities that the individual does more than 40 minutes per instance.
    Overall the individual workouts 42 minutes on average during weekdays and burns 252 calories on average. On weekends he workouts a bit more on average 51 minutes and 286 calories.'''),
    html.Br(),
    html.H2('Step and Floor Climb Analysis:'),
    html.Div('''Most of the walking more than 20 minutes happen between hours 20 to 22 and walking duration between 10 to 20 happens mostly after 12 pm. On average individual walks 2000
    meters and burns 135 calories by walking. Climbing 9 steps mostly happens after 8 pm and some between hours 12 to 13. Lots of one step instances scattered between 10 am to 20pm.'''),
    html.Br(),
    html.H2('Overall Conclusion:'),
    html.Div('''This individual has a healthy life style and workouts pretty much everyday. Based on the heart rate data and the individuals activity, the individual should be male and 
    around 18 to 35 years old. He must have some kind of a daily job because he does much less activity around hours 8 to 16. He burns about 400 calories per day by working out and walking
    which shows he is healthy. He is not a party person because he mostly wakes up around 5 to 6 am even on weekends.''')
    ])          


# Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/sleep':
        return page_1_layout
    elif pathname == '/exercise':
        return page_2_layout
    elif pathname == '/step':
        return page_3_layout
    elif pathname == '/conclusion':
        return page_4_layout    
    else:
        return index_page
    # You could also return a 404 "URL not found" page here


if __name__ == '__main__':
    app.run_server(debug=True)