import base64
import io
import dash
from dash import dcc, html, Input, Output, State, dash_table
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os

app = dash.Dash(__name__)
app.title = "BrainyStats - Gráficos de Control"

# 🎨 Paleta de colores profesional basada en la imagen
colors = {
    'bg_primary': '#0A2540',        # Azul marino profundo
    'bg_secondary': '#0D3A5F',      # Azul intermedio
    'bg_card': '#FFFFFF',           # Blanco puro
    'accent_gold': '#D4AF37',       # Oro elegante
    'accent_gold_light': '#F4E5C3', # Oro claro
    'green_primary': '#1B5E20',     # Verde bosque
    'green_secondary': '#2E7D32',   # Verde medio
    'text_primary': '#1A1A1A',      # Negro suave
    'text_secondary': '#546E7A',    # Gris azulado
    'text_light': '#FFFFFF',        # Blanco
    'success': '#4CAF50',           # Verde éxito
    'warning': '#FF9800',           # Naranja advertencia
    'danger': '#E53935',            # Rojo peligro
    'chart_line1': '#2196F3',       # Azul vibrante
    'chart_line2': '#FF6F00',       # Naranja vibrante
    'border': '#E0E0E0',            # Gris claro
    'shadow': 'rgba(0, 0, 0, 0.15)' # Sombra suave
}

# 📊 Constantes de gráficos de control
CONTROL_CHART_CONSTANTS = {
    2: {'A2': 1.880, 'D3': 0, 'D4': 3.267, 'd2': 1.128, 'A3': 2.659, 'B3': 0, 'B4': 3.267, 'c4': 0.7979},
    3: {'A2': 1.023, 'D3': 0, 'D4': 2.574, 'd2': 1.693, 'A3': 1.954, 'B3': 0, 'B4': 2.568, 'c4': 0.8862},
    4: {'A2': 0.729, 'D3': 0, 'D4': 2.282, 'd2': 2.059, 'A3': 1.628, 'B3': 0, 'B4': 2.266, 'c4': 0.9213},
    5: {'A2': 0.577, 'D3': 0, 'D4': 2.114, 'd2': 2.326, 'A3': 1.427, 'B3': 0, 'B4': 2.089, 'c4': 0.9400},
    6: {'A2': 0.483, 'D3': 0, 'D4': 2.004, 'd2': 2.534, 'A3': 1.287, 'B3': 0.030, 'B4': 1.970, 'c4': 0.9515},
    7: {'A2': 0.419, 'D3': 0.076, 'D4': 1.924, 'd2': 2.704, 'A3': 1.182, 'B3': 0.118, 'B4': 1.882, 'c4': 0.9594},
    8: {'A2': 0.373, 'D3': 0.136, 'D4': 1.864, 'd2': 2.847, 'A3': 1.099, 'B3': 0.185, 'B4': 1.815, 'c4': 0.9650},
    9: {'A2': 0.337, 'D3': 0.184, 'D4': 1.816, 'd2': 2.970, 'A3': 1.032, 'B3': 0.239, 'B4': 1.761, 'c4': 0.9693},
    10: {'A2': 0.308, 'D3': 0.223, 'D4': 1.777, 'd2': 3.078, 'A3': 0.975, 'B3': 0.284, 'B4': 1.716, 'c4': 0.9727},
    11: {'A2': 0.285, 'D3': 0.256, 'D4': 1.744, 'd2': 3.173, 'A3': 0.927, 'B3': 0.321, 'B4': 1.679, 'c4': 0.9754},
    12: {'A2': 0.266, 'D3': 0.283, 'D4': 1.717, 'd2': 3.258, 'A3': 0.886, 'B3': 0.354, 'B4': 1.646, 'c4': 0.9776},
    15: {'A2': 0.223, 'D3': 0.348, 'D4': 1.652, 'd2': 3.472, 'A3': 0.789, 'B3': 0.428, 'B4': 1.572, 'c4': 0.9823},
    20: {'A2': 0.180, 'D3': 0.414, 'D4': 1.586, 'd2': 3.735, 'A3': 0.680, 'B3': 0.510, 'B4': 1.490, 'c4': 0.9869},
    25: {'A2': 0.153, 'D3': 0.459, 'D4': 1.541, 'd2': 3.931, 'A3': 0.606, 'B3': 0.565, 'B4': 1.435, 'c4': 0.9896}
}

# 🖼️ Logos - Actualizado para usar carpeta assets
logo_unimag = 'assets/logo_unimag.png'
logo_ing = 'assets/logo_ing_industrial.png'
logo_brainystats = 'assets/logo_brainystats.png'

def encode_image(image_file):
    if not os.path.exists(image_file):
        return None
    encoded = base64.b64encode(open(image_file, 'rb').read()).decode()
    return f"data:image/png;base64,{encoded}"

logo_unimag_base64 = encode_image(logo_unimag)
logo_ing_base64 = encode_image(logo_ing)
logo_brainystats_base64 = encode_image(logo_brainystats)

