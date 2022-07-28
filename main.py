import streamlit as st
import pandas as pd
import leafmap.foliumap as leafmap
st.title("Heatmap")

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    #  # To read file as bytes:
    #  bytes_data = uploaded_file.getvalue()
    #  st.write(bytes_data)

    #  # To convert to a string based IO:
    #  stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    #  st.write(stringio)

    #  # To read file as string:
    #  string_data = stringio.read()
    #  st.write(string_data)

     # Can be used wherever a "file-like" object is accepted:
    dataframe = pd.read_excel(uploaded_file,
                                # on_bad_lines='skip'
                                )
    st.write(dataframe)
    
    lat = st.selectbox(
     'Quelle est la colonne de la latitude ?',
     dataframe.columns)

    long = st.selectbox(
     'Quelle est la colonne de la longitude ?',
     dataframe.columns)
    dataframe = dataframe.dropna(subset=[lat,long])
    dataframe = dataframe.assign(**{"val":1})
    filepath = "data.csv"
    m = leafmap.Map(center=[5.3, -4], zoom=10)
    m.add_heatmap(
        dataframe,
        latitude=lat,
        longitude=long,
        value="val",
        name="Heat map",
        radius=20,
    )
    m.to_streamlit(height=700)