import dash
from dash import dcc
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from dash.dependencies import Input, Output, State
from dash import dash_table
from dash import Dash, html, dcc
from  dash_bootstrap_components import FormGroup,Button, Row, Col, Card, CardBody,themes
from dash import html as html2
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__,
external_stylesheets=external_stylesheets)

# STYLOS
colors = {
    'title':'blue',
    'background': 'aliceblue',
    'text': 'darkgrey'
}
# the style arguments for the sidebar.
SIDEBAR_STYLE = {
    'position': 'fixed',
    'top': 0,
    'left': 0,
    'bottom': 0,
    'width': '20%',
    'padding': '20px 10px',
    'background-color': '#f8f9fa'
}

# the style arguments for the main content page.
CONTENT_STYLE = {
    'margin-left': '25%',
    'margin-right': '5%',
    'top': 0,
    'padding': '20px 10px'
}

TEXT_STYLE = {
    'textAlign': 'center',
    'color': '#191970'
}

CARD_TEXT_STYLE = {
    'textAlign': 'center',
    'color': '#0074D9'
}

CARD_TEXT_STYLE2 = {
    'textAlign': 'center',
    'color': '#FFFFFF'
}

#DATOS
indicadores= pd.read_csv('variables_rating_app.csv', sep=';')
empresas_disponibles=list(indicadores.empresa.unique())
años_disponibles=list(indicadores.año.unique())

empresas_disponibles = [x for x in empresas_disponibles if pd.isnull(x) == False]
años_disponibles = [x for x in años_disponibles if np.isnan(x) == False]

sectores= pd.read_csv('tabla_sectores_it3.csv', sep=';')
rating= pd.read_csv('resultados_rating_app.csv')
informados= pd.read_csv('porc_informadas_app.csv')
tabla_pesos=pd.read_csv('tabla_pesos_tema.csv', sep=';')

controls = FormGroup(
    [
        html2.P('Empresa', style={
            'textAlign': 'center'
        }),
        dcc.Dropdown(
            id='dropdown_empresas',
            options=[{'label': i, 'value': i} for i in empresas_disponibles]
            #value=['value1'],  # default value
            #multi=True
        ),
 html2.Br(),
        html2.P('Año', style={
            'textAlign': 'center'
        }),
        dcc.Dropdown(
            id='dropdown_años',
            options=[{'label': i, 'value': i} for i in años_disponibles]
            #value=['value1'],  # default value
            #multi=True
        ),
        html2.Br(),

        html2.P('Tipo Rating', style={
            'textAlign': 'center'
        }),
       dcc.RadioItems(
            id='tipo_rating',
    options=[
       {'label': 'Ranking total', 'value': 'total'},
       {'label': 'Ranking cualitativo', 'value': 'cual'},
   ]
        ),
       
    ]
)


sidebar = html2.Div(
    [
        html2.H2('Parameters', style={'text-align': 'center','color': colors['title']}),
        html2.Hr(),
        controls
    ],
    style=SIDEBAR_STYLE,
)

content_first_row = Row([
    Col(
        Card(
            [

                CardBody(
                    [
                        html2.H4(id='card_title_1', children=['Empresa'], className='card-title',
                                style=CARD_TEXT_STYLE),
                        html2.P(id='card_text_1',  style=CARD_TEXT_STYLE),
                    ]
                )
            ]
        ),
        md=3
    ),
    Col(
        Card(
            [

                CardBody(
                    [
                        html2.H4(id='card_title_2', children=['Año'], className='card-title',
                                style=CARD_TEXT_STYLE),
                        html2.P(id='card_text_2',  style=CARD_TEXT_STYLE),
                    ]
                )
            ]
        ),
        md=3
    ),
    Col(
        Card(
            [

                CardBody(
                    [
                        html2.H4(id='card_title_3', children=['Sector'], className='card-title',
                                style=CARD_TEXT_STYLE),
                        html2.P(id='card_text_3', style=CARD_TEXT_STYLE),
                    ]
                )
            ]
        ),
        md=3
    ),
    Col(
        Card(
            

                CardBody(
                    [
                        html2.H4(id='card_title_4', children=['Score'], className='card-title',
                                style=CARD_TEXT_STYLE),
                        html2.P(id='card_text_4',style=CARD_TEXT_STYLE),
                    ]
                ), style={"width": "18rem","border-radius":"2%","background":"PowderBlue"}
            
        ),
        md=3
    ),
    
] ,justify="center")


