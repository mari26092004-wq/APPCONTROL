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

# 🎨 Paleta de colores profesional
colors = {
    'bg_primary': '#0A2540',
    'bg_secondary': '#0D3A5F',
    'bg_card': '#FFFFFF',
    'accent_gold': '#D4AF37',
    'accent_gold_light': '#F4E5C3',
    'green_primary': '#1B5E20',
    'green_secondary': '#2E7D32',
    'text_primary': '#1A1A1A',
    'text_secondary': '#546E7A',
    'text_light': '#FFFFFF',
    'success': '#4CAF50',
    'warning': '#FF9800',
    'danger': '#E53935',
    'chart_line1': '#2196F3',
    'chart_line2': '#FF6F00',
    'border': '#E0E0E0',
    'shadow': 'rgba(0, 0, 0, 0.15)'
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

# 🖼️ Logos
logo_unimag = 'logo_unimag.png'
logo_ing = 'logo_ing_industrial.png'
logo_brainystats = 'logo_brainystats.png'

def encode_image(image_file):
    if not os.path.exists(image_file):
        return None
    encoded = base64.b64encode(open(image_file, 'rb').read()).decode()
    return f"data:image/png;base64,{encoded}"

logo_unimag_base64 = encode_image(logo_unimag)
logo_ing_base64 = encode_image(logo_ing)
logo_brainystats_base64 = encode_image(logo_brainystats)

# 🌐 Layout principal
app.layout = html.Div(style={
    'background': f'linear-gradient(180deg, {colors["bg_primary"]} 0%, {colors["bg_secondary"]} 100%)',
    'minHeight': '100vh',
    'padding': '0',
    'fontFamily': "'Inter', 'Segoe UI', 'Roboto', sans-serif"
}, children=[

    # Header
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
            html.Div(style={'display': 'flex', 'gap': '20px', 'alignItems': 'center'}, children=[
                html.Img(src=logo_unimag_base64, style={'height': '80px'}) if logo_unimag_base64 else html.Div(),
                html.Img(src=logo_brainystats_base64, style={'height': '80px'}) if logo_brainystats_base64 else html.Div(),
            ]),
            
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
            
            html.Img(src=logo_ing_base64, style={'height': '80px', 'filter': 'brightness(0) invert(1)'}) if logo_ing_base64 else html.Div(),
        ])
    ]),

    # Contenedor principal
    html.Div(style={'padding': '40px', 'maxWidth': '1400px', 'margin': '0 auto'}, children=[
        
        # Panel de configuración
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

            # Upload
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
                
                # 📝 Instrucciones de formato
                html.Div(style={
                    'marginTop': '20px',
                    'padding': '20px',
                    'backgroundColor': '#F0F7FF',
                    'borderRadius': '8px',
                    'border': '1px solid #BBDEFB'
                }, children=[
                    html.Div("📋 Formato del archivo:", style={
                        'fontWeight': '700',
                        'fontSize': '14px',
                        'color': colors['text_primary'],
                        'marginBottom': '12px',
                        'textTransform': 'uppercase',
                        'letterSpacing': '0.5px'
                    }),
                    html.Ul([
                        html.Li("Cada COLUMNA representa una medición (x1, x2, x3, ...)", style={'marginBottom': '8px', 'fontSize': '13px'}),
                        html.Li("Cada FILA representa un subgrupo/muestra", style={'marginBottom': '8px', 'fontSize': '13px'}),
                        html.Li("NO incluir encabezados ni nombres de columnas", style={'marginBottom': '8px', 'fontSize': '13px', 'fontWeight': '600'}),
                        html.Li("Solo valores numéricos", style={'fontSize': '13px'}),
                    ], style={'paddingLeft': '20px', 'margin': '0', 'color': colors['text_primary']}),
                    html.Div(style={'marginTop': '15px', 'padding': '12px', 'backgroundColor': 'white', 'borderRadius': '6px', 'fontFamily': 'monospace', 'fontSize': '12px'}, children=[
                        html.Div("Ejemplo CSV:", style={'fontWeight': '700', 'marginBottom': '8px', 'color': colors['text_primary']}),
                        html.Pre("10.2,10.1,10.3,10.0,10.2\n10.3,10.2,10.4,10.1,10.3\n10.1,10.0,10.2,10.1,10.1", 
                                style={'margin': '0', 'color': '#1565C0'})
                    ])
                ]),
                
                html.Div(id='output-data-upload', style={'marginTop': '20px'})
            ]),

            # Manual
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

            # Límites de Especificación (USL/LSL)
            html.Div(style={'marginTop': '30px', 'padding': '25px', 'backgroundColor': '#F5F5F5', 'borderRadius': '8px', 'border': f'1px solid {colors["border"]}'}, children=[
                html.Label("Límites de Especificación (Opcionales)", style={
                    'color': colors['text_primary'],
                    'fontSize': '15px',
                    'fontWeight': '600',
                    'marginBottom': '15px',
                    'display': 'block',
                    'textTransform': 'uppercase',
                    'letterSpacing': '0.5px'
                }),
                html.P("Para calcular Cpk y Ppk, ingresa los límites de especificación de tu proceso", style={
                    'fontSize': '13px',
                    'color': colors['text_secondary'],
                    'marginBottom': '15px',
                    'fontWeight': '500'
                }),
                html.Div(style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '20px'}, children=[
                    html.Div([
                        html.Label("USL (Upper Specification Limit)", style={
                            'fontSize': '13px',
                            'fontWeight': '600',
                            'color': colors['text_primary'],
                            'marginBottom': '8px',
                            'display': 'block'
                        }),
                        dcc.Input(
                            id='usl-input',
                            type='number',
                            placeholder='Ej: 105.5',
                            style={
                                'width': '100%',
                                'padding': '12px',
                                'borderRadius': '6px',
                                'border': f'1px solid {colors["border"]}',
                                'background': colors['bg_card'],
                                'color': colors['text_primary'],
                                'fontSize': '14px',
                                'fontWeight': '500'
                            }
                        )
                    ]),
                    html.Div([
                        html.Label("LSL (Lower Specification Limit)", style={
                            'fontSize': '13px',
                            'fontWeight': '600',
                            'color': colors['text_primary'],
                            'marginBottom': '8px',
                            'display': 'block'
                        }),
                        dcc.Input(
                            id='lsl-input',
                            type='number',
                            placeholder='Ej: 94.5',
                            style={
                                'width': '100%',
                                'padding': '12px',
                                'borderRadius': '6px',
                                'border': f'1px solid {colors["border"]}',
                                'background': colors['bg_card'],
                                'color': colors['text_primary'],
                                'fontSize': '14px',
                                'fontWeight': '500'
                            }
                        )
                    ])
                ])
            ]),

            # Tipo de gráfico
            html.Div(style={'marginTop': '30px'}, children=[
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

            # Botón generar
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

        # Área de resultados
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

# Callbacks
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
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), header=None)
        elif 'xls' in filename.lower():
            df = pd.read_excel(io.BytesIO(decoded), header=None)
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None
    return df

