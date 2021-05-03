import plotly.express as px

def MapRepresentation(df) : 
    fig = px.scatter(df, x="x", y="y", color="fruit", custom_data=["customdata"])
    fig.update_layout(clickmode='event+select')
    fig.update_traces(marker_size=20)
    return(fig)