# 🌐 Layout principal con diseño profesional
app.layout = html.Div(style={
    'background': f'linear-gradient(180deg, {colors["bg_primary"]} 0%, {colors["bg_secondary"]} 100%)',
    'minHeight': '100vh',
    'padding': '0',
    'fontFamily': "'Inter', 'Segoe UI', 'Roboto', sans-serif"
}, children=[

    # 🔹 Header profesional con onda dorada
    html.Div(style={
        'position': 'relative',
        'background': f'linear-gradient(135deg, {colors["bg_primary"]} 0%, {colors["bg_secondary"]} 100%)',
        'paddingTop': '40px',
        'paddingBottom': '60px',
        'paddingLeft': '40px',
        'paddingRight': '40px',
        'marginBottom': '0',
        'borderBottom': f'4px solid {colors["accent_gold"]}',
        'boxShadow': f'0 4px 20px {colors["shadow"]}'
    }, children=[
        # Decoración onda superior (verde)
        html.Div(style={
            'position': 'absolute',
            'top': '0',
            'left': '0',
            'right': '0',
            'height': '8px',
            'background': f'linear-gradient(90deg, {colors["green_primary"]} 0%, {colors["green_secondary"]} 100%)'
        }),
        
        html.Div(style={
            'display': 'flex',
            'justifyContent': 'space-between',
            'alignItems': 'center',
            'flexWrap': 'wrap',
            'gap': '20px',
            'maxWidth': '1400px',
            'margin': '0 auto'
        }, children=[
            # Logos izquierda
            html.Div(style={'display': 'flex', 'gap': '20px', 'alignItems': 'center'}, children=[
                html.Img(src=logo_unimag_base64, style={'height': '80px'}) if logo_unimag_base64 else html.Div(),
                html.Img(src=logo_brainystats_base64, style={'height': '80px'}) if logo_brainystats_base64 else html.Div(),
            ]),
            
            # Título central profesional
            html.Div(style={'flex': '1', 'textAlign': 'center'}, children=[
                html.H1("Gráficos de Control", style={
                    'color': colors['text_light'],
                    'fontSize': '42px',
                    'fontWeight': '700',
                    'margin': '0',
                    'letterSpacing': '1px',
                    'textTransform': 'uppercase'
                }),
                html.Div(style={
                    'height': '3px',
                    'width': '150px',
                    'background': f'linear-gradient(90deg, {colors["accent_gold"]} 0%, {colors["accent_gold_light"]} 100%)',
                    'margin': '15px auto',
                    'borderRadius': '2px'
                }),
                html.P("Control Estadístico de Procesos", style={
                    'color': colors['accent_gold_light'],
                    'fontSize': '16px',
                    'marginTop': '5px',
                    'fontWeight': '500',
                    'letterSpacing': '2px',
                    'textTransform': 'uppercase'
                }),
                html.P("Universidad del Magdalena • Ingeniería Industrial", style={
                    'color': 'rgba(255,255,255,0.7)',
                    'fontSize': '14px',
                    'marginTop': '8px',
                    'fontWeight': '400'
                }),
            ]),
            
            # Logo derecha - CORREGIDO: quitado el filtro que volvía blanco el logo
            html.Img(src=logo_ing_base64, style={'height': '80px'}) if logo_ing_base64 else html.Div(),
        ])
    ]),

    # Contenedor principal con padding
    html.Div(style={'padding': '40px', 'maxWidth': '1400px', 'margin': '0 auto'}, children=[
        
        # 🔸 Panel de configuración profesional
        html.Div(style={
            'backgroundColor': colors['bg_card'],
            'borderRadius': '12px',
            'padding': '40px',
            'marginBottom': '30px',
            'boxShadow': f'0 8px 32px {colors["shadow"]}',
            'border': f'1px solid {colors["border"]}',
        }, children=[
            html.Div(style={'borderLeft': f'5px solid {colors["accent_gold"]}', 'paddingLeft': '20px', 'marginBottom': '35px'}, children=[
                html.H3("Configuración del Análisis", style={
                    'color': colors['text_primary'],
                    'margin': '0',
                    'fontSize': '28px',
                    'fontWeight': '700'
                })
            ]),
            
            # Método de entrada
            html.Label("Método de entrada de datos", style={
                'color': colors['text_primary'],
                'fontSize': '15px',
                'fontWeight': '600',
                'marginBottom': '15px',
                'display': 'block',
                'textTransform': 'uppercase',
                'letterSpacing': '0.5px'
            }),
            dcc.RadioItems(
                id='input-method',
                options=[
                    {'label': ' Subir archivo CSV/Excel', 'value': 'upload'},
                    {'label': ' Entrada manual', 'value': 'manual'}
                ],
                value='upload',
                inline=True,
                style={'marginBottom': '30px'},
                labelStyle={
                    'color': colors['text_primary'],
                    'marginRight': '30px',
                    'fontSize': '15px',
                    'cursor': 'pointer',
                    'display': 'inline-flex',
                    'alignItems': 'center',
                    'fontWeight': '500'
                }
            ),

            # 🔸 Upload profesional
            html.Div(id='upload-div', children=[
                dcc.Upload(
                    id='upload-data',
                    children=html.Div([
                        html.Div("📁", style={'fontSize': '60px', 'marginBottom': '15px', 'opacity': '0.7'}),
                        html.Div('Arrastra tu archivo aquí', style={
                            'fontSize': '20px',
                            'fontWeight': '600',
                            'color': colors['text_primary'],
                            'marginBottom': '8px'
                        }),
                        html.Div('o haz clic para seleccionar', style={
                            'fontSize': '14px',
                            'color': colors['text_secondary'],
                            'fontWeight': '400'
                        }),
                        html.Div('CSV o XLSX', style={
                            'fontSize': '13px',
                            'color': colors['text_light'],
                            'marginTop': '20px',
                            'padding': '8px 24px',
                            'background': colors['accent_gold'],
                            'borderRadius': '6px',
                            'display': 'inline-block',
                            'fontWeight': '600',
                            'letterSpacing': '1px'
                        })
                    ], style={'textAlign': 'center'}),
                    style={
                        'width': '100%',
                        'minHeight': '220px',
                        'borderRadius': '8px',
                        'border': f'2px dashed {colors["border"]}',
                        'background': '#FAFAFA',
                        'display': 'flex',
                        'alignItems': 'center',
                        'justifyContent': 'center',
                        'cursor': 'pointer',
                        'transition': 'all 0.3s ease',
                    },
                    multiple=False
                ),
                html.Div(id='output-data-upload', style={'marginTop': '20px'})
            ]),

            # 🔸 Manual profesional
            html.Div(id='manual-div', style={'display': 'none'}, children=[
                html.Div([
                    html.Label("Número de mediciones por subgrupo", style={
                        'color': colors['text_primary'],
                        'fontSize': '15px',
                        'fontWeight': '600',
                        'marginBottom': '12px',
                        'display': 'block',
                        'textTransform': 'uppercase',
                        'letterSpacing': '0.5px'
                    }),
                    html.Div(style={'display': 'flex', 'gap': '15px', 'alignItems': 'center'}, children=[
                        dcc.Input(
                            id='num-mediciones',
                            type='number',
                            value=5,
                            min=2,
                            max=25,
                            step=1,
                            style={
                                'width': '120px',
                                'padding': '12px',
                                'borderRadius': '6px',
                                'border': f'1px solid {colors["border"]}',
                                'background': colors['bg_card'],
                                'color': colors['text_primary'],
                                'fontSize': '15px',
                                'fontWeight': '500'
                            }
                        ),
                        html.Button('Actualizar tabla', id='update-table', n_clicks=0, style={
                            'background': colors['accent_gold'],
                            'color': colors['text_light'],
                            'border': 'none',
                            'padding': '12px 28px',
                            'borderRadius': '6px',
                            'fontSize': '14px',
                            'fontWeight': '600',
                            'cursor': 'pointer',
                            'boxShadow': f'0 4px 12px {colors["shadow"]}',
                            'transition': 'transform 0.2s ease',
                            'textTransform': 'uppercase',
                            'letterSpacing': '0.5px'
                        }),
                    ]),
                ], style={'marginBottom': '25px'}),

                dash_table.DataTable(
                    id='manual-table',
                    editable=True,
                    row_deletable=True,
                    style_table={'overflowX': 'auto', 'borderRadius': '8px', 'overflow': 'hidden', 'border': f'1px solid {colors["border"]}'},
                    style_cell={
                        'textAlign': 'center',
                        'padding': '14px',
                        'backgroundColor': colors['bg_card'],
                        'color': colors['text_primary'],
                        'border': f'1px solid {colors["border"]}',
                        'fontWeight': '500',
                        'fontSize': '14px'
                    },
                    style_header={
                        'backgroundColor': colors['bg_primary'],
                        'color': colors['text_light'],
                        'fontWeight': '700',
                        'border': 'none',
                        'fontSize': '14px',
                        'textTransform': 'uppercase',
                        'letterSpacing': '0.5px'
                    },
                    style_data_conditional=[{
                        'if': {'row_index': 'odd'},
                        'backgroundColor': '#F9F9F9'
                    }]
                ),

                html.Button('Agregar subgrupo', id='add-row', n_clicks=0, style={
                    'marginTop': '18px',
                    'background': 'transparent',
                    'color': colors['text_primary'],
                    'border': f'2px solid {colors["accent_gold"]}',
                    'padding': '10px 24px',
                    'borderRadius': '6px',
                    'fontSize': '14px',
                    'fontWeight': '600',
                    'cursor': 'pointer',
                    'transition': 'all 0.3s ease',
                    'textTransform': 'uppercase',
                    'letterSpacing': '0.5px'
                })
            ]),

            # Configuración de gráficos
            html.Div(style={'marginTop': '40px', 'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '25px'}, children=[
                html.Div([
                    html.Label("Tipo de gráfico", style={
                        'color': colors['text_primary'],
                        'fontSize': '15px',
                        'fontWeight': '600',
                        'marginBottom': '12px',
                        'display': 'block',
                        'textTransform': 'uppercase',
                        'letterSpacing': '0.5px'
                    }),
                    dcc.Dropdown(
                        id='chart-type',
                        options=[
                            {'label': 'X̄-R (Promedio y Rango)', 'value': 'XR'},
                            {'label': 'X̄-S (Promedio y Desviación)', 'value': 'XS'}
                        ],
                        value='XR',
                        style={
                            'backgroundColor': colors['bg_card'],
                            'borderRadius': '6px',
                            'fontWeight': '500'
                        }
                    ),
                ]),
                
                html.Div([
                    html.Label("Nivel de significancia (α)", style={
                        'color': colors['text_primary'],
                        'fontSize': '15px',
                        'fontWeight': '600',
                        'marginBottom': '12px',
                        'display': 'block',
                        'textTransform': 'uppercase',
                        'letterSpacing': '0.5px'
                    }),
                    dcc.Input(
                        id='alpha',
                        type='number',
                        value=0.0027,
                        min=0.001,
                        max=0.1,
                        step=0.0001,
                        style={
                            'width': '100%',
                            'padding': '12px',
                            'borderRadius': '6px',
                            'border': f'1px solid {colors["border"]}',
                            'background': colors['bg_card'],
                            'color': colors['text_primary'],
                            'fontSize': '15px',
                            'fontWeight': '500'
                        }
                    ),
                ]),
            ]),

            # Botón generar profesional
            html.Button('Generar Análisis', id='generate-button', n_clicks=0, style={
                'marginTop': '35px',
                'width': '100%',
                'background': f'linear-gradient(135deg, {colors["accent_gold"]} 0%, {colors["accent_gold_light"]} 100%)',
                'color': colors['text_primary'],
                'border': 'none',
                'padding': '18px',
                'borderRadius': '8px',
                'fontSize': '16px',
                'fontWeight': '700',
                'cursor': 'pointer',
                'boxShadow': f'0 6px 20px {colors["shadow"]}',
                'transition': 'transform 0.2s ease',
                'textTransform': 'uppercase',
                'letterSpacing': '1.5px'
            }),
        ]),

        # 🔸 Área de resultados
        html.Div(id='results-area', style={'display': 'none'}, children=[
            html.Div(id='alerta-principal'),
            html.Div(id='estadisticas-proceso'),
            dcc.Graph(id='chart-xbar', config={'displayModeBar': False}),
            dcc.Graph(id='chart-rs', config={'displayModeBar': False}),
            html.Div(id='analisis-avanzado'),
            html.Div(id='recomendaciones')
        ])
    ])
])

