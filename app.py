import streamlit as st
import pandas as pd
import scipy.stats
import time

# Variables de estado
if 'experiment_no' not in st.session_state:
    st.session_state['experiment_no'] = 0

if 'df_experiment_results' not in st.session_state:
    st.session_state['df_experiment_results'] = pd.DataFrame(columns=['no', 'iteraciones', 'media'])

# Título
st.header('Lanzar una moneda')

# Control deslizante y botón
number_of_trials = st.slider('¿Número de intentos?', 1, 1000, 10, key='slider_unico')
start_button = st.button('Ejecutar')

# Gráfico
chart = st.line_chart([0.5])

# Función para lanzar moneda
def toss_coin(n):
    trial_outcomes = scipy.stats.bernoulli.rvs(p=0.5, size=n)
    mean = None
    outcome_no = 0
    outcome_1_count = 0
    for r in trial_outcomes:
        outcome_no += 1
        if r == 1:
            outcome_1_count += 1
        mean = outcome_1_count / outcome_no
        chart.add_rows([mean])
        time.sleep(0.05)
    return mean

# Ejecutar experimento
if start_button:
    st.write(f'Experimento con {number_of_trials} intentos en curso.')
    st.session_state['experiment_no'] += 1
    mean = toss_coin(number_of_trials)

    # Guardar resultados
    st.session_state['df_experiment_results'] = pd.concat([
        st.session_state['df_experiment_results'],
        pd.DataFrame([[st.session_state['experiment_no'], number_of_trials, mean]],
                     columns=['no', 'iteraciones', 'media'])
    ], ignore_index=True)

# Mostrar resultados
st.write(st.session_state['df_experiment_results'])
