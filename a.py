from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import glob
from dotenv import load_dotenv

load_dotenv()

# 環境変数から取得
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
SELENIUM_HOST = os.getenv("SELENIUM_HOST", "selenium")  # fallback to "selenium"
# DOWNLOAD_DIR = "/home/seluser/Downloads" #Downloadsフォルダにseluserの書き込み権限がないので出力できない
DOWNLOAD_DIR = "/home/seluser"

# Chromeオプション
options = Options()
options.add_experimental_option("prefs", {
    "download.default_directory": DOWNLOAD_DIR,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--headless=new")

# Selenium Remote WebDriver に接続
driver = webdriver.Remote(
    command_executor=f"http://{SELENIUM_HOST}:4444/wd/hub",
    options=options
)

try:
    print("🌐 SSOログインページにアクセス...")
    # login_start_url = "https://sso.fun.ac.jp/my.policy"
    login_start_url = "https://hope.fun.ac.jp/local/hope/login.php"
    export_url = "https://hope.fun.ac.jp/grade/export/txt/index.php?id=2059"

    driver.get(login_start_url)

    # 「未来大の学生・教職員」リンクをクリック（テキストで探す方法）
    print("⌛ hopeへ移動->「未来大の学生・教職員」をクリックします")
    fun_link = driver.find_element(By.LINK_TEXT, "未来大の学生・教職員 FUN Students & Staff")
    fun_link.click()

    print("⌛ usernameフィールドを待機中...")
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.NAME, "username")))

    driver.find_element(By.NAME, "username").send_keys(USERNAME)
    driver.find_element(By.NAME, "password").send_keys(PASSWORD)
    driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

    WebDriverWait(driver, 15).until(EC.url_changes(login_start_url))

    print("✅ ログイン成功！エクスポートページへ移動中...")
    driver.get(export_url)
    # driver.save_screenshot("sso_page.png")

    download_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "id_submitbutton")))
    time.sleep(2)  # ページが落ち着くまで少し待つ
    download_button.click()

    print("⬇️ ダウンロード中...（5秒待機）")
    downloaded_files = glob.glob(DOWNLOAD_DIR)
    if downloaded_files:
        print("✅ CSVファイルが見つかりました！", downloaded_files)
    else:
        print("⚠️ CSVファイルが見つかりませんでした")

    print("✅ ダウンロード完了（たぶん）")

finally:
    driver.quit()
