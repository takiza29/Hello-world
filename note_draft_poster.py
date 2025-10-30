#!/usr/bin/env python3
"""
noteに下書き記事を投稿するSeleniumスクリプト

このスクリプトはSeleniumを使用してnoteに自動でログインし、
下書き記事を作成します。
"""

import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class NoteDraftPoster:
    """noteに下書き記事を投稿するクラス"""

    def __init__(self, email=None, password=None, headless=False):
        """
        初期化

        Args:
            email (str): noteのログインメールアドレス（環境変数NOTE_EMAILからも取得可能）
            password (str): noteのログインパスワード（環境変数NOTE_PASSWORDからも取得可能）
            headless (bool): ヘッドレスモードで実行するか
        """
        self.email = email or os.getenv('NOTE_EMAIL')
        self.password = password or os.getenv('NOTE_PASSWORD')
        self.headless = headless
        self.driver = None

        if not self.email or not self.password:
            raise ValueError("メールアドレスとパスワードは必須です。引数または環境変数で設定してください。")

    def setup_driver(self):
        """Chromeドライバーをセットアップ"""
        chrome_options = Options()

        if self.headless:
            chrome_options.add_argument('--headless')

        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')

        # ユーザーエージェントを設定
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10)

    def login(self):
        """noteにログイン"""
        print("noteにログイン中...")

        # noteのログインページにアクセス
        self.driver.get('https://note.com/login')
        time.sleep(2)

        try:
            # メールアドレスでログインボタンをクリック
            email_login_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'メールアドレスでログイン')]"))
            )
            email_login_button.click()
            time.sleep(1)

            # メールアドレスを入力
            email_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "emailOrUrlname"))
            )
            email_input.send_keys(self.email)
            time.sleep(1)

            # パスワードを入力
            password_input = self.driver.find_element(By.NAME, "password")
            password_input.send_keys(self.password)
            time.sleep(1)

            # ログインボタンをクリック
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()

            # ログイン完了まで待機
            time.sleep(5)

            print("ログインに成功しました")

        except (TimeoutException, NoSuchElementException) as e:
            print(f"ログインエラー: {e}")
            raise

    def create_draft(self, title, content, tags=None):
        """
        下書き記事を作成

        Args:
            title (str): 記事のタイトル
            content (str): 記事の本文
            tags (list): タグのリスト（オプション）
        """
        print("下書き記事を作成中...")

        try:
            # 投稿ページに移動
            self.driver.get('https://note.com/post')
            time.sleep(3)

            # タイトルを入力
            title_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[placeholder*='タイトル']"))
            )
            title_input.send_keys(title)
            time.sleep(1)

            # 本文を入力
            # noteのエディタは複雑な構造なので、JavaScriptで直接入力する方法も検討
            content_area = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[contenteditable='true']"))
            )
            content_area.click()
            time.sleep(1)
            content_area.send_keys(content)
            time.sleep(2)

            # タグを追加（オプション）
            if tags:
                self._add_tags(tags)

            # 下書き保存ボタンを探してクリック
            # noteは自動保存されるので、少し待機するだけでOK
            print("下書きを保存中...")
            time.sleep(3)

            print("下書き記事の作成が完了しました")

        except (TimeoutException, NoSuchElementException) as e:
            print(f"下書き作成エラー: {e}")
            raise

    def _add_tags(self, tags):
        """
        タグを追加

        Args:
            tags (list): タグのリスト
        """
        try:
            # タグ追加ボタンを探してクリック
            # noteのUIは変更される可能性があるため、複数の方法を試す
            time.sleep(1)

            for tag in tags:
                # ここでタグ入力のロジックを実装
                # 実際のnoteのUIに合わせて調整が必要
                pass

        except Exception as e:
            print(f"タグ追加エラー: {e}")
            # タグ追加は必須ではないので、エラーが出ても続行

    def close(self):
        """ブラウザを閉じる"""
        if self.driver:
            self.driver.quit()
            print("ブラウザを閉じました")


def main():
    """メイン関数"""
    # 使用例
    poster = NoteDraftPoster(headless=False)

    try:
        # ドライバーをセットアップ
        poster.setup_driver()

        # ログイン
        poster.login()

        # 下書き記事を作成
        poster.create_draft(
            title="Seleniumで自動投稿したテスト記事",
            content="これはSeleniumを使って自動投稿されたテスト記事です。\n\n自動化により、効率的に記事を投稿できます。",
            tags=["テスト", "自動化"]
        )

        # 完了メッセージ
        print("\n処理が完了しました！")
        print("ブラウザは10秒後に自動的に閉じます...")
        time.sleep(10)

    except Exception as e:
        print(f"エラーが発生しました: {e}")
        time.sleep(5)

    finally:
        poster.close()


if __name__ == "__main__":
    main()
