from dash import Dash, html, callback

fondo_grande = "assets/fondo_grande.mp4"
fondo_pequeno = "assets/fondo_pequeno.mp4"
avatar = "assets/avatar.jpg"

nombre_usuario = "@cristian arboleda"

links=[
        {"tipo": "texto", "texto": "github", "url": "", "imagen": "assets/iconos/github.png"},
    {"tipo": "texto", "texto": "youtube", "url": "", "imagen": "assets/iconos/youtube.png"},
    {"tipo": "texto", "texto": "facebook", "url": "", "imagen": "assets/iconos/facebook.png"},
    {"tipo": "texto", "texto": "tiktok", "url": "", "imagen": "assets/iconos/tiktok.png"},
    {"tipo": "texto", "texto": "instagram", "url": "", "imagen": "assets/iconos/instagram.png"},
    {"tipo": "texto", "texto": "pagina_web", "url": "", "imagen": "assets/iconos/pagina_web.png"},
]

app = Dash(__name__)

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
                html.Video(
                    src=fondo_pequeno,
                    id='fondo_pequeno',
                    autoPlay=True,
                    loop=True,
                    controls=False,
                    muted=True,
                ) if None else None,
                
                # Contenedor principal -------------------------------------------------------------------------------------
                html.Div(
                    id='contenedor',
                    children=[
                        # foto de perfil
                        html.Img(
                            src=avatar,
                            id="avatar",
                        ),
                        html.P(
                            children=nombre_usuario.title(),
                            id='nombre_usuario',
                        ),
                        html.Hr(),
                        # links ----------------------------------------------------
                        html.Div(
                            id="contenedor_links",
                            children=[
                                html.A(
                                    className='link',
                                    href=link['url'],
                                    
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
                            ]
                        ),
                        # Video destacado -------------------------------------------------------
                        html.Iframe(
                            src='https://www.youtube.com/embed/--pxv_RCjOg?si=OsuLfLq73Ide8dAh',
                            id='video_destacado',
                        )
                    ]
                ),
            ]
        )
    ]
)

app.run_server(port=8050, debug=True)