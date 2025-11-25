import altair as alt
import pandas as pd
import streamlit as st

def home_page():
    """Halaman Beranda untuk pengguna yang sudah login."""
    st.markdown(
        f"<h1 class='main-header'>Temukan Pekerjaan Impianmu dengan Mudah {st.session_state['username']}</h1>", 
        unsafe_allow_html=True
    )
    st.write("Jelajahi ribuan lowongan, temukan role yang cocok, dan pantau tren pekerjaan terbaru.")

    st.markdown("---")

    data_jobs = pd.DataFrame({
        "Pekerjaan": [
            "Software Engineer", "Data Analyst", "UI/UX Designer", "Product Manager",
            "Mobile Developer", "Backend Developer", "Frontend Developer",
            "Digital Marketer", "IT Support", "Cyber Security"
        ],
        "Peminat": [520, 440, 310, 260, 390, 420, 360, 380, 290, 340]
    })

    data_industri = pd.DataFrame({
        "Industri": ["Teknologi", "Finance", "Retail", "Kesehatan", "Logistik", "Startup"],
        "Lowongan": [830, 420, 260, 310, 210, 540]
    })

    data_growth = pd.DataFrame({
        "Minggu": ["M1", "M2", "M3", "M4", "M5"],
        "Jumlah": [120, 160, 210, 260, 310]
    })

    data_salary = pd.DataFrame({
        "Role": ["Backend Dev", "Frontend Dev", "Data Analyst", "UI/UX", "Cyber Security"],
        "Gaji (Juta)": [15, 14, 13, 11, 17]
    })

    st.subheader("10 Pekerjaan yang Paling Diminati")

    chart_jobs = (
        alt.Chart(data_jobs)
        .mark_bar()
        .encode(
            x=alt.X("Pekerjaan", sort="-y"),
            y="Peminat",
            tooltip=["Pekerjaan", "Peminat"],
            color=alt.Color("Pekerjaan", legend=None)
        )
        .properties(width="container", height=350)
    )
    st.altair_chart(chart_jobs, use_container_width=True)

    st.markdown("---")

    st.subheader("Industri dengan Lowongan Terbanyak")

    chart_industri = (
        alt.Chart(data_industri)
        .mark_bar()
        .encode(
            x=alt.X("Industri", sort="-y"),
            y="Lowongan",
            tooltip=["Industri", "Lowongan"],
            color=alt.Color("Industri", legend=None)
        )
        .properties(width="container", height=300)
    )
    st.altair_chart(chart_industri, use_container_width=True)

    st.markdown("---")

    st.subheader("Pertumbuhan Lowongan per Minggu")

    chart_growth = (
        alt.Chart(data_growth)
        .mark_line(point=True)
        .encode(
            x="Minggu",
            y="Jumlah",
            tooltip=["Minggu", "Jumlah"],
        )
        .properties(width="container", height=300)
    )
    st.altair_chart(chart_growth, use_container_width=True)

    st.markdown("---")

    st.subheader("Rata-Rata Gaji per pekerjaan")

    chart_salary = (
        alt.Chart(data_salary)
        .mark_bar()
        .encode(
            x=alt.X("Role", sort="-y"),
            y="Gaji (Juta)",
            tooltip=["Role", "Gaji (Juta)"],
            color=alt.Color("Role", legend=None)
        )
        .properties(width="container", height=300)
    )
    st.altair_chart(chart_salary, use_container_width=True)

    st.markdown("---")

