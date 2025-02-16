# Web Lista de Comunion en streamlit
import pandas as pd
import streamlit as st

# Cargamos los datos de la lista de regalos sin asignar
df = pd.read_csv("lista_regalos_no_asignados.csv")