def detectar_patrones_western_electric(datos, UCL, LCL, CL):
    """Detecta patrones Western Electric (Reglas 1-5)"""
    n = len(datos)
    violaciones = []
    violaciones_detectadas = set()
    
    sigma_1 = (UCL - CL) / 3
    limite_2sigma_superior = CL + 2 * sigma_1
    limite_2sigma_inferior = CL - 2 * sigma_1
    limite_1sigma_superior = CL + sigma_1
    limite_1sigma_inferior = CL - sigma_1
    
    # Regla 1: Un punto fuera de 3σ
    for i in range(n):
        if datos[i] > UCL or datos[i] < LCL:
            key = f"R1-{i}"
            if key not in violaciones_detectadas:
                violaciones.append(f"Regla 1: Punto {i+1} fuera de límites (3σ) - Valor: {datos[i]:.4f}")
                violaciones_detectadas.add(key)
    
    # Regla 2: 2 de 3 puntos fuera de 2σ
    for i in range(n-2):
        ventana = datos[i:i+3]
        fuera_2sigma_sup = sum(1 for x in ventana if x > limite_2sigma_superior)
        fuera_2sigma_inf = sum(1 for x in ventana if x < limite_2sigma_inferior)
        
        if fuera_2sigma_sup >= 2:
            key = f"R2-{i}-sup"
            if key not in violaciones_detectadas:
                violaciones.append(f"Regla 2: Puntos {i+1}-{i+3} - 2/3 fuera de 2σ (superior)")
                violaciones_detectadas.add(key)
        
        if fuera_2sigma_inf >= 2:
            key = f"R2-{i}-inf"
            if key not in violaciones_detectadas:
                violaciones.append(f"Regla 2: Puntos {i+1}-{i+3} - 2/3 fuera de 2σ (inferior)")
                violaciones_detectadas.add(key)
    
    # Regla 3: 4 de 5 puntos fuera de 1σ
    for i in range(n-4):
        ventana = datos[i:i+5]
        fuera_1sigma_sup = sum(1 for x in ventana if x > limite_1sigma_superior)
        fuera_1sigma_inf = sum(1 for x in ventana if x < limite_1sigma_inferior)
        
        if fuera_1sigma_sup >= 4:
            key = f"R3-{i}-sup"
            if key not in violaciones_detectadas:
                violaciones.append(f"Regla 3: Puntos {i+1}-{i+5} - 4/5 fuera de 1σ (superior)")
                violaciones_detectadas.add(key)
        
        if fuera_1sigma_inf >= 4:
            key = f"R3-{i}-inf"
            if key not in violaciones_detectadas:
                violaciones.append(f"Regla 3: Puntos {i+1}-{i+5} - 4/5 fuera de 1σ (inferior)")
                violaciones_detectadas.add(key)
    
    # Regla 4: 8 puntos consecutivos en un lado
    for i in range(n-7):
        ventana = datos[i:i+8]
        if all(x > CL for x in ventana):
            key = f"R4-{i}-sup"
            if key not in violaciones_detectadas:
                violaciones.append(f"Regla 4: Puntos {i+1}-{i+8} - 8 consecutivos arriba de CL")
                violaciones_detectadas.add(key)
        elif all(x < CL for x in ventana):
            key = f"R4-{i}-inf"
            if key not in violaciones_detectadas:
                violaciones.append(f"Regla 4: Puntos {i+1}-{i+8} - 8 consecutivos debajo de CL")
                violaciones_detectadas.add(key)
    
    # Regla 5: 6 puntos en tendencia
    for i in range(n-5):
        ventana = datos[i:i+6]
        if all(ventana[j] < ventana[j+1] for j in range(5)):
            key = f"R5-{i}-asc"
            if key not in violaciones_detectadas:
                violaciones.append(f"Regla 5: Puntos {i+1}-{i+6} - Tendencia ascendente continua")
                violaciones_detectadas.add(key)
        elif all(ventana[j] > ventana[j+1] for j in range(5)):
            key = f"R5-{i}-desc"
            if key not in violaciones_detectadas:
                violaciones.append(f"Regla 5: Puntos {i+1}-{i+6} - Tendencia descendente continua")
                violaciones_detectadas.add(key)
    
    return violaciones

