import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
import streamlit as st

# --- Streamlit 페이지 설정 ---
st.set_page_config(page_title="Crystal Shard Poster", page_icon="💎", layout="centered")

st.title("Crystal Shard Poster Generator")

# --- 사이드바 설정 (옵션 조절) ---
st.sidebar.header("Poster Settings")
n_points = st.sidebar.slider("Shard Density (Points):", min_value=30, max_value=150, value=90, step=10)
seed_input = st.sidebar.number_input("Seed (0 for random):", min_value=0, max_value=9999, value=42)

# 시드값 처리
seed = None if seed_input == 0 else int(seed_input)

# --- 포스터 생성 함수 ---
def generate_crystal_shard_poster(n_points=90, seed=None):
    if seed is not None:
        np.random.seed(seed)

    fig, ax = plt.subplots(figsize=(8, 11))
    bg_color = "#0B0B10"
    fig.patch.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)

    # 무작위 포인트 생성
    x = np.random.uniform(-1.5, 1.5, n_points)
    y = np.random.uniform(-2.2, 2.2, n_points)

    # 캔버스 모서리 외곽 포인트 추가
    borders = np.array([
        [-1.5, -2.2], [1.5, -2.2], [-1.5, 2.2], [1.5, 2.2],
        [0, -2.2], [0, 2.2], [-1.5, 0], [1.5, 0],
        [-1.5, -1.1], [1.5, -1.1], [-1.5, 1.1], [1.5, 1.1]
    ])
    points = np.vstack([np.column_stack([x, y]), borders])

    # 델로네 삼각분할 적용
    tri = Delaunay(points)

    def get_shard_color(cx, cy):
        dist = np.sqrt(cx**2 + cy**2)
        if dist < 0.7:
            colors = ["#FF007F", "#7928ca", "#00f0ff"] # 중심부 네온 핫스팟
        elif dist < 1.4:
            colors = ["#3867D6", "#00FFCC", "#8A2BE2"] # 중간부 일렉트릭 블루/민트
        else:
            colors = ["#FF4500", "#FFD700", "#1E1E24"] # 외곽부 앰버/딥 다크
        return np.random.choice(colors)

    for tri_indices in tri.simplices:
        pts = points[tri_indices]
        cx = np.mean(pts[:, 0])
        cy = np.mean(pts[:, 1])

        color = get_shard_color(cx, cy)
        alpha = np.random.uniform(0.35, 0.8)

        ax.fill(pts[:, 0], pts[:, 1], color=color, alpha=alpha, edgecolor='#12121A', linewidth=0.9)

    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-2.2, 2.2)
    ax.axis('off')

    plt.tight_layout()
    plt.close(fig) # 중복 출력 방지
    return fig

# --- 포스터 생성 및 화면 출력 ---
with st.spinner("크리스탈 조각을 생성하는 중입니다..."):
    poster_fig = generate_crystal_shard_poster(n_points=n_points, seed=seed)
    st.pyplot(poster_fig)
