from dash import Dash, html, callback, dcc, Input, Output, ctx, no_update, State
from dash.exceptions import PreventUpdate
import re
import os
import psycopg2
from dotenv import load_dotenv
import plotly.express as px
import plotly.graph_objects as go

fondo_grande = "assets/fondo_grande.mp4"
fondo_pequeno = "assets/fondo_pequeno.mp4"
avatar = "assets/avatar.png"

nombre_usuario = "cristian arboleda"

links=[
    {"tipo": "texto", "texto": "github", "url": "https://github.com/Cristian-Arboleda", "imagen": "assets/iconos/github.png"},
    {"tipo": "texto", "texto": "web_page", "url": "", "imagen": "assets/iconos/pagina_web.png"},
    {"tipo": "texto", "texto": "linkedin", "url": "", "imagen": "assets/iconos/linkedin.png"},
    {"tipo": "texto", "texto": "youtube", "url": "", "imagen": "assets/iconos/youtube.png"},
    {"tipo": "texto", "texto": "facebook", "url": "", "imagen": "assets/iconos/facebook.png"},
    {"tipo": "texto", "texto": "tiktok", "url": "", "imagen": "assets/iconos/tiktok.png"},
    {"tipo": "texto", "texto": "instagram", "url": "", "imagen": "assets/iconos/instagram.png"},
]


# links ----------------------------------------------------
links_html = html.Div(
    id="contenedor_links",
    children=[
        *[
            html.A(
                className='link',
                href=link['url'],
                target='_blank',
                children=[
                    html.Img(
                        src=link['imagen'],
                        className='imagen_link',
                    ),
                    html.P(
                        children=link['texto'].title().replace('_', ' '),
                        className='texto_link'
                    ),
                    html.P('⚡'),
                ]
            )
            for link in links
        ],
    ]
)

# Video destacado -------------------------------------------------------
videos_destacados_html = html.Div(
    id='contenedor_featured',
    children=[
        html.Iframe(
            src='https://www.youtube.com/embed/--pxv_RCjOg?si=OsuLfLq73Ide8dAh',
            id='video_destacado',
        ),
    ]
)

# About me ------------------------------------------------------------------------------------------------------
about_me_message = """
Hello, thank you for being here. My name is Cristian. I'm a self-taught enthusiast and enjoy delving deeply into my passions.
I have an academic background in statistics, programming, and artificial intelligence (Universidad del Valle), and I complement that foundation with additional courses that keep my skills up-to-date. 
I consider myself responsible, punctual, and highly committed to the projects I work on. I'm results-oriented, detail-oriented, and eager to learn and apply new tools. I seek opportunities to contribute rigorous analysis, data-driven solutions, and well-structured code to challenging projects.
"""
# Datos
skills = ['python', 'SQL', 'machine_learning', 'dashboards_&_data_visualization','mathematics', 'statistics', 'english', 'rstudio', ]
datos = {
    "skills": [skill.replace('_', ' ').title() for skill in skills],
    "porcent": [95, 70, 70, 80, 50, 50, 40, 30]
}
colors = ['yellow', 'pink', 'green', 'violet', 'tomato', 'orange', 'royalblue', 'purple']
# iniciar grafico
fig = go.Figure()

fig.add_trace(go.Bar(
    x=datos['porcent'],
    y=datos['skills'],
    orientation='h',
    textposition='inside',
    showlegend=False,
    marker=dict(
        color=colors, # colores de las barras
        line=dict(color='black') # color de la linea de la barra
    ),
    text=datos['skills'],
    insidetextanchor='start', # Orden donde inicia el texto dentro de las barras
    textfont=dict(color='black', size=13),
    hoverlabel=dict(bgcolor='black'), # Fondo de la etiqueta
    hovertemplate="(%{x}, %{y})<extra></extra>", # Desactiva las etiquetas adicionales
))

# Trazado de texto para los valores fueta del texto a la derecha
fig.add_trace(go.Scatter(
    x=datos['porcent'],
    y=datos['skills'],
    mode='text',
    text=[f'{value}%' for value in datos['porcent']],
    textposition='middle right',
    showlegend=False,
    hoverinfo='skip',
    marker=dict(color='white',),  
    textfont=dict(color='white', size=13), # estilos del texto exterior
))

