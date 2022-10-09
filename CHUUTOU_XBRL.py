# -*- coding: utf-8 -*-
"""
Created on Sat Jul 16 14:21:05 2022

@author: pccnf
"""
#chrome driverはコマンドプロンプトからpip install chromedriver-binary-autoでインストール
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select#スクレイピングでドロップダウンリストを使う時の定義
import time
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_binary#Chromedriverへのパスを通す

#ブラウザを立ち上げないで処理するヘッドレスモード
#options = Options()
#options.add_argument('--headless') 


#ダウンロード先をこのスクリプトがあるフォルダにする
iDir = os.getcwd()+ "\\ダウンロードファイル"#「ダウンロードファイル」フォルダを指定

options = webdriver.ChromeOptions()
options.add_experimental_option("prefs", {"download.default_directory": iDir})

chromedriver = 'chromedriver.exe'
browser = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)
browser.implicitly_wait(300)#find_elementで要素が見つかるまで最大300秒待機する

browser.get('https://www.release.tdnet.info/inbs/I_main_00.html')
time.sleep(3)


#ドロップダウンをクリックして開示日を選択する
#この部分はiframeになっていないので普通に要素を取得していく
elem_table= browser.find_element_by_id('day-selector')
elem_table.click()

#リストから特定の日付を選択
#from selenium.webdriver.support.select import Select

#dropdown = browser.find_element_by_id('day-selector')
#select = Select(dropdown)
 
#select.select_by_value('I_list_001_20220715.html')


#リストから●番目のものを選択
from selenium.webdriver.support.select import Select

dropdown = browser.find_element_by_id('day-selector')
select = Select(dropdown)
 
select.select_by_index(2)  # 9番目のoptionタグを選択状態に（本日が7/16（土）なので7/8（金）が選択される）
#select.select_by_index(len(select.options)-1)  # 最後のoptionタグを選択状態に

def getXBRLfile():#下記の一連の流れを「getXBRLfile」と定義する
    #短信のXBRLファイルだけをダウンロードしてファイルの名前を会社名に変更
    #from selenium import webdriver
    #from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import Select#スクレイピングでドロップダウンリストを使う時の定義
    import time
    import os
    import datetime
    now = datetime.datetime.now()#本日の日付を取得してnowに入れる
    
    #download_path = iDir2#os.getenv("HOMEDRIVE") + os.getenv("HOMEPATH") + "\\Downloads"
    #download_path
    
    #iframeの操作
    iframe = browser.find_element_by_id("main_list")#iframeを特定
    browser.switch_to.frame(iframe)#親フレームからiframeに移動
    
    
    #ページのなかの４つ目の表が各社の情報の入った表（テーブル）となっている
    elem_tables= browser.find_elements_by_tag_name("tbody")
    elem_tables[3].text
    
        
    #1ページの表の中にtr（行）が最大100個（100行）入る
    elem_Companys = elem_tables[3].find_elements_by_tag_name("tr")
    Looptimes = len(elem_Companys) - 1
    
    #j番目の行の要素を取ってくる
    j = 0
    elem_CompanyInfos = elem_Companys[j].find_elements_by_tag_name("td")
    
    CHUUTOU = ['67520','65010','67020','65020','65030','67010','67530','65040','69810','67030','65060','65080']
    #KAKUCHUUTOU = ['66410','65070','65160','66220','66170','69240','79510','66450','49020','67040','97190','52140','67070','66520','67980','68040','67630','68260','67230','68570']
    
    #１行ずつ順番に
    for elem_Company in elem_Companys:
        for i in range(0,7):#0番目から6番目（7の一つ手前）まで
        
    
            if elem_CompanyInfos[4].text =="" or elem_CompanyInfos[1].text not in CHUUTOU:#XBRLファイルがなかったら、または証券番号がリストにはいっていなければスルー
                pass
            else:       
                #XBRLファイルがあり、PDFファイルの名前に「短信」が含まれていなかったら,または「訂正」が含まれていたら、またはDENKIリストの証券番号に入っていなかったらスルー
                if "短信" not in elem_CompanyInfos[3].text or "訂正" in elem_CompanyInfos[3].text: 
                    pass
                
                else:#短信のXBRLファイルをダウンロード
                                  
                    if i ==1:
                        code = elem_CompanyInfos[i].text
                        print(code)
                        
                    elif i ==2:
                        name = elem_CompanyInfos[i].text
                        print(name)
                        
                    elif i ==4:
                        elem_CompanyInfos[i].click()
                        time.sleep(3)
                        
                        #ダウンロードフォルダにあるzipファイルのうち、最も新しいものを取得
                        from glob import glob
                        files=glob(iDir+"/*.zip")
    
                        #カレントディレクトリの場所を取得する
                        import os
                        #ダウンロードフォルダの中のCSVファイルを更新日時（時系列）に並べて、最も新しいファイルを取得
                        sorted_files=sorted(files, key=os.path.getmtime)
                        downloadfile=sorted_files[-1]
                        
                        downloadfile_name = os.path.basename(downloadfile)
                        #print(downloadfile_name)
                        
                        just_downloadfile_name = os.path.splitext(os.path.basename(downloadfile))[0]
                        #print(just_downloadfile_name)
                        
     
                        # 変更前ファイル
                        path1 = downloadfile
     
                        # 変更後ファイル
                        path2= iDir + "\\1_" + name +"_"+now.strftime("%m%d%H%M")+ ".zip"
     
                        # ファイル名の変更 
                        os.rename(path1, path2)  
                        # ファイルの存在確認 
                        #print(os.path.exists(path2))
                        
                    else:
                        pass
                    
        time.sleep(1)           
        if j != Looptimes:
            j += 1
            
        #取得が終わったら次の行に移る
        elem_CompanyInfos = elem_Companys[j].find_elements_by_tag_name("td")
        time.sleep(1)
        
    browser.switch_to.default_content()#iframeから戻る
    
getXBRLfile()#定義した関数を実行


# 次へをクリックしページ遷移する
#iframe = browser.find_element_by_id("main_list")#iframeを特定
#browser.switch_to.frame(iframe)#親フレームからiframeに移動

while True:#「次へ」ボタンがあれば押して次のページへ。なければ処理を終わらせる
  try:
    iframe = browser.find_element_by_id("main_list")#iframeを特定
    browser.switch_to.frame(iframe)#親フレームからiframeに移動
    
    next_btn = browser.find_element(By.CLASS_NAME, "pager-R")
    next_btn.click()
    browser.implicitly_wait(300)#find_elementで要素が見つかるまで最大300秒待機する
    browser.switch_to.default_content()#iframeから戻る
   
    getXBRLfile()
    
  except Exception:#exceptで例外型を指定する際に使う（Python逆引き大全P120）
    break#breakはループを抜ける処理
    
#browser.switch_to.default_content()
time.sleep(3)

browser.quit()