# Callbacks (mantienen la lógica original)
@app.callback(
    Output('manual-table', 'columns'),
    Output('manual-table', 'data'),
    Input('update-table', 'n_clicks'),
    State('num-mediciones', 'value')
)
def update_manual_table(n_clicks, num_mediciones):
    if num_mediciones < 2:
        num_mediciones = 2
    if num_mediciones > 25:
        num_mediciones = 25
    
    cols = [{'name': 'Subgrupo', 'id': 'Subgrupo', 'editable': True, 'type': 'text'}] + \
           [{'name': f'x{i+1}', 'id': f'x{i+1}', 'editable': True, 'type': 'numeric'} for i in range(num_mediciones)]
    data = [{'Subgrupo': i+1, **{f'x{j+1}': None for j in range(num_mediciones)}} for i in range(10)]
    return cols, data

@app.callback(
    Output('manual-table', 'data', allow_duplicate=True),
    Input('add-row', 'n_clicks'),
    State('manual-table', 'data'),
    prevent_initial_call='initial_duplicate'
)
def add_row(n_clicks, rows):
    if n_clicks > 0 and rows:
        new_row = {'Subgrupo': len(rows)+1}
        for k in rows[0].keys():
            if k != 'Subgrupo':
                new_row[k] = None
        rows.append(new_row)
    return rows

