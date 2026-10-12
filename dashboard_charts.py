"""Biểu đồ Plotly: cùng màu nhãn và cùng mẫu số với notebook."""
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from steel_analysis import COLORS, fault_structure, fault_by_steel


def finish(fig, title, x_label, y_label, height=430):
    fig.update_layout(title=title, xaxis_title=x_label, yaxis_title=y_label, template="plotly_white",
                      height=height, margin=dict(l=20, r=20, t=70, b=50),
                      font=dict(family="Arial", size=12), legend_title_text="Loại lỗi")
    return fig


def structure_chart(data):
    table = fault_structure(data)
    fig = px.bar(table, x="Count", y="Fault_Type_Clean", color="Fault_Type_Clean",
                 color_discrete_map=COLORS, text=table["Percent"].map(lambda v: f"{v:.2f}%"),
                 hover_data={"Count": True, "Percent": ":.2f"})
    fig.update_yaxes(categoryorder="array", categoryarray=table["Fault_Type_Clean"].tolist(), autorange="reversed")
    fig.update_xaxes(rangemode="tozero")
    fig.update_layout(showlegend=False)
    return finish(fig, "Cơ cấu lỗi trong mẫu đang chọn", "Số bản ghi lỗi", "Loại lỗi")


def pareto_chart(data):
    table = fault_structure(data)
    fig = go.Figure()
    fig.add_bar(x=table["Fault_Type_Clean"], y=table["Count"], name="Số bản ghi",
                marker_color=[COLORS[label] for label in table["Fault_Type_Clean"]])
    fig.add_scatter(x=table["Fault_Type_Clean"], y=table["Cumulative_Percent"], name="Lũy kế (%)",
                    mode="lines+markers", yaxis="y2", line_color="#202020")
    fig.update_layout(yaxis2=dict(title="Lũy kế (%)", overlaying="y", side="right", range=[0, 105]),
                      legend=dict(orientation="h", y=1.15), showlegend=True)
    fig.update_yaxes(rangemode="tozero")
    return finish(fig, "Pareto số bản ghi lỗi", "Loại lỗi (giảm dần theo số lượng)", "Số bản ghi lỗi")


def steel_charts(data):
    table = fault_by_steel(data)
    order = fault_structure(data)["Fault_Type_Clean"].tolist()
    counts, shares = go.Figure(), go.Figure()
    for steel, pattern in [("A300", "/"), ("A400", "")]:
        subset = table.loc[table["Steel_Type"].eq(steel)].set_index("Fault_Type_Clean").reindex(order)
        n = int(subset["Count"].sum())
        counts.add_bar(x=order, y=subset["Count"], name=f"{steel} (n={n:,})",
                       marker=dict(color=[COLORS[label] for label in order], pattern_shape=pattern))
    for label in order:
        subset = table.loc[table["Fault_Type_Clean"].eq(label)]
        shares.add_bar(x=subset["Steel_Type"], y=subset["Percent_Within_Steel"], name=label,
                       marker_color=COLORS[label], customdata=subset[["Count", "N_Steel"]],
                       hovertemplate="%{x}: %{y:.2f}%<br>%{customdata[0]} / %{customdata[1]} bản ghi<extra>%{fullData.name}</extra>")
    counts.update_layout(barmode="group", legend_title_text="Dòng thép", legend=dict(orientation="h", y=1.15))
    counts.update_yaxes(rangemode="tozero")
    shares.update_layout(barmode="stack")
    shares.update_yaxes(range=[0, 100])
    return (finish(counts, "Số lượng theo dòng thép", "Loại lỗi", "Số bản ghi lỗi"),
            finish(shares, "Cơ cấu trong từng dòng thép", "Dòng thép", "Tỷ trọng trong dòng thép (%)"))


def brightness_chart(data):
    corr = data["Minimum_of_Luminosity"].corr(data["Maximum_of_Luminosity"]) if len(data) > 1 else np.nan
    label = f"r={corr:.4f}" if np.isfinite(corr) else "r chưa xác định"
    fig = px.scatter(data, x="Minimum_of_Luminosity", y="Maximum_of_Luminosity", color="Fault_Type_Clean",
                     color_discrete_map=COLORS, hover_data=["Steel_Type", "Source_Row"], opacity=.4)
    return finish(fig, f"Độ sáng nhỏ nhất × lớn nhất | {label}", "Độ sáng nhỏ nhất (thang nguồn)", "Độ sáng lớn nhất (thang nguồn)", 500)


def box_chart(data, column, title, axis_title, logarithmic=False):
    """Tứ phân vị tuyến tính Pandas; râu tới điểm quan sát trong 1,5 IQR."""
    order = fault_structure(data)["Fault_Type_Clean"].tolist()
    fig = go.Figure()
    axis_categories = []
    for label in order:
        values = data.loc[data["Fault_Type_Clean"].eq(label), column]
        q1, median, q3 = values.quantile([.25, .5, .75])
        iqr = q3 - q1
        inside = values.between(q1 - 1.5 * iqr, q3 + 1.5 * iqr)
        category = f"{label} (n={len(values):,})"
        axis_categories.append(category)
        fig.add_trace(go.Box(name=label, y=[category], q1=[q1], median=[median], q3=[q3],
                             lowerfence=[values.loc[inside].min()], upperfence=[values.loc[inside].max()],
                             orientation="h", marker_color=COLORS[label], boxpoints=False, showlegend=False))
        outliers = values.loc[~inside]
        fig.add_scatter(x=outliers, y=[category] * len(outliers), mode="markers", name=label,
                        marker=dict(color=COLORS[label], size=5, opacity=.5), showlegend=False,
                        hovertemplate=f"{label}<br>Giá trị: %{{x}}<extra></extra>")
    fig.update_yaxes(categoryorder="array", categoryarray=axis_categories, autorange="reversed")
    if logarithmic:
        fig.update_xaxes(type="log")
    return finish(fig, title, axis_title, "Loại lỗi và cỡ mẫu", 500)


def trade_charts(data):
    lines, balance = go.Figure(), go.Figure()
    for column, label, color in [("Export_USD", "Xuất khẩu", "#0072B2"), ("Import_USD", "Nhập khẩu", "#D55E00")]:
        lines.add_scatter(x=data["Year"], y=data[column] / 1e9, name=label, mode="lines+markers",
                          line_color=color, connectgaps=False)
    balance.add_bar(x=data["Year"], y=data["Trade_Balance_USD"] / 1e9, name="Xuất − nhập", marker_color="#586675")
    balance.add_hline(y=0, line_color="#222222")
    for year in data.loc[data["HS_Version_Changed"], "Year"]:
        for fig in [lines, balance]:
            fig.add_vline(x=int(year), line_dash="dash", line_color="#999999", annotation_text="Đổi HS")
    lines.update_yaxes(rangemode="tozero")
    for fig in [lines, balance]:
        fig.update_xaxes(dtick=1)
    lines.update_layout(legend=dict(orientation="h", y=1.15), legend_title_text="Luồng thương mại")
    return (finish(lines, "Xuất nhập khẩu sắt và thép Việt Nam", "Năm", "Trị giá danh nghĩa (tỷ USD)"),
            finish(balance, "Chênh lệch xuất nhập khẩu", "Năm", "Xuất khẩu − nhập khẩu (tỷ USD)"))