content_tab_1 = Row([
    Col([

        Row(
        html.Div([

            html.Br(),
            html.H1(children='INDICADORES',style={
            
            'color': colors['text'], 'textAlign': 'center','font-size':'large'
                }),
            html.Br(),
            dash_table.DataTable(
            id='table-nir',editable=True,
            style_cell={'padding': '5px'},
            style_header={
            'backgroundColor': 'grey',
            'fontWeight': 'bold'
    }
            
            )])

        )
        ,
        Row(
        html.Div([

            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.H1(children='COMPARACIÓN CON EL SECTOR',style={
            
            'color': colors['text'], 'textAlign': 'center','font-size':'large'
                }),
            html.Br(),
            dcc.Graph(
            id='graph-sector'
        )
            ])

        )



    ],md=3,width=3,
    ),


    Col([
        
        Row(
            
        html.Div([
            html.Br(),
            html.H1(children='CONTRIBUCCIÓN EN PESOS DE LOS TEMAS',style={
            
            'color': colors['text'],'textAlign': 'center', 'font-size':'large'
        }),
        
        dcc.Graph(
            id='graph-pesos'
        )
            
            ])
        
    )
    
    ,

            Row(
        html.Div([
            
           
            
            html.H1(children='EVOLUCIÓN HISTÓRICA',style={
            
            'color': colors['text'],'textAlign': 'center','font-size':'large'
        }),
        dcc.Graph(
            id='graph-hist'
        )
            
            ])
        
    )],
    
    
    
        md=3,width={"size": 9, "offset": 3}
    
    ),

    
])

content_tab_2 = Col([

        Row([

        
        html.Div([
            html.Br(),
            html.H1(children='COMPARACIÓN IBEX 35',style={
            
            'color': colors['text'],'textAlign': 'center', 'font-size':'large'
        }),
        html.Br(),
    
        dcc.Graph(
            id='graph-ibex'
        )     
            ])
         ,],justify="center"),

        Row([

        
        html.Div([
            html.Br(),
            html.H1(children='% INDICADORES INFORMADOS',style={
            
            'color': colors['text'],'textAlign': 'center', 'font-size':'large'
        }),

        html.Br(),
        dcc.Graph(
            id='graph-informados'
        )
            
            ])
        
    
        ,],justify="center"),])

        

       
    
  

    



content = html2.Div(
    [
        html2.H2('RATING ENVIRONMENT IBEX 35 ', style=TEXT_STYLE),
html.Br(),
        content_first_row,
       html.Br(),
    
        html2.Hr(),

        dcc.Tabs([
            dcc.Tab(
                label='Información',
                children = [content_tab_1]

            ),

        dcc.Tab(
                label='Ranking IBEX 35',
                children = [content_tab_2]

            ),

    ]),
        
        html2.Hr(),
 
    ],
    style=CONTENT_STYLE
)

app = dash.Dash(external_stylesheets=[themes.BOOTSTRAP])
app.layout = html.Div([sidebar, content])






@app.callback(
    Output('card_text_1', 'children'),
    
    Input('dropdown_empresas', 'value')
    )
def update_card_text_1( dropdown_value_e):
    return dropdown_value_e

@app.callback(
    Output('card_text_2', 'children'),
    
    [Input('dropdown_años', 'value')
     ])
def update_card_text_2(  dropdown_value_a):
    print(dropdown_value_a)
    return dropdown_value_a

@app.callback(
    Output('card_text_3', 'children'),
    Input('dropdown_empresas', 'value')
    )
def update_card_text_3(value_e):
    sector= sectores[sectores.empresa==value_e].sector
    return sector

@app.callback(
    Output('card_text_4', 'children'),
    
   [Input('dropdown_empresas', 'value'),Input('dropdown_años', 'value'), Input('tipo_rating','value')]
    )
def update_card_text_1( value_e,value_a, tipo_rating):
    data= rating[rating.empresas==value_e]
    data= data[data.año==value_a]
    if tipo_rating=='total':
        score=data.score
        return score
    if tipo_rating=='cual':
        score=data.score_cualitativo
        return score

@app.callback(
    [Output("table-nir", "data"),
         Output('table-nir', 'columns')],
    [Input('dropdown_años', 'value'),Input('dropdown_empresas', 'value'), Input('tipo_rating','value')])
