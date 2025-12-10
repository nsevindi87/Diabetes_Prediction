Tamamlanan Proje. 
 verilerin olusturuldugu bir PKL dosyasi olusturuluyor. 
 Main.py ile sorgu yapabilen bir sistem kuruldu.
 App.py dosyasi ile streamlit ui ile model kullanilabiliyor.
 test_diabets_api ile de calisan api kullanilarak modelden(yani olusturulan pkl den) veri cekiliyor.

cd Diabetes
python3 -m venv venv
source .venv/bin/activate
pip install -r requirements.txt
cd src
python main.py (api olarak)
streamlit run app.py (ui)
test icinde test_diabetes_api.ipynb kullan