@app.callback(
    [Output('upload-div', 'style'),
     Output('manual-div', 'style')],
    Input('input-method', 'value')
)
def toggle_input_method(method):
    if method == 'upload':
        return {'display': 'block'}, {'display': 'none'}
    else:
        return {'display': 'none'}, {'display': 'block'}

def parse_contents(contents, filename):
    if contents is None:
        return None
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename.lower():
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename.lower():
            df = pd.read_excel(io.BytesIO(decoded))
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None
    return df

def detectar_patrones_western_electric(datos, UCL, LCL, CL):
    n = len(datos)
    violaciones = []
    
    sigma_1 = (UCL - CL) / 3
    limite_2sigma_superior = CL + 2 * sigma_1
    limite_2sigma_inferior = CL - 2 * sigma_1
    limite_1sigma_superior = CL + sigma_1
    limite_1sigma_inferior = CL - sigma_1
    
    for i in range(n):
        if datos[i] > UCL or datos[i] < LCL:
            violaciones.append(f"Regla 1: Punto {i+1} fuera de límites (3σ)")
    
    for i in range(n-2):
        ventana = datos[i:i+3]
        fuera_2sigma = sum(1 for x in ventana if x > limite_2sigma_superior or x < limite_2sigma_inferior)
        if fuera_2sigma >= 2:
            violaciones.append(f"Regla 2: Puntos {i+1}-{i+3} - 2/3 fuera de 2σ")
    
    for i in range(n-4):
        ventana = datos[i:i+5]
        fuera_1sigma = sum(1 for x in ventana if x > limite_1sigma_superior or x < limite_1sigma_inferior)
        if fuera_1sigma >= 4:
            violaciones.append(f"Regla 3: Puntos {i+1}-{i+5} - 4/5 fuera de 1σ")
    
    for i in range(n-7):
        ventana = datos[i:i+8]
        if all(x > CL for x in ventana) or all(x < CL for x in ventana):
            violaciones.append(f"Regla 4: Puntos {i+1}-{i+8} - 8 consecutivos en un lado")
    
    for i in range(n-5):
        ventana = datos[i:i+6]
        if all(ventana[j] < ventana[j+1] for j in range(5)):
            violaciones.append(f"Regla 5: Puntos {i+1}-{i+6} - Tendencia ascendente")
        elif all(ventana[j] > ventana[j+1] for j in range(5)):
            violaciones.append(f"Regla 5: Puntos {i+1}-{i+6} - Tendencia descendente")
    
    return violaciones

def analizar_capacidad(datos, UCL, LCL):
    sigma_estimada = (UCL - LCL) / 6
    if sigma_estimada == 0:
        return None
    
    rango_especificacion = UCL - LCL
    Cp = rango_especificacion / (6 * sigma_estimada)
    
    return {
        'sigma': sigma_estimada,
        'Cp': Cp,
        'interpretacion': 'Excelente' if Cp >= 2.0 else 'Adecuado' if Cp >= 1.33 else 'Marginal' if Cp >= 1.0 else 'Inadecuado'
    }