def update_output(selected_año,selected_empresa, selected_type):

    if selected_año!='None' and selected_empresa!='None' and selected_type!='None'  :

        filtered_df = indicadores[indicadores.año == selected_año]
        filtered_df = filtered_df[filtered_df.empresa == selected_empresa]
        if selected_type=='total':
            filtered_df=filtered_df.loc[:,['variable','valor']]
            col=[{'id': i, 'name': i}  for i in filtered_df.columns]
        if selected_type=='cual':
            filtered_df = filtered_df[filtered_df.tipo == 'cualitativo']
            filtered_df=filtered_df.loc[:,['variable','valor']]
            col=[{'id': i, 'name': i}  for i in filtered_df.columns]

        return [filtered_df.to_dict('records'),col]
@app.callback(
    Output('graph-pesos', 'figure'),
    [Input('dropdown_empresas', 'value')])
def update_figure(empresa):

    if empresa!='None'  :
        sector = list(sectores[sectores.empresa == empresa].sector)[0]
        
        df = tabla_pesos[tabla_pesos.sector==sector]
        
    
        fig = px.pie(df, values='peso', names='tema',hole=.3,height=600, width=500)

            
            
        fig.update_layout(transition_duration=500)
        fig.update_layout(legend=dict(
            yanchor="top",
            y=1.50,
            xanchor="left",
            x=0.01
        ))
        return fig

@app.callback(
    Output('graph-sector', 'figure'),
    [Input('dropdown_empresas', 'value'),Input('dropdown_años', 'value'), Input('tipo_rating','value')])
def update_figure(empresa,value_año,tipo_rating):

    if empresa!='None' and value_año!='None'  and tipo_rating!='None'  :
        sector = list(sectores[sectores.empresa == empresa].sector)[0]
        
        empresas_mismo_sector=list(sectores[sectores.sector == sector].empresa)
        
        scores_mismo_sector=[]
        empresas_mismo_sector_con_datos=[]

        if tipo_rating=='total':
            for e in empresas_mismo_sector:
                try:
                    data=rating[rating.empresas==e]

                    
                    score_s=list(data[data.año==value_año].score)[0]
                    
                    empresas_mismo_sector_con_datos.append(e)
                    scores_mismo_sector.append(score_s)
                    
                except:
                    pass

            
            data_scores=pd.DataFrame()
            
            data_scores['rating']= scores_mismo_sector
            data_scores['empresa']=empresas_mismo_sector_con_datos
            
            data_scores['rating'] = data_scores['rating'].astype('float64')
            
            frase="Empresas del sector "+sector
        
            fig = px.bar(data_scores, x="empresa", y="rating", title="",height=350, width=500)
            fig.update_layout(
            
            xaxis_title=frase,
            yaxis_title="Score",
            yaxis_range=[0,100],
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            font_color=colors['text']
        )
            
            
            fig.update_layout(transition_duration=500)

        if tipo_rating=='cual':
            for e in empresas_mismo_sector:
                try:
                    data=rating[rating.empresas==e]

                    
                    score_s=list(data[data.año==value_año].score_cualitativo)[0]
                    
                    empresas_mismo_sector_con_datos.append(e)
                    scores_mismo_sector.append(score_s)
                    
                except:
                    pass

            
            data_scores=pd.DataFrame()
            
            data_scores['rating']= scores_mismo_sector
            data_scores['empresa']=empresas_mismo_sector_con_datos
            
            data_scores['rating'] = data_scores['rating'].astype('float64')
            
            frase="Empresas del sector "+sector
        
            fig = px.bar(data_scores, x="empresa", y="rating", title="",height=350, width=500)
            fig.update_layout(
            
            xaxis_title=frase,
            yaxis_title="Score",
            yaxis_range=[0,100],
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            font_color=colors['text']
        )
            
            
            fig.update_layout(transition_duration=500)
        return fig

@app.callback(
    Output('graph-hist', 'figure'),
    [Input('dropdown_empresas', 'value'), Input('tipo_rating','value')])
