# =============================================================================
#  CREAT TABLE
# =============================================================================

import pymysql
#連線db4free
conn = pymysql.connect(host='db4free.net',port=3306,db='moviebox1',user='jimlyttt',passwd='jimlyt0713')
cur = conn.cursor()
print("CREATE TABLE NOW...")

#執行mysql語法 '若資料表存在則刪除之'
cur.execute("DROP TABLE IF EXISTS rc_circuits")
#建立資料表
sql = """CREATE TABLE rc_circuits (
  DATA_ID INT AUTO_INCREMENT,
  區域 VARCHAR(16),
  店名 VARCHAR(64),
  地址 VARCHAR(128),
  電話 VARCHAR(16),
  營業時間 VARCHAR(128),
  公休日 VARCHAR(128),
  備註 VARCHAR(256),
  on_road VARCHAR(2),
  off_road VARCHAR(2),
  電房 VARCHAR(2),
  油房 VARCHAR(2),
  飄移 VARCHAR(2),
  mini_z VARCHAR(2),
  PRIMARY KEY (DATA_ID)
)"""

cur.execute(sql)
print("CREATE TABLE OK")
# =============================================================================
# 
# =============================================================================
from selenium import webdriver
driver = webdriver.Chrome('chromedriver')
url='https://rccar-navi.com/'
driver.get(url)
area_count_list=[7,6,7,4,6,5,4,8] #左上方每一層連結數量
data=['none','none','none','none','none','none','none','none','none','none','none','none','none'] #預設待寫入資料為none
plus=0
error_count=0
error_list=[]
#點擊畫面左上方區域連結
count=1
for i in range(1,9):
    for j in range(1,area_count_list[i-1]+1):
        driver.find_element_by_css_selector('#sidebar > div:nth-child(1) > ul > li:nth-child(%d) > a:nth-child(%d)'%(i,j)).click()
        city=driver.find_element_by_css_selector('#sidebar > div:nth-child(1) > ul > li:nth-child(%d) > a:nth-child(%d)'%(i,j)).text                                     
