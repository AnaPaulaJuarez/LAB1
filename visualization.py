def plot_investment_strategy(data: "DataFrame que contiene el desempeño de la estrategia "):

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=data.index, y=data["Evolución Capital Invertido"], name="Capital Invertido"))
    fig.update_layout(title="Desempeño estrategia de inversión", xaxis_title="Date", yaxis_title="MXN")

    fig.add_trace(go.Scatter(x=data.index, y=data["Evolución Capital Invertido"], name="Invested Capital"))
    fig.update_layout(title="Investment Strategy Performance", xaxis_title="Fecha", yaxis_title="MXN")

    
    return fig

