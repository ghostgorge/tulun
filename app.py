import streamlit as st
import networkx as nx
import plotly.graph_objects as go
import random

st.set_page_config(page_title="🔗 图论演示系统", layout="wide")
st.title("🔗 图论可视化与遍历演示")

# ====================
# 🧱 图初始化
# ====================
graph_type = st.selectbox("选择图类型", ["无向图", "有向图"])
G = nx.DiGraph() if graph_type == "有向图" else nx.Graph()

num_nodes = st.slider("节点数量", 3, 20, 6)
edge_prob = st.slider("边生成概率", 0.1, 1.0, 0.3)

if st.button("🎲 生成随机图"):
    G = nx.gnp_random_graph(num_nodes, edge_prob, directed=(graph_type == "有向图"))

# ====================
# 📈 图可视化函数
# ====================
def plot_graph(G, highlight_path=None):
    pos = nx.spring_layout(G, seed=42)
    edge_x, edge_y = [], []

    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x, node_y = [], []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=[str(n) for n in G.nodes()],
        textposition="top center",
        marker=dict(size=30, color='skyblue', line=dict(width=2, color='black')),
        hoverinfo='text'
    )

    fig = go.Figure(data=[edge_trace, node_trace],
                   layout=go.Layout(
                       showlegend=False,
                       hovermode='closest',
                       margin=dict(b=20, l=20, r=20, t=20),
                       xaxis=dict(showgrid=False, zeroline=False),
                       yaxis=dict(showgrid=False, zeroline=False)
                   ))

    # 高亮路径
    if highlight_path:
        path_edges = list(zip(highlight_path, highlight_path[1:]))
        for u, v in path_edges:
            fig.add_trace(go.Scatter(
                x=[pos[u][0], pos[v][0]],
                y=[pos[u][1], pos[v][1]],
                mode="lines+markers+text",
                line=dict(color="red", width=4),
                marker=dict(color="red", size=10),
                text=[f"{u}", f"{v}"],
                textposition="top center"
            ))

    return fig

# ====================
# 🔁 BFS / DFS 演示
# ====================
algo = st.selectbox("选择遍历算法", ["BFS", "DFS"])

if G.number_of_nodes() == 0:
    st.warning("图为空，请先生成图！")
else:
    valid_nodes = list(G.nodes())
    start_node = st.selectbox("起始节点", valid_nodes, index=0)

    if st.button("🚀 开始遍历"):
        def bfs(G, start):
            visited_order = []
            queue = [start]
            visited_set = set()
            while queue:
                node = queue.pop(0)
                if node not in visited_set:
                    visited_order.append(node)
                    visited_set.add(node)
                    queue.extend(sorted(set(G.neighbors(node)) - visited_set))
            return visited_order

        def dfs(G, start):
            visited_order = []
            stack = [start]
            visited_set = set()
            while stack:
                node = stack.pop()
                if node not in visited_set:
                    visited_order.append(node)
                    visited_set.add(node)
                    stack.extend(sorted(set(G.neighbors(node)) - visited_set, reverse=True))
            return visited_order

        path = bfs(G, start_node) if algo == "BFS" else dfs(G, start_node)
        st.success(f"{algo} 遍历顺序：{path}")
        fig = plot_graph(G, highlight_path=path)
        st.plotly_chart(fig, use_container_width=True)
    else:
        fig = plot_graph(G)
        st.plotly_chart(fig, use_container_width=True)
