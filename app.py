import streamlit as st
import pandas as pd
import webbrowser

# CSS para personalizar los colores de la tabla y el título
st.markdown(
    """
    <style>
    .gold-header h1 {
        color: gold;
        font-size: 36px;
        font-weight: bold;
        text-align: center;
    }
    .centered-table {
        margin-left: auto;
        margin-right: auto;
        width: 50%;
    }
    .dataframe thead tr {
        background: linear-gradient(to right, orange, white);
    }
    .dataframe tbody tr:nth-child(odd) {
        background: linear-gradient(to right, #ADD8E6, white);
    }
    .dataframe tbody tr:nth-child(even) {
        background: linear-gradient(to right, white, #ADD8E6);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Título de la aplicación con la clase personalizada
st.markdown('<div class="gold-header"><h1>Esperanza - Mi Primera Comunión</h1></div>', unsafe_allow_html=True)

# Cargar los regalos desde el archivo CSV
df_regalos = pd.read_csv('lista_regalos_no_asignados.csv')

# Ajustar el índice para que comience en 1
df_regalos.index += 1

# Filtrar los regalos disponibles y no disponibles
df_disponibles = df_regalos[df_regalos['Disponible'] == True]
df_no_disponibles = df_regalos[df_regalos['Disponible'] == False]

# Variables para manejar la selección del regalo
if 'selected_gift' not in st.session_state:
    st.session_state['selected_gift'] = None
if 'action' not in st.session_state:
    st.session_state['action'] = None

# Mostrar la lista de regalos no asignados centrada
st.subheader('Regalos Disponibles')
st.markdown(df_disponibles[['Nombre', 'Precio']].to_html(index=False, classes='centered-table dataframe'), unsafe_allow_html=True)

# Selectbox para seleccionar un regalo no asignado
selected_no_asignado = st.selectbox('¿Que quieres regalarle a Esperanza?', [''] + df_disponibles['Nombre'].tolist())

if selected_no_asignado:
    st.session_state['selected_gift'] = df_disponibles[df_disponibles['Nombre'] == selected_no_asignado].index[0]
    st.session_state['action'] = 'Asignar'

# Mostrar el mensaje de confirmación para asignar
if st.session_state['selected_gift'] is not None and st.session_state['action'] == 'Asignar':
    selected_gift = st.session_state['selected_gift']
    regalo = df_disponibles.loc[selected_gift]
    st.write(f"**¿Confirmas que deseas regalar {regalo['Nombre']}?**")
    confirm_col, cancel_col = st.columns(2)
    if confirm_col.button("Sí", key="confirm_asignar"):
        df_regalos.at[selected_gift, 'Disponible'] = False
        df_regalos.to_csv('lista_regalos_no_asignados.csv', index=False)
        st.success(f"Has escogido {regalo['Nombre']} para regalarle a Esperanza")
        webbrowser.open(regalo['Link'])
        st.session_state['selected_gift'] = None
        st.session_state['action'] = None
    if cancel_col.button("No", key="cancel_asignar"):
        st.session_state['selected_gift'] = None
        st.session_state['action'] = None

# Mostrar la lista de regalos asignados centrada
st.subheader('Regalos Asignados')
st.markdown(df_no_disponibles[['Nombre']].to_html(index=False, classes='centered-table dataframe'), unsafe_allow_html=True)

# Selectbox para seleccionar un regalo asignado
selected_asignado = st.selectbox('¿Has Cambiado de Opinion?', [''] + df_no_disponibles['Nombre'].tolist())

if selected_asignado:
    st.session_state['selected_gift'] = df_no_disponibles[df_no_disponibles['Nombre'] == selected_asignado].index[0]
    st.session_state['action'] = 'Desasignar'

# Mostrar el mensaje de confirmación para desasignar
if st.session_state['selected_gift'] is not None and st.session_state['action'] == 'Desasignar':
    selected_gift = st.session_state['selected_gift']
    regalo = df_no_disponibles.loc[selected_gift]
    st.write(f"**¿Prefieres no regalar {regalo['Nombre']} y escoger otro regalo?**")
    confirm_col, cancel_col = st.columns(2)
    if confirm_col.button("Sí", key="confirm_desasignar"):
        df_regalos.at[selected_gift, 'Disponible'] = True
        df_regalos.to_csv('lista_regalos_no_asignados.csv', index=False)
        st.success(f"{regalo['Nombre']} Vuelve a estar disponible para regalar")
        st.session_state['selected_gift'] = None
        st.session_state['action'] = None
    if cancel_col.button("No", key="cancel_desasignar"):
        st.session_state['selected_gift'] = None
        st.session_state['action'] = None
