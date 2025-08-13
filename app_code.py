import plotly.graph_objects as go

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
    hovermode='closest', #desactivas la etiquetas adicionales
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