@app.callback(
    [Output('chart-xbar', 'figure'),
     Output('chart-rs', 'figure'),
     Output('alerta-principal', 'children'),
     Output('alerta-principal', 'style'),
     Output('estadisticas-proceso', 'children'),
     Output('analisis-avanzado', 'children'),
     Output('recomendaciones', 'children'),
     Output('results-area', 'style')],
    Input('generate-button', 'n_clicks'),
    State('upload-data', 'contents'),
    State('upload-data', 'filename'),
    State('manual-table', 'data'),
    State('input-method', 'value'),
    State('chart-type', 'value'),
    State('alpha', 'value')
)
def update_graph(n_clicks, contents, filename, manual_data, method, chart_type, alpha):
    empty_results = (go.Figure(), go.Figure(), "", {}, "", "", "", {'display': 'none'})
    
    if n_clicks == 0:
        return empty_results
    
    if method == 'upload':
        df = parse_contents(contents, filename)
        if df is None:
            return empty_results
    else:
        df = pd.DataFrame(manual_data)
        df = df.drop(columns=['Subgrupo'], errors='ignore').dropna(how='all')

    if df is None or df.empty:
        return empty_results

    try:
        subgroups = df.to_numpy(dtype=float)
        subgroups = subgroups[~np.isnan(subgroups).all(axis=1)]
        if len(subgroups) == 0:
            return empty_results
    except:
        return empty_results

    means = np.nanmean(subgroups, axis=1)
    ranges = np.ptp(subgroups, axis=1)
    stds = np.nanstd(subgroups, axis=1, ddof=1)
    n = subgroups.shape[1]

    if n not in CONTROL_CHART_CONSTANTS:
        n_keys = sorted(CONTROL_CHART_CONSTANTS.keys())
        n_use = min(n_keys, key=lambda x: abs(x - n))
    else:
        n_use = n
    
    constants = CONTROL_CHART_CONSTANTS[n_use]
    A2, A3 = constants['A2'], constants['A3']
    D3, D4 = constants['D3'], constants['D4']
    B3, B4 = constants['B3'], constants['B4']
    d2, c4 = constants['d2'], constants['c4']

    CLx = np.mean(means)
    CLr = np.mean(ranges)
    CLs = np.mean(stds)
    
    if chart_type == 'XR':
        UCLx = CLx + A2 * CLr
        LCLx = CLx - A2 * CLr
        UCLr = D4 * CLr
        LCLr = D3 * CLr
        sigma_estimada = CLr / d2
    else:
        UCLx = CLx + A3 * CLs
        LCLx = CLx - A3 * CLs
        UCLs = B4 * CLs
        LCLs = B3 * CLs
        sigma_estimada = CLs / c4

    # Gráfico X̄ profesional
    num_subgrupos = np.arange(1, len(means) + 1)
    
    fig_xbar = go.Figure()
    
    fig_xbar.add_trace(go.Scatter(
        x=num_subgrupos, y=means,
        mode='lines+markers',
        name='X̄',
        line=dict(color=colors['chart_line1'], width=3),
        marker=dict(size=10, color=colors['chart_line1'], line=dict(color='white', width=2)),
        hovertemplate='<b>Subgrupo %{x}</b><br>X̄ = %{y:.4f}<extra></extra>'
    ))
    
    fig_xbar.add_hline(y=UCLx, line_dash='dash', line_color=colors['danger'], line_width=2.5,
                       annotation_text=f"UCL {UCLx:.4f}", annotation_position="right",
                       annotation=dict(font=dict(size=11, color=colors['danger'])))
    fig_xbar.add_hline(y=LCLx, line_dash='dash', line_color=colors['danger'], line_width=2.5,
                       annotation_text=f"LCL {LCLx:.4f}", annotation_position="right",
                       annotation=dict(font=dict(size=11, color=colors['danger'])))
    fig_xbar.add_hline(y=CLx, line_dash='solid', line_color=colors['success'], line_width=3,
                       annotation_text=f"CL {CLx:.4f}", annotation_position="right",
                       annotation=dict(font=dict(size=11, color=colors['success'])))
    
    # Zonas sigma profesionales
    sigma_1 = (UCLx - CLx) / 3
    fig_xbar.add_hrect(y0=CLx + sigma_1, y1=CLx + 2*sigma_1, fillcolor=colors['warning'], opacity=0.1, line_width=0)
    fig_xbar.add_hrect(y0=CLx - sigma_1, y1=CLx - 2*sigma_1, fillcolor=colors['warning'], opacity=0.1, line_width=0)
    fig_xbar.add_hrect(y0=CLx + 2*sigma_1, y1=UCLx, fillcolor=colors['danger'], opacity=0.08, line_width=0)
    fig_xbar.add_hrect(y0=LCLx, y1=CLx - 2*sigma_1, fillcolor=colors['danger'], opacity=0.08, line_width=0)
    
    fuera_control_x = np.where((means > UCLx) | (means < LCLx))[0]
    if len(fuera_control_x) > 0:
        fig_xbar.add_trace(go.Scatter(
            x=num_subgrupos[fuera_control_x], y=means[fuera_control_x],
            mode='markers', name='Fuera de control',
            marker=dict(size=14, color=colors['danger'], symbol='x', line=dict(width=3, color='white')),
            hovertemplate='⚠️ Fuera de control<br>Subgrupo %{x}<br>X̄ = %{y:.4f}<extra></extra>'
        ))
    
    fig_xbar.update_layout(
        title={'text': f"<b>Gráfico X̄ - Promedios</b>", 'x': 0.5, 'xanchor': 'center', 'font': {'size': 22, 'color': colors['text_primary']}},
        xaxis_title="Número de Subgrupo",
        yaxis_title="Media (X̄)",
        template="plotly_white",
        paper_bgcolor='white',
        plot_bgcolor='#FAFAFA',
        font=dict(size=13, color=colors['text_primary'], family="Inter"),
        hovermode='x unified',
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=70, r=70, t=90, b=70)
    )

    # Gráfico R/S profesional
    fig_rs = go.Figure()
    
    if chart_type == 'XR':
        fig_rs.add_trace(go.Scatter(
            x=num_subgrupos, y=ranges,
            mode='lines+markers', name='R',
            line=dict(color=colors['chart_line2'], width=3),
            marker=dict(size=10, color=colors['chart_line2'], line=dict(color='white', width=2)),
            hovertemplate='<b>Subgrupo %{x}</b><br>R = %{y:.4f}<extra></extra>'
        ))
        
        fig_rs.add_hline(y=UCLr, line_dash='dash', line_color=colors['danger'], line_width=2.5,
                         annotation_text=f"UCL {UCLr:.4f}", annotation_position="right",
                         annotation=dict(font=dict(size=11, color=colors['danger'])))
        fig_rs.add_hline(y=LCLr, line_dash='dash', line_color=colors['danger'], line_width=2.5,
                         annotation_text=f"LCL {LCLr:.4f}", annotation_position="right",
                         annotation=dict(font=dict(size=11, color=colors['danger'])))
        fig_rs.add_hline(y=CLr, line_dash='solid', line_color=colors['success'], line_width=3,
                         annotation_text=f"CL {CLr:.4f}", annotation_position="right",
                         annotation=dict(font=dict(size=11, color=colors['success'])))
        
        fuera_control_r = np.where((ranges > UCLr) | (ranges < LCLr))[0]
        if len(fuera_control_r) > 0:
            fig_rs.add_trace(go.Scatter(
                x=num_subgrupos[fuera_control_r], y=ranges[fuera_control_r],
                mode='markers', name='Fuera de control',
                marker=dict(size=14, color=colors['danger'], symbol='x', line=dict(width=3, color='white')),
                hovertemplate='⚠️ Fuera de control<br>Subgrupo %{x}<br>R = %{y:.4f}<extra></extra>'
            ))
        
        fig_rs.update_layout(
            title={'text': "<b>Gráfico R - Rangos</b>", 'x': 0.5, 'xanchor': 'center', 'font': {'size': 22, 'color': colors['text_primary']}},
            xaxis_title="Número de Subgrupo", yaxis_title="Rango (R)"
        )
    else:
        fig_rs.add_trace(go.Scatter(
            x=num_subgrupos, y=stds,
            mode='lines+markers', name='S',
            line=dict(color=colors['chart_line2'], width=3),
            marker=dict(size=10, color=colors['chart_line2'], line=dict(color='white', width=2)),
            hovertemplate='<b>Subgrupo %{x}</b><br>S = %{y:.4f}<extra></extra>'
        ))
        
        fig_rs.add_hline(y=UCLs, line_dash='dash', line_color=colors['danger'], line_width=2.5,
                         annotation_text=f"UCL {UCLs:.4f}", annotation_position="right",
                         annotation=dict(font=dict(size=11, color=colors['danger'])))
        fig_rs.add_hline(y=LCLs, line_dash='dash', line_color=colors['danger'], line_width=2.5,
                         annotation_text=f"LCL {LCLs:.4f}", annotation_position="right",
                         annotation=dict(font=dict(size=11, color=colors['danger'])))
        fig_rs.add_hline(y=CLs, line_dash='solid', line_color=colors['success'], line_width=3,
                         annotation_text=f"CL {CLs:.4f}", annotation_position="right",
                         annotation=dict(font=dict(size=11, color=colors['success'])))
        
        fuera_control_s = np.where((stds > UCLs) | (stds < LCLs))[0]
        if len(fuera_control_s) > 0:
            fig_rs.add_trace(go.Scatter(
                x=num_subgrupos[fuera_control_s], y=stds[fuera_control_s],
                mode='markers', name='Fuera de control',
                marker=dict(size=14, color=colors['danger'], symbol='x', line=dict(width=3, color='white')),
                hovertemplate='⚠️ Fuera de control<br>Subgrupo %{x}<br>S = %{y:.4f}<extra></extra>'
            ))
        
        fig_rs.update_layout(
            title={'text': "<b>Gráfico S - Desviación Estándar</b>", 'x': 0.5, 'xanchor': 'center', 'font': {'size': 22, 'color': colors['text_primary']}},
            xaxis_title="Número de Subgrupo", yaxis_title="Desviación (S)"
        )
    
    fig_rs.update_layout(
        template="plotly_white",
        paper_bgcolor='white',
        plot_bgcolor='#FAFAFA',
        font=dict(size=13, color=colors['text_primary'], family="Inter"),
        hovermode='x unified',
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=70, r=70, t=90, b=70)
    )

    # Análisis
    num_fuera_control = len(fuera_control_x)
    violaciones_patrones = detectar_patrones_western_electric(means, UCLx, LCLx, CLx)
    
    # Alerta principal profesional
    if num_fuera_control > 0 or len(violaciones_patrones) > 0:
        alerta_texto = html.Div([
            html.Div(style={'display': 'flex', 'alignItems': 'center', 'gap': '20px'}, children=[
                html.Div("⚠️", style={'fontSize': '60px'}),
                html.Div([
                    html.Div("Proceso Fuera de Control", style={'fontSize': '28px', 'fontWeight': '700', 'marginBottom': '8px'}),
                    html.Div(f"{num_fuera_control} puntos detectados fuera de los límites de control", 
                            style={'fontSize': '16px', 'fontWeight': '500', 'opacity': '0.9'})
                ])
            ])
        ])
        alerta_style = {
            'padding': '30px 40px',
            'borderRadius': '8px',
            'marginBottom': '30px',
            'backgroundColor': '#FFEBEE',
            'border': f'1px solid {colors["danger"]}',
            'borderLeft': f'5px solid {colors["danger"]}',
            'boxShadow': f'0 4px 12px {colors["shadow"]}',
            'color': colors['text_primary']
        }
    else:
        alerta_texto = html.Div([
            html.Div(style={'display': 'flex', 'alignItems': 'center', 'gap': '20px'}, children=[
                html.Div("✓", style={'fontSize': '60px', 'color': colors['success'], 'fontWeight': 'bold'}),
                html.Div([
                    html.Div("Proceso Bajo Control", style={'fontSize': '28px', 'fontWeight': '700', 'marginBottom': '8px'}),
                    html.Div("Todos los puntos dentro de los límites de control establecidos", 
                            style={'fontSize': '16px', 'fontWeight': '500', 'opacity': '0.9'})
                ])
            ])
        ])
        alerta_style = {
            'padding': '30px 40px',
            'borderRadius': '8px',
            'marginBottom': '30px',
            'backgroundColor': '#E8F5E9',
            'border': f'1px solid {colors["success"]}',
            'borderLeft': f'5px solid {colors["success"]}',
            'boxShadow': f'0 4px 12px {colors["shadow"]}',
            'color': colors['text_primary']
        }

    # Estadísticas profesionales
    capacidad = analizar_capacidad(means, UCLx, LCLx)
    
    estadisticas_html = html.Div(style={
        'display': 'grid',
        'gridTemplateColumns': 'repeat(auto-fit, minmax(320px, 1fr))',
        'gap': '25px',
        'marginBottom': '30px'
    }, children=[
        # Card 1: X̄
        html.Div(style={
            'backgroundColor': colors['bg_card'],
            'border': f'1px solid {colors["border"]}',
            'borderTop': f'4px solid {colors["accent_gold"]}',
            'borderRadius': '8px',
            'padding': '30px',
            'boxShadow': f'0 4px 12px {colors["shadow"]}'
        }, children=[
            html.Div(style={'marginBottom': '25px'}, children=[
                html.Div("GRÁFICO X̄", style={'fontSize': '13px', 'fontWeight': '700', 'color': colors['text_secondary'], 'letterSpacing': '1px', 'marginBottom': '10px'}),
                html.Div("Promedios del Proceso", style={'fontSize': '20px', 'fontWeight': '700', 'color': colors['text_primary']})
            ]),
            html.Div([
                html.Div([
                    html.Div("Línea Central", style={'fontSize': '12px', 'color': colors['text_secondary'], 'fontWeight': '600', 'marginBottom': '5px'}),
                    html.Div(f"{CLx:.4f}", style={'fontSize': '32px', 'fontWeight': '700', 'color': colors['text_primary']})
                ], style={'marginBottom': '20px', 'padding': '15px', 'backgroundColor': '#FAFAFA', 'borderRadius': '6px'}),
                html.Div(style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '15px'}, children=[
                    html.Div([
                        html.Div("UCL", style={'fontSize': '11px', 'color': colors['text_secondary'], 'fontWeight': '600', 'marginBottom': '5px'}),
                        html.Div(f"{UCLx:.4f}", style={'fontSize': '18px', 'fontWeight': '700', 'color': colors['danger']})
                    ]),
                    html.Div([
                        html.Div("LCL", style={'fontSize': '11px', 'color': colors['text_secondary'], 'fontWeight': '600', 'marginBottom': '5px'}),
                        html.Div(f"{LCLx:.4f}", style={'fontSize': '18px', 'fontWeight': '700', 'color': colors['danger']})
                    ])
                ])
            ])
        ]),
        
        # Card 2: R/S
        html.Div(style={
            'backgroundColor': colors['bg_card'],
            'border': f'1px solid {colors["border"]}',
            'borderTop': f'4px solid {colors["chart_line2"]}',
            'borderRadius': '8px',
            'padding': '30px',
            'boxShadow': f'0 4px 12px {colors["shadow"]}'
        }, children=[
            html.Div(style={'marginBottom': '25px'}, children=[
                html.Div(f"GRÁFICO {'R' if chart_type == 'XR' else 'S'}", style={'fontSize': '13px', 'fontWeight': '700', 'color': colors['text_secondary'], 'letterSpacing': '1px', 'marginBottom': '10px'}),
                html.Div(f"{'Rangos' if chart_type == 'XR' else 'Desviación Estándar'}", style={'fontSize': '20px', 'fontWeight': '700', 'color': colors['text_primary']})
            ]),
            html.Div([
                html.Div([
                    html.Div("Línea Central", style={'fontSize': '12px', 'color': colors['text_secondary'], 'fontWeight': '600', 'marginBottom': '5px'}),
                    html.Div(f"{CLr if chart_type == 'XR' else CLs:.4f}", 
                            style={'fontSize': '32px', 'fontWeight': '700', 'color': colors['text_primary']})
                ], style={'marginBottom': '20px', 'padding': '15px', 'backgroundColor': '#FAFAFA', 'borderRadius': '6px'}),
                html.Div(style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '15px'}, children=[
                    html.Div([
                        html.Div("UCL", style={'fontSize': '11px', 'color': colors['text_secondary'], 'fontWeight': '600', 'marginBottom': '5px'}),
                        html.Div(f"{UCLr if chart_type == 'XR' else UCLs:.4f}", 
                                style={'fontSize': '18px', 'fontWeight': '700', 'color': colors['danger']})
                    ]),
                    html.Div([
                        html.Div("Tamaño (n)", style={'fontSize': '11px', 'color': colors['text_secondary'], 'fontWeight': '600', 'marginBottom': '5px'}),
                        html.Div(f"{n}", style={'fontSize': '18px', 'fontWeight': '700', 'color': colors['text_primary']})
                    ])
                ])
            ])
        ]),
        
        # Card 3: Capacidad
        html.Div(style={
            'backgroundColor': colors['bg_card'],
            'border': f'1px solid {colors["border"]}',
            'borderTop': f'4px solid {colors["success"]}',
            'borderRadius': '8px',
            'padding': '30px',
            'boxShadow': f'0 4px 12px {colors["shadow"]}'
        }, children=[
            html.Div(style={'marginBottom': '25px'}, children=[
                html.Div("CAPACIDAD", style={'fontSize': '13px', 'fontWeight': '700', 'color': colors['text_secondary'], 'letterSpacing': '1px', 'marginBottom': '10px'}),
                html.Div("Índice del Proceso", style={'fontSize': '20px', 'fontWeight': '700', 'color': colors['text_primary']})
            ]),
            html.Div([
                html.Div([
                    html.Div("Índice Cp", style={'fontSize': '12px', 'color': colors['text_secondary'], 'fontWeight': '600', 'marginBottom': '5px'}),
                    html.Div(f"{capacidad['Cp']:.3f}" if capacidad else "N/A", 
                            style={'fontSize': '38px', 'fontWeight': '700', 'color': colors['text_primary']})
                ], style={'marginBottom': '20px', 'padding': '15px', 'backgroundColor': '#FAFAFA', 'borderRadius': '6px'}),
                html.Div([
                    html.Div("σ estimada", style={'fontSize': '11px', 'color': colors['text_secondary'], 'fontWeight': '600', 'marginBottom': '5px'}),
                    html.Div(f"{sigma_estimada:.4f}", style={'fontSize': '16px', 'fontWeight': '700', 'color': colors['text_primary'], 'marginBottom': '15px'})
                ]),
                html.Div(
                    capacidad['interpretacion'] if capacidad else "N/A",
                    style={
                        'padding': '10px 20px',
                        'background': colors['success'] if capacidad and capacidad['Cp'] >= 1.33 else colors['danger'],
                        'borderRadius': '6px',
                        'fontSize': '14px',
                        'fontWeight': '700',
                        'textAlign': 'center',
                        'color': 'white',
                        'textTransform': 'uppercase',
                        'letterSpacing': '0.5px'
                    }
                )
            ])
        ])
    ])

    # Análisis avanzado profesional
    analisis_html = html.Div(style={
        'backgroundColor': colors['bg_card'],
        'borderRadius': '8px',
        'padding': '35px',
        'marginBottom': '30px',
        'marginTop': '30px',
        'border': f'1px solid {colors["border"]}',
        'boxShadow': f'0 4px 12px {colors["shadow"]}'
    }, children=[
        html.Div(style={'borderLeft': f'5px solid {colors["accent_gold"]}', 'paddingLeft': '20px', 'marginBottom': '30px'}, children=[
            html.H4("Análisis de Patrones Western Electric", style={
                'color': colors['text_primary'],
                'margin': '0',
                'fontSize': '24px',
                'fontWeight': '700'
            })
        ]),
        
        html.Div([
            html.Div(style={'marginBottom': '30px'}, children=[
                html.Div("PUNTOS FUERA DE CONTROL", style={'fontSize': '12px', 'fontWeight': '700', 'color': colors['text_secondary'], 'letterSpacing': '1px', 'marginBottom': '12px'}),
                html.Div(style={
                    'display': 'inline-flex',
                    'alignItems': 'center',
                    'gap': '15px',
                    'padding': '15px 25px',
                    'background': '#FFEBEE' if num_fuera_control > 0 else '#E8F5E9',
                    'borderRadius': '6px',
                    'border': f'1px solid {colors["danger"] if num_fuera_control > 0 else colors["success"]}'
                }, children=[
                    html.Span(f"{num_fuera_control}", style={'fontSize': '32px', 'fontWeight': '700', 'color': colors['danger'] if num_fuera_control > 0 else colors['success']}),
                    html.Span("detectados", style={'fontSize': '14px', 'fontWeight': '600', 'color': colors['text_secondary']})
                ]),
            ]),
            
            html.Div([
                html.Ul([
                    html.Li(f"Subgrupo {i+1}: X̄ = {means[i]:.4f}", 
                           style={'color': colors['text_primary'], 'marginBottom': '8px', 'fontSize': '14px', 'fontWeight': '500'}) 
                    for i in fuera_control_x
                ], style={'paddingLeft': '20px', 'margin': '0'}) if num_fuera_control > 0 
                else html.P("Todos los puntos dentro de los límites de control", 
                           style={'color': colors['success'], 'fontWeight': '600', 'fontSize': '15px', 'margin': '0'})
            ], style={'padding': '20px', 'backgroundColor': '#FAFAFA', 'borderRadius': '6px', 'marginBottom': '30px'})
        ]),
        
        html.Div([
            html.Div("PATRONES ANORMALES", style={'fontSize': '12px', 'fontWeight': '700', 'color': colors['text_secondary'], 'letterSpacing': '1px', 'marginBottom': '12px'}),
            html.Div(style={
                'display': 'inline-flex',
                'alignItems': 'center',
                'gap': '15px',
                'padding': '15px 25px',
                'background': '#FFF3E0' if len(violaciones_patrones) > 0 else '#E8F5E9',
                'borderRadius': '6px',
                'marginBottom': '20px',
                'border': f'1px solid {colors["warning"] if len(violaciones_patrones) > 0 else colors["success"]}'
            }, children=[
                html.Span(f"{len(violaciones_patrones)}", style={'fontSize': '32px', 'fontWeight': '700', 'color': colors['warning'] if len(violaciones_patrones) > 0 else colors['success']}),
                html.Span("patrones", style={'fontSize': '14px', 'fontWeight': '600', 'color': colors['text_secondary']})
            ]),
            
            html.Div([
                html.Ul([
                    html.Li(v, style={'color': colors['text_primary'], 'marginBottom': '8px', 'fontSize': '14px', 'fontWeight': '500'}) 
                    for v in violaciones_patrones
                ], style={'paddingLeft': '20px', 'margin': '0'}) if len(violaciones_patrones) > 0 
                else html.P("No se detectaron patrones anormales en los datos", 
                           style={'color': colors['success'], 'fontWeight': '600', 'fontSize': '15px', 'margin': '0'})
            ], style={'padding': '20px', 'backgroundColor': '#FAFAFA', 'borderRadius': '6px'})
        ])
    ])

    # Recomendaciones profesionales
    recomendaciones_lista = []
    
    if num_fuera_control > 0:
        recomendaciones_lista.extend([
            "Investigar causas especiales en los puntos fuera de control identificados",
            "Revisar y verificar la calibración de los equipos de medición",
            "Verificar si hubo cambios en el operador o en el método de trabajo",
            "Inspeccionar la calidad y consistencia de la materia prima",
            "Revisar las condiciones ambientales del proceso"
        ])
    
    if len(violaciones_patrones) > 0:
        recomendaciones_lista.append("Analizar los patrones detectados para identificar causas asignables")
        if any("Regla 5" in v for v in violaciones_patrones):
            recomendaciones_lista.append("Tendencia detectada: verificar desgaste de herramientas o deriva del proceso")
        if any("Regla 4" in v for v in violaciones_patrones):
            recomendaciones_lista.append("Sesgo detectado: verificar ajustes y centrado del proceso")
    
    if capacidad and capacidad['Cp'] < 1.33:
        recomendaciones_lista.extend([
            "La capacidad del proceso es inadecuada: implementar acciones para reducir la variación",
            "Considerar metodologías de mejora continua (Six Sigma, Lean Manufacturing)"
        ])
    
    if len(recomendaciones_lista) == 0:
        recomendaciones_lista.append("El proceso se encuentra estable y capaz. Mantener el monitoreo continuo y las condiciones actuales")
    
    recomendaciones_html = html.Div(style={
        'backgroundColor': colors['bg_card'],
        'borderRadius': '8px',
        'padding': '35px',
        'border': f'1px solid {colors["border"]}',
        'borderLeft': f'5px solid {colors["accent_gold"]}',
        'boxShadow': f'0 4px 12px {colors["shadow"]}'
    }, children=[
        html.Div(style={'marginBottom': '25px'}, children=[
            html.H4("Recomendaciones", style={
                'color': colors['text_primary'],
                'margin': '0',
                'fontSize': '24px',
                'fontWeight': '700'
            })
        ]),
        html.Ul([
            html.Li(rec, style={
                'color': colors['text_primary'],
                'marginBottom': '12px',
                'fontSize': '15px',
                'fontWeight': '500',
                'lineHeight': '1.6'
            }) 
            for rec in recomendaciones_lista
        ], style={'paddingLeft': '25px', 'margin': '0'})
    ])

    return (fig_xbar, fig_rs, alerta_texto, alerta_style, estadisticas_html, 
            analisis_html, recomendaciones_html, {'display': 'block'})


if __name__ == '__main__':
    app.run(debug=True)