def update_figure(empresa,tipo_rating):
    if empresa!='None' and tipo_rating!='None'  :
    # para calcular el grafico de su historial
        data=rating[rating.empresas==empresa]
        años_disponibles_2=list(data.año.unique())



        if tipo_rating=='total':
            scores=[]
            for año in años_disponibles_2:
                score_s=list(data[data.año==año].score)[0]
                scores.append(score_s)

            data_scores=pd.DataFrame()
            data_scores['rating']= scores
            data_scores['años']=años_disponibles_2
            data_scores['rating'] = data_scores['rating'].astype('float64')
            data_scores['años'] = data_scores['años'].astype('object')

            # calcular grafico con score medio de sector
            sector = list(sectores[sectores.empresa == empresa].sector)[0]

            empresas_mismo_sector=list(sectores[sectores.sector == sector].empresa)
            
            score_medio_años=[]
            for año in años_disponibles_2:

                scores_mismo_sector=[]
                empresas_mismo_sector_con_datos=[]
                for e in empresas_mismo_sector:
                    try:
                        data=rating[rating.empresas==e]

                        
                        score_s=list(data[data.año==año].score)[0]
                        
                        empresas_mismo_sector_con_datos.append(e)
                        scores_mismo_sector.append(score_s) 
                        
                    except:
                        pass
            
            
                score_medio_años.append(np.mean(scores_mismo_sector)) 
            
            data_medio=pd.DataFrame()
            data_medio['rating']= score_medio_años
            data_medio['años']=años_disponibles_2
            data_medio['rating'] = data_medio['rating'].astype('float64')
            data_medio['años'] = data_medio['años'].astype('object')

        if tipo_rating=='cual':
            scores=[]
            for año in años_disponibles_2:
                score_s=list(data[data.año==año].score_cualitativo)[0]
                scores.append(score_s)

            data_scores=pd.DataFrame()
            data_scores['rating']= scores
            data_scores['años']=años_disponibles_2
            data_scores['rating'] = data_scores['rating'].astype('float64')
            data_scores['años'] = data_scores['años'].astype('object')
    
            # calcular grafico con score medio de sector
            sector = list(sectores[sectores.empresa == empresa].sector)[0]

            empresas_mismo_sector=list(sectores[sectores.sector == sector].empresa)
            
            score_medio_años=[]
            for año in años_disponibles_2:

                scores_mismo_sector=[]
                empresas_mismo_sector_con_datos=[]
                for e in empresas_mismo_sector:
                    try:
                        data=rating[rating.empresas==e]

                        
                        score_s=list(data[data.año==año].score_cualitativo)[0]
                        
                        empresas_mismo_sector_con_datos.append(e)
                        scores_mismo_sector.append(score_s) 
                        
                    except:
                        pass
            
            
                score_medio_años.append(np.mean(scores_mismo_sector)) 
            
            data_medio=pd.DataFrame()
            data_medio['rating']= score_medio_años
            data_medio['años']=años_disponibles_2
            data_medio['rating'] = data_medio['rating'].astype('float64')
            data_medio['años'] = data_medio['años'].astype('object')
        

        # grafico

        try:

            nombre_score='Score '+empresa
            nombre_medio='Score medio' +'\n' +sector
            fig = go.Figure()

            fig.add_trace(go.Bar(x=data_scores['años'], y=data_scores['rating'], name=nombre_score))
            fig.add_trace(go.Scatter(x=data_medio['años'], y=data_medio['rating'], name=nombre_medio,line=dict(color="crimson")))

            

            #fig = px.bar(data_scores, x="años", y="rating", title="",height=350, width=500)
            fig.update_layout(
            
            xaxis_title='Año',
            yaxis_title="Score",
            width=int(500),
            yaxis_range=[0,100],
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            font_color=colors['text']
        )
            
            fig.update_layout(transition_duration=500)
            fig.update_layout(legend=dict(
            yanchor="top",
            y=1.20,
            xanchor="left",
            x=0.01
        ))
            return fig
        except:
            pass

@app.callback(
    Output('graph-informados', 'figure'),
    [Input('dropdown_años', 'value'), Input('tipo_rating','value')])

def update_figure(value_año, tipo):
    if tipo!='None' and value_año!='None'  :
        data=informados[informados.año==value_año]

        empresa_disponibles_2=list(data.empresa.unique())
        
        if tipo=='total':

            porc=[]
            for empresa in empresa_disponibles_2:
                porc_s=list(data[data.empresa==empresa]['%_informadas'])[0]
                porc.append(porc_s)

            data_scores=pd.DataFrame()
            data_scores['%_informadas']= porc
            data_scores['empresa']=empresa_disponibles_2
            data_scores['%_informadas'] = data_scores['%_informadas'].astype('float64')
            data_scores['empresa'] = data_scores['empresa'].astype('object')
            data_scores=data_scores.sort_values('%_informadas', ascending=False)
            fig = px.bar(data_scores, x="empresa", y="%_informadas", title="",height=350, width=500)
            fig.update_layout(
            
            xaxis_title='Empresa',
            yaxis_title="%_informadas",
            yaxis_range=[0,100],
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            font_color=colors['text']
        )
            fig.update_layout(width=int(600))
            fig.update_layout(transition_duration=500)
            return fig
        
        if tipo=='cual':
            porc=[]
            for empresa in empresa_disponibles_2:
                porc_s=list(data[data.empresa==empresa]['%_informadas_cualitativas'])[0]
                porc.append(porc_s)

            data_scores=pd.DataFrame()
            data_scores['%_informadas']= porc
            data_scores['empresa']=empresa_disponibles_2
            data_scores['%_informadas'] = data_scores['%_informadas'].astype('float64')
            data_scores['empresa'] = data_scores['empresa'].astype('object')
            data_scores=data_scores.sort_values('%_informadas', ascending=False)
            fig = px.bar(data_scores, x="empresa", y="%_informadas", title="",height=350, width=500)
            fig.update_layout(
            
            xaxis_title='Empresa',
            yaxis_title="%_informadas",
            yaxis_range=[0,100],
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            font_color=colors['text']
        )
            fig.update_layout(width=int(600))
            fig.update_layout(transition_duration=500)

            return fig