#
fig.update_layout(
    plot_bgcolor='rgba(0,0,0,0)', # quitar fondo intero
    paper_bgcolor='rgba(0,0,0,0)', # quitar fondo externo
    margin=dict(l=0, r=0, t=0, b=0), # disminuir area alrededor del grafico
    width=400,
    height=300,
    yaxis=dict(autorange='reversed'), # Invierte el orden de las categorias del eje y
    dragmode=False, # desactiva el zoom con el cursor
    hovermode='closest' #desactivas la etiquetas adicionales
)

# Ejes
fig.update_xaxes(
    showticklabels=False, # Dasactiva los valores del eje x
    showgrid=False, # Desactiva la cuadricula del eje x
    zeroline=False, # Desactiva la linea base del eje x
)
fig.update_yaxes(
    showticklabels=False, # Desactiva los valor del eje y
)
all_buttons = [
    "zoom2d", "pan2d", "select2d", "lasso2d",
    "zoomIn2d", "zoomOut2d", "autoScale2d", "resetScale2d",
    "hoverClosestCartesian", "hoverCompareCartesian",
    "zoom3d", "pan3d", "orbitRotation", "tableRotation",
    "zoomInGeo", "zoomOutGeo", "resetGeo", "hoverClosestGeo",
    "hoverClosestGl2d", "hoverClosestPie", "toggleHover",
    "resetViews", "toggleSpikelines", "resetViewMapbox"
]
grafico = dcc.Graph(
    figure=fig,
    config={"displayModeBar": True, "modeBarButtonsToRemove": all_buttons, 'displaylogo': False,},
)

app = html.Div(
    id='contendor_app',
    children=[
        html.Div(
            id='contenedor_app_iconos',
            children=[
                html.Img(
                    src=f'assets/iconos/{skill}.png',
                    className='app_icono'
                )
                for skill in skills
            ]
        ),
        grafico
    ]
)

code = html.Div(
    id='contenedor_code',
    children=[
        dcc.Textarea(
            id='code',
            value=str(fig),
            readOnly=True,
        ),
        dcc.Clipboard(
            target_id='code',
            id='copy_code',
        )
    ]
)



about_me = html.Div(
    id='contenedor_about_me',
    children=[
        html.P(children=about_me_message,
            id='about_me',
        ),
        dcc.Tabs(
            id='',
            value='code',
            children=[
                dcc.Tab(value='app', label='App', children=app),
                dcc.Tab(value='code', label='Code', children=code),
            ]
        )
    ]
)

# ----------------------------------------------------------------
contenido_tabs = {
    'links': links_html,
    'featured': videos_destacados_html,
    'about_me': about_me
}

# enviar_mensaje ----------------------------------------------------
enviar_mensaje = html.Div(
    id='contenedor_enviar_mensaje',
    children=[
        html.P(
            children='Send me a message',
            id='enviar_mensaje_titulo',
        ),
        dcc.Input(
            id='email',
            placeholder='Write your email',
        ),
        html.P(
            children='Wrong email',
            id='wrong_email_warning',
        ),
        dcc.Textarea(
            id='mensaje',
            placeholder='Write your message',
        ),
        html.P(
            children='Your message is empty :(',
            id='empty_message',
        ),
        html.Button(
            children='Send',
            id = 'send',
        ),
    ]
)

app = Dash(__name__,)
server = app.server

app.title = nombre_usuario

app.layout = html.Div(
    id="all",
    children=[
        html.Video(
            id="fondo_grande",
            src=fondo_grande,
            autoPlay=True,
            loop=True,
            controls=False,
            muted=True,
        ),
        html.Div(
            id='main',
            children=[
                # Contenedor principal -------------------------------------------------------------------------------------
                html.Div(
                    id='contenedor',
                    children=[
                        # foto de perfil
                        html.Div(
                            id='contenedor_perfil',
                            children=[
                                html.Img(
                                src=avatar,
                                id="avatar",
                                ),
                                html.P(
                                    children=nombre_usuario.title(),
                                    id='nombre_usuario',
                                ),
                                html.Hr(),
                            ]
                        ),
                        # contenedor de tabs
                        html.Div(
                            id='contenedor_btn_tabs',
                            children=[
                                html.Button(children=tab.replace('_', ' ').title(), id=f'btn_{tab}', className='btn_tab')
                                for tab in contenido_tabs
                            ]
                        ),
                        *[
                            contenido_tabs[tab] for tab in contenido_tabs
                        ],
                        html.Hr(),
                        enviar_mensaje,
                        html.P(id='mensaje_enviado')
                    ]
                ),
            ]
        )
    ]
)

