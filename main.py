import streamlit as st
import pandas as pd

from htbuilder import HtmlElement, div, ul, li, br, hr, a, p, img, styles, classes, fonts
from htbuilder.units import percent, px
from htbuilder.funcs import rgba, rgb


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

def image(src_as_string, **style):
    return img(src=src_as_string, style=styles(**style))


def link(link, text, **style):
    return a(_href=link, _target="_blank", style=styles(**style))(text)


def layout(*args):

    style = """
    <style>
      # MainMenu {visibility: hidden;}
      footer {visibility: hidden;}
     .stApp { bottom: 105px; }
    </style>
    """

    style_div = styles(
        position="fixed",
        left=0,
        bottom=0,
        margin=px(0, 0, 0, 0),
        width=percent(100),
        color="Orange",
        text_align="center",
        height="auto",
        opacity=1
    )

    style_hr = styles(
        display="block",
        margin=px(8, 8, "auto", "auto"),
        border_style="inset",
        border_width=px(2)
    )

    body = p()
    foot = div(
        style=style_div
    )(
        hr(
            style=style_hr
        ),
        body
    )

    st.markdown(style, unsafe_allow_html=True)

    for arg in args:
        if isinstance(arg, str):
            body(arg)

        elif isinstance(arg, HtmlElement):
            body(arg)

    st.markdown(str(foot), unsafe_allow_html=True)


def footer():
    myargs = [
        "Made in Streamlit",
        image('https://avatars3.githubusercontent.com/u/45109972?s=400&v=4',
              width=px(25), height=px(25)),
        " by ",
        link("https://www.linkedin.com/in/caudanna-moussa-y-70115710b/", "Caudanna Moussa YEO"),
    ]
    layout(*myargs)


if __name__ == "__main__":
    footer()