@app.callback(
    Output('graph-ibex', 'figure'),
    [Input('dropdown_años', 'value'), Input('tipo_rating','value')])
def update_figure(value_año, tipo):
    if tipo!='None' and value_año!='None'  :
        data=rating[rating.año==value_año]
        data_inf=informados[informados.año==value_año]
        empresa_disponibles_2=list(data.empresas.unique())
        
        if tipo=='total':

            scores=[]
            porc=[]
            for empresa in empresa_disponibles_2:
                score_s=list(data[data.empresas==empresa].score)[0]
                scores.append(score_s)
                try:
                    porc_s=list(data_inf[data_inf.empresa==empresa]['%_informadas'])[0]
                    porc.append(porc_s)
                except:
                    porc.append(0)

            data_scores=pd.DataFrame()
            data_scores['rating']= scores
            data_scores['%_informadas']= porc
            data_scores['empresa']=empresa_disponibles_2
            data_scores['rating'] = data_scores['rating'].astype('float64')
            data_scores['%_informadas'] = data_scores['%_informadas'].astype('float64')
            data_scores['empresa'] = data_scores['empresa'].astype('object')
            data_scores=data_scores.sort_values('rating', ascending=False)

            nombre_score='Score'
            nombre_medio='% variables informadas' 
            fig = go.Figure()

            fig.add_trace(go.Bar(x=data_scores['empresa'], y=data_scores['rating'], name=nombre_score))
            fig.add_trace(go.Scatter(x=data_scores['empresa'], y=data_scores['%_informadas'], name=nombre_medio,line=dict(color="crimson")))

            fig.update_layout(
            
            xaxis_title='Año',
            yaxis_title="Score",
            width=int(500),
            yaxis_range=[0,100],
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            font_color=colors['text']
                )
            
            fig.update_layout(transition_duration=500)
            fig.update_layout(legend=dict(
            yanchor="top",
            y=1.20,
            xanchor="left",
            x=0.01
                ))
            return fig
        
        if tipo=='cual':
            scores=[]
            porc=[]
            for empresa in empresa_disponibles_2:
                score_s=list(data[data.empresas==empresa].score_cualitativo)[0]
                scores.append(score_s)
                try:
                    porc_s=list(data_inf[data_inf.empresa==empresa]['%_informadas_cualitativas'])[0]
                    porc.append(porc_s)
                except:
                    porc.append(0)

            data_scores=pd.DataFrame()
            data_scores['rating']= scores
            data_scores['%_informadas']= porc
            data_scores['empresa']=empresa_disponibles_2
            data_scores['rating'] = data_scores['rating'].astype('float64')
            data_scores['%_informadas'] = data_scores['%_informadas'].astype('float64')
            data_scores['empresa'] = data_scores['empresa'].astype('object')
            data_scores=data_scores.sort_values('rating', ascending=False)

            nombre_score='Score'
            nombre_medio='% variables informadas' 
            fig = go.Figure()

            fig.add_trace(go.Bar(x=data_scores['empresa'], y=data_scores['rating'], name=nombre_score))
            fig.add_trace(go.Scatter(x=data_scores['empresa'], y=data_scores['%_informadas'], name=nombre_medio,line=dict(color="crimson")))

            fig.update_layout(
            
            xaxis_title='Año',
            yaxis_title="Score",
            width=int(500),
            yaxis_range=[0,100],
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            font_color=colors['text']
                )
            
            fig.update_layout(transition_duration=500)
            fig.update_layout(legend=dict(
            yanchor="top",
            y=1.20,
            xanchor="left",
            x=0.01
                ))
            return fig


if __name__ == '__main__':
    app.run_server(host="0.0.0.0",debug=False, port=8080)
