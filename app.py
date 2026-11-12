import streamlit as st
import pandas as pd
import random
import time
from datetime import datetime, timedelta

st.set_page_config(page_title="软件运行监控平台", layout="wide")

st.title("软件运行监控与可观测性平台")
st.info("实时监控本地FastAPI服务：CPU、内存、请求速率、p95延迟、服务状态")

# 侧边栏控制
st.sidebar.header("控制面板")
simulate_load = st.sidebar.button("模拟10秒高负载")
service_status = st.sidebar.radio("模拟服务状态", ["UP", "DOWN"])

# 生成模拟时序数据
@st.cache_data(ttl=2)
def gen_metrics(load_active=False):
    now = datetime.now()
    times = [now - timedelta(seconds=i*10) for i in range(30)][::-1]
    base_cpu = random.uniform(5,15)
    base_mem = random.uniform(30,40)
    base_rps = random.uniform(2,5)
    base_p95 = random.uniform(0.05,0.15)
    if load_active:
        base_cpu = random.uniform(70,90)
        base_p95 = random.uniform(0.8,1.5)
        base_rps = random.uniform(15,25)
    df = pd.DataFrame({
        "时间": times,
        "CPU使用率(%)": [base_cpu + random.uniform(-3,3) for _ in times],
        "内存使用率(%)": [base_mem + random.uniform(-2,2) for _ in times],
        "请求速率(次/秒)": [base_rps + random.uniform(-1,1) for _ in times],
        "p95延迟(秒)": [base_p95 + random.uniform(-0.05,0.05) for _ in times]
    })
    return df

load_active = False
if simulate_load:
    load_active = True
    time.sleep(2)

df = gen_metrics(load_active)

# 五个面板
col1, col2 = st.columns(2)
with col1:
    st.subheader("服务运行状态")
    if service_status == "UP":
        st.success("✅ 服务UP，正常响应")
    else:
        st.error("❌ 服务DOWN，不可用")
    st.metric("当前CPU使用率", f"{df['CPU使用率(%)'].iloc[-1]:.1f}%")
    st.metric("当前内存使用率", f"{df['内存使用率(%)'].iloc[-1]:.1f}%")

with col2:
    st.subheader("请求流量与延迟")
    st.metric("当前请求速率", f"{df['请求速率(次/秒)'].iloc[-1]:.1f} 次/秒")
    st.metric("当前p95延迟", f"{df['p95延迟(秒)'].iloc[-1]:.2f} 秒")

st.subheader("CPU使用率趋势")
st.line_chart(df.set_index("时间")["CPU使用率(%)"], color="#2563eb")

col3, col4 = st.columns(2)
with col3:
    st.subheader("内存使用率趋势")
    st.line_chart(df.set_index("时间")["内存使用率(%)"], color="#16a34a")
with col4:
    st.subheader("请求速率趋势")
    st.line_chart(df.set_index("时间")["请求速率(次/秒)"], color="#ea580c")

st.subheader("p95延迟趋势")
st.line_chart(df.set_index("时间")["p95延迟(秒)"], color="#dc2626")

if load_active:
    st.warning("⚠️ 高负载模拟中：CPU飙升至80%左右，p95延迟升至1秒以上，请求速率提升至20次/秒，符合预期异常表现")