#因單頁車場數量若>5 資料分割為二區，故判斷資料數量,並分成兩種寫法
        circuits_count=len(driver.find_elements_by_css_selector('#content > div.blog > div:nth-child(2) > div > dl > dt> a'))
        if circuits_count > 5:
            for click_1 in range(1,6):#點擊上半部連結
                #check
                check_url_1=driver.current_url
                driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[1]/div/dl[1]/dt[%d]/a'%click_1).click()
                while driver.current_url==check_url_1:
                    driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[1]/div/dl[1]/dt[%d]/a'%click_1).click()
                else:                    
                    '''
                    爬
                    '''
                    #擷取網頁第一個表格內容 依序代入data list
                    a=driver.find_elements_by_css_selector('#entry_box > table > tbody > tr > th')
                    plus=0
                    #預設待寫入內容'data list'為none
                    data=['none','none','none','none','none','none','none','none','none','none','none','none','none']
                    for l in a:
                        if l.text=='住所':
                            data[2]=driver.find_element_by_css_selector('#entry_box > table > tbody > tr:nth-child(%d) > td'%(plus+1)).text
                            plus+=1
                        elif l.text=='電話':
                            data[3]=driver.find_element_by_css_selector('#entry_box > table > tbody > tr:nth-child(%d) > td'%(plus+1)).text
                            plus+=1
                        elif l.text=='営業時間':
                            data[4]=driver.find_element_by_css_selector('#entry_box > table > tbody > tr:nth-child(%d) > td'%(plus+1)).text
                            plus+=1
                        elif l.text=='定休日':
                            data[5]=driver.find_element_by_css_selector('#entry_box > table > tbody > tr:nth-child(%d) > td'%(plus+1)).text
                            plus+=1
                        else:
                            data[6]=driver.find_element_by_xpath('//*[@id="entry_box"]/table/tbody/tr[%d]/td/a'%(plus+1)).get_attribute('href')
                            plus+=1
                    data[0]=city
                    data[1]=driver.find_element_by_css_selector('#content > div.blog > h2').text        
                    
                    b=driver.find_elements_by_css_selector('#content > div.blog > div:nth-child(3) > div.designTable > table > tbody > tr:nth-child(2) > td > div')
                    plus=7
                    for p in b:
                        data[plus]=p.text
                        plus+=1
                    print(data)
                    #寫入DB
                    try:
                        sql_insert = r"insert into rc_circuits(區域,店名,地址,電話,營業時間,公休日,備註,on_road,off_road,電房,油房,飄移,mini_z) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"\
                        %(data[0],data[1].replace("'", ""),data[2],data[3],data[4],data[5],data[6].replace("'", ""),data[7],data[8],data[9],data[10],data[11],data[12])
                        cur.execute(sql_insert)
                        conn.commit()
                        pass
                    except:
                        print('error')
                        error_count+=1
                        error_list.append(data)
                #點擊回到當前區域頁面
                driver.find_element_by_css_selector('#sidebar > div:nth-child(1) > ul > li:nth-child(%d) > a:nth-child(%d)'%(i,j)).click()           
            for click_2 in range(1,circuits_count-4):#點擊下半部連結
                #check
                check_url_1=driver.current_url
                driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[1]/div/dl[2]/dt[%d]/a'%click_2).click()
                while driver.current_url==check_url_1:
                    driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[1]/div/dl[2]/dt[%d]/a'%click_2).click()
                else:                
                    '''
                    爬
                    '''
                    a=driver.find_elements_by_css_selector('#entry_box > table > tbody > tr > th')
                    plus=0
                    data=['none','none','none','none','none','none','none','none','none','none','none','none','none']
                    for m in a:
                        if m.text=='住所':
                            data[2]=driver.find_element_by_css_selector('#entry_box > table > tbody > tr:nth-child(%d) > td'%(plus+1)).text
                            plus+=1
                        elif m.text=='電話':
                            data[3]=driver.find_element_by_css_selector('#entry_box > table > tbody > tr:nth-child(%d) > td'%(plus+1)).text
                            plus+=1
                        elif m.text=='営業時間':
                            data[4]=driver.find_element_by_css_selector('#entry_box > table > tbody > tr:nth-child(%d) > td'%(plus+1)).text
                            plus+=1
                        elif m.text=='定休日':
                            data[5]=driver.find_element_by_css_selector('#entry_box > table > tbody > tr:nth-child(%d) > td'%(plus+1)).text
                            plus+=1
                        else:
                            data[6]=driver.find_element_by_xpath('//*[@id="entry_box"]/table/tbody/tr[%d]/td/a'%(plus+1)).get_attribute('href')
                            plus+=1
                    data[0]=city
                    data[1]=driver.find_element_by_css_selector('#content > div.blog > h2').text        
                    
                    b=driver.find_elements_by_css_selector('#content > div.blog > div:nth-child(3) > div.designTable > table > tbody > tr:nth-child(2) > td > div')
                    plus=7
                    for q in b:
                        data[plus]=q.text
                        plus+=1
                    print(data)
                    #寫入DB
                    try:
                        sql_insert = r"insert into rc_circuits(區域,店名,地址,電話,營業時間,公休日,備註,on_road,off_road,電房,油房,飄移,mini_z) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"\
                        %(data[0],data[1].replace("'", ""),data[2],data[3],data[4],data[5],data[6].replace("'", ""),data[7],data[8],data[9],data[10],data[11],data[12])
                        cur.execute(sql_insert)
                        conn.commit()
                        pass
                    except:
                        print('error')
                        error_count+=1
                        error_list.append(data)                                 
                #點擊回到當前區域頁面
                driver.find_element_by_css_selector('#sidebar > div:nth-child(1) > ul > li:nth-child(%d) > a:nth-child(%d)'%(i,j)).click()                               
        else:
            for click_3 in range(1,circuits_count+1):#點擊連結
                #check
                check_url_1=driver.current_url
                driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[1]/div/dl[1]/dt[%d]/a'%click_3).click()
                while driver.current_url==check_url_1:
                    driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[1]/div/dl[1]/dt[%d]/a'%click_3).click()
                else:
                    '''
                    爬
                    '''
                    a=driver.find_elements_by_css_selector('#entry_box > table > tbody > tr > th')
                    plus=0
                    data=['none','none','none','none','none','none','none','none','none','none','none','none','none']                                       
                    for n in a:
                        if n.text=='住所':
                            data[2]=driver.find_element_by_css_selector('#entry_box > table > tbody > tr:nth-child(%d) > td'%(plus+1)).text
                            plus+=1
                        elif n.text=='電話':
                            data[3]=driver.find_element_by_css_selector('#entry_box > table > tbody > tr:nth-child(%d) > td'%(plus+1)).text
                            plus+=1
                        elif n.text=='営業時間':
                            data[4]=driver.find_element_by_css_selector('#entry_box > table > tbody > tr:nth-child(%d) > td'%(plus+1)).text
                            plus+=1
                        elif n.text=='定休日':
                            data[5]=driver.find_element_by_css_selector('#entry_box > table > tbody > tr:nth-child(%d) > td'%(plus+1)).text
                            plus+=1
                        else:
                            data[6]=driver.find_element_by_xpath('//*[@id="entry_box"]/table/tbody/tr[%d]/td/a'%(plus+1)).get_attribute('href')
                            plus+=1
                    data[0]=city
                    data[1]=driver.find_element_by_css_selector('#content > div.blog > h2').text        
                    
                    b=driver.find_elements_by_css_selector('#content > div.blog > div:nth-child(3) > div.designTable > table > tbody > tr:nth-child(2) > td > div')
                    plus=7
                    for r in b:
                        data[plus]=r.text
                        plus+=1
                    print(data)
                    #寫入DB
                    try:
                        sql_insert = r"insert into rc_circuits(區域,店名,地址,電話,營業時間,公休日,備註,on_road,off_road,電房,油房,飄移,mini_z) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"\
                        %(data[0],data[1].replace("'", ""),data[2],data[3],data[4],data[5],data[6].replace("'", ""),data[7],data[8],data[9],data[10],data[11],data[12])
                        cur.execute(sql_insert)
                        conn.commit()
                        pass
                    except:
                        print('error')
                        error_count+=1
                        error_list.append(data)
                #點擊回到當前區域頁面
                driver.find_element_by_css_selector('#sidebar > div:nth-child(1) > ul > li:nth-child(%d) > a:nth-child(%d)'%(i,j)).click()                                                                                  