import streamlit as st
import random

def ai_consultation_page(get_jobs):
    st.title("🤖 Konsultasi AI: Temukan Pekerjaan Cocok untukmu")

    st.write("""
    Masukkan preferensi atau minat kamu, kemudian AI akan memberikan rekomendasi pekerjaan yang cocok.
    """)

    user_input = st.text_area("Ceritakan minat, skill, atau bidang pekerjaan yang kamu suka:")

    if st.button("Cari Rekomendasi Pekerjaan"):
        if not user_input.strip():
            st.warning("Tuliskan sedikit tentang minat atau skill kamu terlebih dahulu.")
            return

        st.info("AI sedang menganalisis...")

        df_jobs = get_jobs()

        user_keywords = [kw.lower() for kw in user_input.split()]

        recommended_jobs = []
        for _, job in df_jobs.iterrows():
            job_title_lower = job['Posisi'].lower()
            if any(kw in job_title_lower for kw in user_keywords):
                recommended_jobs.append(job)

        if not recommended_jobs:
            recommended_jobs = df_jobs.sample(min(3, len(df_jobs))).to_dict('records')
        else:
            recommended_jobs = [job.to_dict() for job in recommended_jobs]

        st.subheader("💼 Rekomendasi Pekerjaan untukmu:")
        for job in recommended_jobs:
            st.markdown(f"**{job['Posisi']}** di {job['Perusahaan']}")
            st.markdown(f"- Lokasi: {job['Lokasi']}")
            st.markdown(f"- Gaji: {job['Gaji_Num']} juta")
            st.markdown(f"- Tanggal Posting: {job['Tanggal Posting']}")
            st.markdown("---")
