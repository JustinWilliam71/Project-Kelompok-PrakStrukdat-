import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta
import math # <--- Tambahkan ini untuk perhitungan pagination
# Import semua fungsi dari file terpisah
from database import get_db_connection
from Sign_In import auth_page
from beranda import home_page
from cari_kerja import search_jobs_page
from profile import profile_page


# ==========================================
# 1. KONFIGURASI APLIKASI & CSS
# ==========================================
st.set_page_config(
    page_title="Getcareer - Platform Karier Terbaik",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {font-size: 2.5rem; color: #00B14F; font-weight: 700;}
    .stButton>button {
        background-color: #00B14F;
        color: white;
        border-radius: 8px; 
        font-weight: bold;
        padding: 10px;
        width: 100%;
    }
    .stButton>button:hover {background-color: #008f40; color: white;}
    .stContainer {
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        padding: 20px;
        margin-bottom: 15px;
    }
    .centered-content {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
    }
    .big-icon { font-size: 80px; color: #00B14F; margin-bottom: 20px; }
</style>
""", unsafe_allow_html=True)


# ==========================================
# 2. SESSION STATE
# ==========================================
def init_session_state():
    defaults = {
        'logged_in': False,
        'user_role': None,
        'username': "",
        'auth_mode': 'login', 
        'current_page': 'Home',
        'profile_pic_preview': None,
        # --- TAMBAHKAN INI ---
        'search_page': 1 # Halaman awal untuk pencarian
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# ==========================================
# 3. GENERATOR DATA DUMMY
# ==========================================
@st.cache_data
def get_jobs():
    """Menghasilkan DataFrame data lowongan kerja dummy."""
    data = []
    companies = ['Gojek', 'Tokopedia', 'Shopee', 'Traveloka', 'Grab', 'Bank BCA', 'Pertamina', 'Telkomsel']
    roles = ['Data Analyst', 'Software Engineer', 'Product Manager', 'UI/UX Designer', 'Digital Marketing', 'HR Manager']
    
    for i in range(30):
        gaji_int = random.randint(6, 35) # Gaji dalam juta
        data.append({
            "ID": i + 1,
            "Posisi": random.choice(roles),
            "Perusahaan": random.choice(companies),
            "Gaji_Num": gaji_int,
            "Lokasi": random.choice(['Jakarta', 'Remote', 'Bandung', 'Surabaya', 'Bali']),
            "Tanggal Posting": (datetime.now() - timedelta(days=random.randint(1, 20))).strftime("%Y-%m-%d")
        })
    return pd.DataFrame(data)


# ==========================================
# 4. NAVIGASI UTAMA
# ==========================================
def main():
    """Fungsi utama yang mengontrol alur aplikasi."""
    if st.session_state['logged_in']:
        st.sidebar.title("Menu Navigasi")
        
        # --- MODE ADMIN ---
        if st.session_state['user_role'] == 'admin':
            st.sidebar.warning("🔧 Mode Admin")
            page = st.sidebar.selectbox("Pilih Halaman", ["Beranda", "Database User"])
            
            if page == "Beranda": 
                home_page()
            elif page == "Database User": 
                st.title("Database Pengguna")
                st.dataframe(pd.read_sql("SELECT * FROM userdata", get_db_connection()), use_container_width=True)
                
        # --- MODE USER BIASA ---
        else:
            menu_dict = {"Home": "🏠 Beranda", "SearchJobs": "🔍 Cari Kerja", "Profile": "👤 Profil Saya"}
            selected = st.sidebar.radio("Ke Halaman:", list(menu_dict.keys()), format_func=lambda x: menu_dict[x])
            st.session_state['current_page'] = selected
            st.sidebar.markdown("---")
            
            if st.sidebar.button("🚪 Keluar Aplikasi"):
                st.session_state['logged_in'] = False
                st.session_state['current_page'] = 'Home'
                # Reset semua state saat logout
                st.session_state['profile_pic_preview'] = None
                st.session_state['search_page'] = 1
                st.session_state['search_term'] = ""
                st.session_state['location_filter'] = "Semua"
                st.rerun()

            # Panggil halaman dari file lain
            if st.session_state['current_page'] == 'Home': 
                home_page()
            elif st.session_state['current_page'] == 'SearchJobs': 
                # Meneruskan fungsi get_jobs dan nomor halaman saat ini
                search_jobs_page(get_jobs, st.session_state['search_page'])
            elif st.session_state['current_page'] == 'Profile': 
                profile_page()
    else:
        # Jika belum login, tampilkan halaman autentikasi
        auth_page()

if __name__ == '__main__':
    main()