@callback(
    *[
        Output(component_id=f'btn_{tab}', component_property='className')
        for tab in contenido_tabs
    ],
    [
        Output(component_id=f'contenedor_{tab}', component_property='style')
        for tab in contenido_tabs
    ],
    *[
        Input(component_id=f'btn_{tab}', component_property='n_clicks')
        for tab in contenido_tabs
    ],
)
def menu_seleccion(*args):
    boton_seleccionado_clase = 'btn_tab btn_tab_seleccionado'
    boton_no_seleccionado_clase = 'btn_tab'
    
    # Al iniciar la pagina
    boton_seleccionado = ctx.triggered_id
    if not boton_seleccionado:
        resultado_clases_menu = [boton_seleccionado_clase if tab == list(contenido_tabs)[0] else boton_no_seleccionado_clase for tab in contenido_tabs]
        resultado_estilos_contenedores_tab = [{'display': 'flex'} if tab == list(contenido_tabs)[2] else {'display': 'none'} for tab in contenido_tabs]
        resultado = resultado_clases_menu + resultado_estilos_contenedores_tab
        return resultado
    
    boton_seleccionado = boton_seleccionado.replace('btn_', '')
    resultado_clases_menu = [boton_seleccionado_clase if boton_seleccionado == tab else boton_no_seleccionado_clase for tab in contenido_tabs]
    resultado_estilos_contenedores_tab = [{"display": "flex"} if tab == boton_seleccionado else {"display": "none"} for tab in contenido_tabs]
    resultado = resultado_clases_menu + resultado_estilos_contenedores_tab
    return resultado



def verificar_correo(email):
    regular = r'^(?!\.)(?!.*\.\.)[a-zA-Z0-9._%+-]+(?<!\.)@[a-zA-Z0-9-]{1,63}(\.[a-zA-Z0-9]{2,})+$'
    email_correcto = re.fullmatch(regular, email) is not None
    return email_correcto

@callback(
    Output(component_id='wrong_email_warning', component_property='style'),
    Output(component_id='email', component_property='className'),
    Output(component_id='empty_message', component_property='style'),
    Output(component_id='mensaje', component_property='className'),
    Output(component_id='contenedor_enviar_mensaje', component_property='style'),
    Output(component_id='mensaje_enviado', component_property='children'),
    Input(component_id='send', component_property='n_clicks'),
    State(component_id='email', component_property='value'),
    State(component_id='mensaje', component_property='value'),
)
def verificar_mensaje(send, email, mensaje):
    if not send or not email:
        raise PreventUpdate
    
    # Verificar que el correo ingresado es correcto
    email_correcto = verificar_correo(email)
    
    # Correo incorrecto
    if not email_correcto:
        return {'display': 'flex'}, 'wrong_email', no_update, no_update, no_update, no_update
    
    # Mensaje vacio
    if not mensaje:
        return {'display': 'none'}, '', {'display': 'flex'}, no_update, no_update, no_update
    
    # enviar email y mensaje a la base de datos
    with conectar_db() as conn:
        with conn.cursor() as cur:
            query = """
                INSERT INTO cristian_messages (email, message)
                VALUES (%s, %s)
            """
            cur.execute(query, (email, mensaje))
    
    mensaje_respuesta = f'Your message has been sent. I will respond to you as soon as possible at "{email}". Thank you for contacting me.'
    return no_update, no_update, no_update, no_update, {'display': 'none'}, mensaje_respuesta


def conectar_db():
    load_dotenv()
    
    HOST = os.getenv('PGHOST')
    DATABASE = os.getenv('PGDATABASE')
    USER = os.getenv('PGUSER')
    PASSWORD = os.getenv('PGPASSWORD')
    PORT = 5432
    
    conn = psycopg2.connect(
        host=HOST,
        database=DATABASE,
        user=USER,
        password=PASSWORD,
        port=PORT,
        sslmode='require',
    )
    
    return conn

if __name__ == '__main__':
    app.run(port=8050, debug=True)