def analizar_capacidad(subgroups, UCL, LCL, USL=None, LSL=None, chart_type='XR'):
    """
    Calcula índices Cp, Cpk, Pp, Ppk
    - Cp/Cpk: Capacidad potencial/real (usa sigma estimada de subgrupos)
    - Pp/Ppk: Performance (usa desviación estándar total)
    """
    medias = np.nanmean(subgroups, axis=1)
    media_proceso = np.mean(medias)
    
    # Sigma estimada (dentro de subgrupos) para Cp/Cpk
    if chart_type == 'XR':
        rangos = np.ptp(subgroups, axis=1)
        n = subgroups.shape[1]
        if n not in CONTROL_CHART_CONSTANTS:
            n_keys = sorted(CONTROL_CHART_CONSTANTS.keys())
            n = min(n_keys, key=lambda x: abs(x - n))
        d2 = CONTROL_CHART_CONSTANTS[n]['d2']
        sigma_within = np.mean(rangos) / d2
    else:
        stds = np.nanstd(subgroups, axis=1, ddof=1)
        n = subgroups.shape[1]
        if n not in CONTROL_CHART_CONSTANTS:
            n_keys = sorted(CONTROL_CHART_CONSTANTS.keys())
            n = min(n_keys, key=lambda x: abs(x - n))
        c4 = CONTROL_CHART_CONSTANTS[n]['c4']
        sigma_within = np.mean(stds) / c4
    
    # Sigma total (todas las observaciones) para Pp/Ppk
    todos_datos = subgroups.flatten()
    todos_datos = todos_datos[~np.isnan(todos_datos)]
    sigma_total = np.std(todos_datos, ddof=1)
    
    if sigma_within == 0 or sigma_total == 0:
        return None
    
    # Con límites de especificación
    if USL is not None and LSL is not None:
        rango_especificacion = USL - LSL
        
        # Cp y Cpk (capacidad)
        Cp = rango_especificacion / (6 * sigma_within)
        Cpu = (USL - media_proceso) / (3 * sigma_within)
        Cpl = (media_proceso - LSL) / (3 * sigma_within)
        Cpk = min(Cpu, Cpl)
        
        # Pp y Ppk (performance)
        Pp = rango_especificacion / (6 * sigma_total)
        Ppu = (USL - media_proceso) / (3 * sigma_total)
        Ppl = (media_proceso - LSL) / (3 * sigma_total)
        Ppk = min(Ppu, Ppl)
        
        # Interpretaciones
        def interpretar(valor):
            if valor >= 2.0:
                return 'Excelente (Clase Mundial)'
            elif valor >= 1.33:
                return 'Adecuado'
            elif valor >= 1.0:
                return 'Marginal (Requiere mejora)'
            else:
                return 'Inadecuado (Acción inmediata)'
        
        return {
            'sigma_within': sigma_within,
            'sigma_total': sigma_total,
            'media': media_proceso,
            'Cp': Cp,
            'Cpk': Cpk,
            'Cpu': Cpu,
            'Cpl': Cpl,
            'Pp': Pp,
            'Ppk': Ppk,
            'Ppu': Ppu,
            'Ppl': Ppl,
            'interpretacion_cp': interpretar(Cp),
            'interpretacion_cpk': interpretar(Cpk),
            'interpretacion_pp': interpretar(Pp),
            'interpretacion_ppk': interpretar(Ppk),
            'tiene_limites': True
        }
    else:
        # Sin límites de especificación
        rango_control = UCL - LCL
        Cp = rango_control / (6 * sigma_within)
        
        return {
            'sigma_within': sigma_within,
            'sigma_total': sigma_total,
            'media': media_proceso,
            'Cp': Cp,
            'interpretacion_cp': 'Excelente' if Cp >= 2.0 else 'Adecuado' if Cp >= 1.33 else 'Marginal' if Cp >= 1.0 else 'Inadecuado',
            'tiene_limites': False
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
    State('usl-input', 'value'),
    State('lsl-input', 'value')
)
def update_graph(n_clicks, contents, filename, manual_data, method, chart_type, USL, LSL):
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

    CLx = np.mean(means)
    CLr = np.mean(ranges)
    CLs = np.mean(stds)
    
    if chart_type == 'XR':
        UCLx = CLx + A2 * CLr
        LCLx = CLx - A2 * CLr
        UCLr = D4 * CLr
        LCLr = D3 * CLr
    else:
        UCLx = CLx + A3 * CLs
        LCLx = CLx - A3 * CLs
        UCLs = B4 * CLs
        LCLs = B3 * CLs

    # Gráfico X̄
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
    
    # Límites de control
    fig_xbar.add_hline(y=UCLx, line_dash='dash', line_color=colors['danger'], line_width=2.5,
                       annotation_text=f"UCL {UCLx:.4f}", annotation_position="right",
                       annotation=dict(font=dict(size=11, color=colors['danger'])))
    fig_xbar.add_hline(y=LCLx, line_dash='dash', line_color=colors['danger'], line_width=2.5,
                       annotation_text=f"LCL {LCLx:.4f}", annotation_position="right",
                       annotation=dict(font=dict(size=11, color=colors['danger'])))
    fig_xbar.add_hline(y=CLx, line_dash='solid', line_color=colors['success'], line_width=3,
                       annotation_text=f"CL {CLx:.4f}", annotation_position="right",
                       annotation=dict(font=dict(size=11, color=colors['success'])))
    
    # Límites de especificación USL/LSL
    if USL is not None:
        fig_xbar.add_hline(y=USL, line_dash='dot', line_color='purple', line_width=2.5,
                           annotation_text=f"USL {USL:.4f}", annotation_position="left",
                           annotation=dict(font=dict(size=11, color='purple')))
    
    if LSL is not None:
        fig_xbar.add_hline(y=LSL, line_dash='dot', line_color='purple', line_width=2.5,
                           annotation_text=f"LSL {LSL:.4f}", annotation_position="left",
                           annotation=dict(font=dict(size=11, color='purple')))
    
    # Zonas sigma
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

    # Gráfico R/S
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
    if chart_type == 'XR':
        num_fuera_control = len(fuera_control_x) + len(fuera_control_r)
    else:
        num_fuera_control = len(fuera_control_x) + len(fuera_control_s)
    
    violaciones_patrones = detectar_patrones_western_electric(means, UCLx, LCLx, CLx)
    
    # Alerta principal
    if num_fuera_control > 0 or len(violaciones_patrones) > 0:
        alerta_texto = html.Div([
            html.Div(style={'display': 'flex', 'alignItems': 'center', 'gap': '20px'}, children=[
                html.Div("⚠️", style={'fontSize': '60px'}),
                html.Div([
                    html.Div("Proceso Fuera de Control", style={'fontSize': '28px', 'fontWeight': '700', 'marginBottom': '8px'}),
                    html.Div(f"{num_fuera_control} puntos fuera de límites • {len(violaciones_patrones)} patrones anormales", 
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
                    html.Div("Proceso Bajo Control Estadístico", style={'fontSize': '28px', 'fontWeight': '700', 'marginBottom': '8px'}),
                    html.Div("Todos los puntos dentro de límites y sin patrones anormales", 
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

    # Análisis de capacidad con Pp y Ppk
    capacidad = analizar_capacidad(subgroups, UCLx, LCLx, USL, LSL, chart_type)
    
    # Cards de estadísticas
    estadisticas_cards = [
        # Card X̄
        html.Div(style={
            'backgroundColor': colors['bg_card'],
            'border': f'1px solid {colors["border"]}',
            'borderTop': f'4px solid {colors["accent_gold"]}',
            'borderRadius': '8px',
            'padding': '30px',
            'boxShadow': f'0 4px 12px {colors["shadow"]}'
        }, children=[
            html.Div("GRÁFICO X̄", style={'fontSize': '13px', 'fontWeight': '700', 'color': colors['text_secondary'], 'marginBottom': '10px', 'letterSpacing': '1px'}),
            html.Div("Promedios del Proceso", style={'fontSize': '18px', 'fontWeight': '700', 'color': colors['text_primary'], 'marginBottom': '20px'}),
            html.Div([
                html.Div("Línea Central", style={'fontSize': '11px', 'color': colors['text_secondary'], 'marginBottom': '5px'}),
                html.Div(f"{CLx:.4f}", style={'fontSize': '28px', 'fontWeight': '700', 'color': colors['text_primary'], 'marginBottom': '15px'})
            ], style={'padding': '15px', 'backgroundColor': '#FAFAFA', 'borderRadius': '6px', 'marginBottom': '15px'}),
            html.Div(style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '10px'}, children=[
                html.Div([
                    html.Div("UCL", style={'fontSize': '10px', 'color': colors['text_secondary'], 'marginBottom': '3px'}),
                    html.Div(f"{UCLx:.4f}", style={'fontSize': '16px', 'fontWeight': '700', 'color': colors['danger']})
                ]),
                html.Div([
                    html.Div("LCL", style={'fontSize': '10px', 'color': colors['text_secondary'], 'marginBottom': '3px'}),
                    html.Div(f"{LCLx:.4f}", style={'fontSize': '16px', 'fontWeight': '700', 'color': colors['danger']})
                ])
            ])
        ]),
        
        # Card R/S
        html.Div(style={
            'backgroundColor': colors['bg_card'],
            'border': f'1px solid {colors["border"]}',
            'borderTop': f'4px solid {colors["chart_line2"]}',
            'borderRadius': '8px',
            'padding': '30px',
            'boxShadow': f'0 4px 12px {colors["shadow"]}'
        }, children=[
            html.Div(f"GRÁFICO {'R' if chart_type == 'XR' else 'S'}", style={'fontSize': '13px', 'fontWeight': '700', 'color': colors['text_secondary'], 'marginBottom': '10px', 'letterSpacing': '1px'}),
            html.Div(f"{'Rangos' if chart_type == 'XR' else 'Desviación Estándar'}", style={'fontSize': '18px', 'fontWeight': '700', 'color': colors['text_primary'], 'marginBottom': '20px'}),
            html.Div([
                html.Div("Línea Central", style={'fontSize': '11px', 'color': colors['text_secondary'], 'marginBottom': '5px'}),
                html.Div(f"{CLr if chart_type == 'XR' else CLs:.4f}", style={'fontSize': '28px', 'fontWeight': '700', 'color': colors['text_primary'], 'marginBottom': '15px'})
            ], style={'padding': '15px', 'backgroundColor': '#FAFAFA', 'borderRadius': '6px', 'marginBottom': '15px'}),
            html.Div(style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '10px'}, children=[
                html.Div([
                    html.Div("UCL", style={'fontSize': '10px', 'color': colors['text_secondary'], 'marginBottom': '3px'}),
                    html.Div(f"{UCLr if chart_type == 'XR' else UCLs:.4f}", style={'fontSize': '16px', 'fontWeight': '700', 'color': colors['danger']})
                ]),
                html.Div([
                    html.Div("n", style={'fontSize': '10px', 'color': colors['text_secondary'], 'marginBottom': '3px'}),
                    html.Div(f"{n}", style={'fontSize': '16px', 'fontWeight': '700', 'color': colors['text_primary']})
                ])
            ])
        ])
    ]
    
    # Cards de capacidad
    if capacidad:
        # Card Cp
        estadisticas_cards.append(
            html.Div(style={
                'backgroundColor': colors['bg_card'],
                'border': f'1px solid {colors["border"]}',
                'borderTop': f'4px solid {colors["success"]}',
                'borderRadius': '8px',
                'padding': '30px',
                'boxShadow': f'0 4px 12px {colors["shadow"]}'
            }, children=[
                html.Div("CAPACIDAD (Cp)", style={'fontSize': '13px', 'fontWeight': '700', 'color': colors['text_secondary'], 'marginBottom': '10px', 'letterSpacing': '1px'}),
                html.Div("Potencial del Proceso", style={'fontSize': '18px', 'fontWeight': '700', 'color': colors['text_primary'], 'marginBottom': '20px'}),
                html.Div([
                    html.Div("Índice Cp", style={'fontSize': '11px', 'color': colors['text_secondary'], 'marginBottom': '5px'}),
                    html.Div(f"{capacidad['Cp']:.3f}", style={'fontSize': '32px', 'fontWeight': '700', 'color': colors['text_primary']})
                ], style={'padding': '15px', 'backgroundColor': '#FAFAFA', 'borderRadius': '6px', 'marginBottom': '15px'}),
                html.Div(capacidad['interpretacion_cp'], style={
                    'padding': '8px 16px',
                    'background': colors['success'] if capacidad['Cp'] >= 1.33 else colors['warning'] if capacidad['Cp'] >= 1.0 else colors['danger'],
                    'borderRadius': '6px',
                    'fontSize': '12px',
                    'fontWeight': '700',
                    'textAlign': 'center',
                    'color': 'white',
                    'textTransform': 'uppercase'
                })
            ])
        )
        
        # Card Cpk (solo si hay límites)
        if capacidad['tiene_limites']:
            estadisticas_cards.append(
                html.Div(style={
                    'backgroundColor': colors['bg_card'],
                    'border': f'1px solid {colors["border"]}',
                    'borderTop': '4px solid #9C27B0',
                    'borderRadius': '8px',
                    'padding': '30px',
                    'boxShadow': f'0 4px 12px {colors["shadow"]}'
                }, children=[
                    html.Div("CAPACIDAD REAL (Cpk)", style={'fontSize': '13px', 'fontWeight': '700', 'color': colors['text_secondary'], 'marginBottom': '10px', 'letterSpacing': '1px'}),
                    html.Div("Con Centrado", style={'fontSize': '18px', 'fontWeight': '700', 'color': colors['text_primary'], 'marginBottom': '20px'}),
                    html.Div([
                        html.Div("Índice Cpk", style={'fontSize': '11px', 'color': colors['text_secondary'], 'marginBottom': '5px'}),
                        html.Div(f"{capacidad['Cpk']:.3f}", style={'fontSize': '32px', 'fontWeight': '700', 'color': colors['text_primary']})
                    ], style={'padding': '15px', 'backgroundColor': '#FAFAFA', 'borderRadius': '6px', 'marginBottom': '15px'}),
                    html.Div(style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '10px', 'marginBottom': '15px'}, children=[
                        html.Div([
                            html.Div("Cpu", style={'fontSize': '10px', 'color': colors['text_secondary'], 'marginBottom': '3px'}),
                            html.Div(f"{capacidad['Cpu']:.3f}", style={'fontSize': '14px', 'fontWeight': '700', 'color': colors['text_primary']})
                        ]),
                        html.Div([
                            html.Div("Cpl", style={'fontSize': '10px', 'color': colors['text_secondary'], 'marginBottom': '3px'}),
                            html.Div(f"{capacidad['Cpl']:.3f}", style={'fontSize': '14px', 'fontWeight': '700', 'color': colors['text_primary']})
                        ])
                    ]),
                    html.Div(capacidad['interpretacion_cpk'], style={
                        'padding': '8px 16px',
                        'background': colors['success'] if capacidad['Cpk'] >= 1.33 else colors['warning'] if capacidad['Cpk'] >= 1.0 else colors['danger'],
                        'borderRadius': '6px',
                        'fontSize': '12px',
                        'fontWeight': '700',
                        'textAlign': 'center',
                        'color': 'white',
                        'textTransform': 'uppercase'
                    })
                ])
            )
            
            # Card Pp
            estadisticas_cards.append(
                html.Div(style={
                    'backgroundColor': colors['bg_card'],
                    'border': f'1px solid {colors["border"]}',
                    'borderTop': '4px solid #FF5722',
                    'borderRadius': '8px',
                    'padding': '30px',
                    'boxShadow': f'0 4px 12px {colors["shadow"]}'
                }, children=[
                    html.Div("PERFORMANCE (Pp)", style={'fontSize': '13px', 'fontWeight': '700', 'color': colors['text_secondary'], 'marginBottom': '10px', 'letterSpacing': '1px'}),
                    html.Div("Desempeño Total", style={'fontSize': '18px', 'fontWeight': '700', 'color': colors['text_primary'], 'marginBottom': '20px'}),
                    html.Div([
                        html.Div("Índice Pp", style={'fontSize': '11px', 'color': colors['text_secondary'], 'marginBottom': '5px'}),
                        html.Div(f"{capacidad['Pp']:.3f}", style={'fontSize': '32px', 'fontWeight': '700', 'color': colors['text_primary']})
                    ], style={'padding': '15px', 'backgroundColor': '#FAFAFA', 'borderRadius': '6px', 'marginBottom': '15px'}),
                    html.Div(capacidad['interpretacion_pp'], style={
                        'padding': '8px 16px',
                        'background': colors['success'] if capacidad['Pp'] >= 1.33 else colors['warning'] if capacidad['Pp'] >= 1.0 else colors['danger'],
                        'borderRadius': '6px',
                        'fontSize': '12px',
                        'fontWeight': '700',
                        'textAlign': 'center',
                        'color': 'white',
                        'textTransform': 'uppercase'
                    })
                ])
            )
            
            # Card Ppk
            estadisticas_cards.append(
                html.Div(style={
                    'backgroundColor': colors['bg_card'],
                    'border': f'1px solid {colors["border"]}',
                    'borderTop': '4px solid #FF6F00',
                    'borderRadius': '8px',
                    'padding': '30px',
                    'boxShadow': f'0 4px 12px {colors["shadow"]}'
                }, children=[
                    html.Div("PERFORMANCE REAL (Ppk)", style={'fontSize': '13px', 'fontWeight': '700', 'color': colors['text_secondary'], 'marginBottom': '10px', 'letterSpacing': '1px'}),
                    html.Div("Con Centrado", style={'fontSize': '18px', 'fontWeight': '700', 'color': colors['text_primary'], 'marginBottom': '20px'}),
                    html.Div([
                        html.Div("Índice Ppk", style={'fontSize': '11px', 'color': colors['text_secondary'], 'marginBottom': '5px'}),
                        html.Div(f"{capacidad['Ppk']:.3f}", style={'fontSize': '32px', 'fontWeight': '700', 'color': colors['text_primary']})
                    ], style={'padding': '15px', 'backgroundColor': '#FAFAFA', 'borderRadius': '6px', 'marginBottom': '15px'}),
                    html.Div(style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '10px', 'marginBottom': '15px'}, children=[
                        html.Div([
                            html.Div("Ppu", style={'fontSize': '10px', 'color': colors['text_secondary'], 'marginBottom': '3px'}),
                            html.Div(f"{capacidad['Ppu']:.3f}", style={'fontSize': '14px', 'fontWeight': '700', 'color': colors['text_primary']})
                        ]),
                        html.Div([
                            html.Div("Ppl", style={'fontSize': '10px', 'color': colors['text_secondary'], 'marginBottom': '3px'}),
                            html.Div(f"{capacidad['Ppl']:.3f}", style={'fontSize': '14px', 'fontWeight': '700', 'color': colors['text_primary']})
                        ])
                    ]),
                    html.Div(capacidad['interpretacion_ppk'], style={
                        'padding': '8px 16px',
                        'background': colors['success'] if capacidad['Ppk'] >= 1.33 else colors['warning'] if capacidad['Ppk'] >= 1.0 else colors['danger'],
                        'borderRadius': '6px',
                        'fontSize': '12px',
                        'fontWeight': '700',
                        'textAlign': 'center',
                        'color': 'white',
                        'textTransform': 'uppercase'
                    })
                ])
            )
    
    estadisticas_html = html.Div(style={
        'display': 'grid',
        'gridTemplateColumns': 'repeat(auto-fit, minmax(260px, 1fr))',
        'gap': '20px',
        'marginBottom': '30px'
    }, children=estadisticas_cards)

    # Análisis avanzado
    analisis_html = html.Div(style={
        'backgroundColor': colors['bg_card'],
        'borderRadius': '8px',
        'padding': '35px',
        'marginBottom': '30px',
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
            html.Div("PUNTOS FUERA DE CONTROL", style={'fontSize': '12px', 'fontWeight': '700', 'color': colors['text_secondary'], 'letterSpacing': '1px', 'marginBottom': '15px'}),
            html.Div(style={
                'display': 'inline-flex',
                'alignItems': 'center',
                'gap': '15px',
                'padding': '15px 25px',
                'background': '#FFEBEE' if num_fuera_control > 0 else '#E8F5E9',
                'borderRadius': '6px',
                'border': f'1px solid {colors["danger"] if num_fuera_control > 0 else colors["success"]}',
                'marginBottom': '20px'
            }, children=[
                html.Span(f"{num_fuera_control}", style={'fontSize': '32px', 'fontWeight': '700', 'color': colors['danger'] if num_fuera_control > 0 else colors['success']}),
                html.Span("puntos detectados", style={'fontSize': '14px', 'fontWeight': '600', 'color': colors['text_secondary']})
            ]),
            
            html.Div([
                html.Div([
                    html.Div("Gráfico X̄:", style={'fontWeight': '700', 'marginBottom': '10px', 'color': colors['chart_line1'], 'fontSize': '15px'}),
                    html.Ul([
                        html.Li(f"Subgrupo {i+1}: X̄ = {means[i]:.4f}", 
                               style={'color': colors['text_primary'], 'marginBottom': '5px', 'fontSize': '14px'}) 
                        for i in fuera_control_x
                    ], style={'paddingLeft': '20px'}) if len(fuera_control_x) > 0 
                    else html.P("✓ Todos los puntos bajo control", style={'color': colors['success'], 'fontWeight': '600', 'paddingLeft': '20px'})
                ], style={'marginBottom': '15px'}),
                html.Div([
                    html.Div(f"Gráfico {'R' if chart_type == 'XR' else 'S'}:", style={'fontWeight': '700', 'marginBottom': '10px', 'color': colors['chart_line2'], 'fontSize': '15px'}),
                    html.Ul([
                        html.Li(f"Subgrupo {i+1}: {'R' if chart_type == 'XR' else 'S'} = {(ranges[i] if chart_type == 'XR' else stds[i]):.4f}", 
                               style={'color': colors['text_primary'], 'marginBottom': '5px', 'fontSize': '14px'}) 
                        for i in (fuera_control_r if chart_type == 'XR' else fuera_control_s)
                    ], style={'paddingLeft': '20px'}) if len(fuera_control_r if chart_type == 'XR' else fuera_control_s) > 0 
                    else html.P("✓ Todos los puntos bajo control", style={'color': colors['success'], 'fontWeight': '600', 'paddingLeft': '20px'})
                ])
            ], style={'padding': '20px', 'backgroundColor': '#FAFAFA', 'borderRadius': '6px', 'marginBottom': '30px'})
        ]),
        
        html.Div([
            html.Div("PATRONES ANORMALES", style={'fontSize': '12px', 'fontWeight': '700', 'color': colors['text_secondary'], 'letterSpacing': '1px', 'marginBottom': '15px'}),
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
                html.Span("patrones detectados", style={'fontSize': '14px', 'fontWeight': '600', 'color': colors['text_secondary']})
            ]),
            
            html.Div([
                html.Ul([
                    html.Li(v, style={'color': colors['text_primary'], 'marginBottom': '10px', 'fontSize': '14px', 'lineHeight': '1.6'}) 
                    for v in violaciones_patrones
                ], style={'paddingLeft': '20px'}) if len(violaciones_patrones) > 0 
                else html.P("✓ No se detectaron patrones anormales", style={'color': colors['success'], 'fontWeight': '600', 'fontSize': '15px'})
            ], style={'padding': '20px', 'backgroundColor': '#FAFAFA', 'borderRadius': '6px'})
        ])
    ])

    # Recomendaciones mejoradas
    recomendaciones_lista = []
    
    if num_fuera_control > 0:
        recomendaciones_lista.extend([
            "🔍 Investigar causas especiales en puntos fuera de límites",
            "⚙️ Verificar calibración de equipos de medición",
            "👤 Revisar cambios en operadores o métodos",
            "📦 Inspeccionar calidad de materia prima",
            "🌡️ Evaluar condiciones ambientales"
        ])
    
    if len(violaciones_patrones) > 0:
        tiene_r1 = any("Regla 1" in v for v in violaciones_patrones)
        tiene_r2 = any("Regla 2" in v for v in violaciones_patrones)
        tiene_r3 = any("Regla 3" in v for v in violaciones_patrones)
        tiene_r4 = any("Regla 4" in v for v in violaciones_patrones)
        tiene_r5 = any("Regla 5" in v for v in violaciones_patrones)
        
        if tiene_r1:
            recomendaciones_lista.append("⚡ Regla 1: Evento extremo - Buscar causa asignable inmediata")
        if tiene_r2:
            recomendaciones_lista.append("📊 Regla 2: Variación excesiva - Revisar estabilidad")
        if tiene_r3:
            recomendaciones_lista.append("🎯 Regla 3: Desviación sostenida - Verificar ajustes")
        if tiene_r4:
            recomendaciones_lista.append("↕️ Regla 4: Sesgo detectado - Verificar centrado")
        if tiene_r5:
            recomendaciones_lista.append("📈 Regla 5: Tendencia continua - Verificar desgaste de herramientas")
    
    if capacidad and capacidad['tiene_limites']:
        if capacidad['Cpk'] < 1.0:
            recomendaciones_lista.extend([
                "🚨 Cpk < 1.0: Proceso inadecuado - Acción urgente",
                "🔧 Reducir variación o ampliar especificaciones"
            ])
        elif capacidad['Cpk'] < 1.33:
            recomendaciones_lista.append("⚠️ Cpk marginal: Implementar mejora continua")
        
        if capacidad['Ppk'] < capacidad['Cpk']:
            recomendaciones_lista.append("📉 Ppk < Cpk: Variación entre subgrupos alta - Revisar consistencia del proceso")
        
        if abs(capacidad['Cpu'] - capacidad['Cpl']) > 0.2:
            recomendaciones_lista.append("⚖️ Proceso descentrado - Ajustar hacia valor nominal")
    
    if len(recomendaciones_lista) == 0:
        recomendaciones_lista.extend([
            "✅ Proceso estable y bajo control",
            "📊 Mantener monitoreo continuo",
            "📝 Documentar condiciones como estándar",
            "🔄 Auditorías periódicas preventivas"
        ])
    
    recomendaciones_html = html.Div(style={
        'backgroundColor': colors['bg_card'],
        'borderRadius': '8px',
        'padding': '35px',
        'border': f'1px solid {colors["border"]}',
        'borderLeft': f'5px solid {colors["accent_gold"]}',
        'boxShadow': f'0 4px 12px {colors["shadow"]}'
    }, children=[
        html.H4("Recomendaciones", style={
            'color': colors['text_primary'],
            'margin': '0 0 25px 0',
            'fontSize': '24px',
            'fontWeight': '700'
        }),
        html.Ul([
            html.Li(rec, style={
                'color': colors['text_primary'],
                'marginBottom': '12px',
                'fontSize': '15px',
                'lineHeight': '1.7'
            }) 
            for rec in recomendaciones_lista
        ], style={'paddingLeft': '25px'})
    ])

    return (fig_xbar, fig_rs, alerta_texto, alerta_style, estadisticas_html, 
            analisis_html, recomendaciones_html, {'display': 'block'})


if __name__ == '__main__':
    app.run(debug=True)