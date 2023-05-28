from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from collections import defaultdict
import json
import re


mainDriver = webdriver.Chrome(service= Service(ChromeDriverManager().install()))
problemDriver = webdriver.Chrome(service= Service(ChromeDriverManager().install()))

url = "https://leetcode.com/problemset/all/"#"https://leetcode.com/problems/two-sum/"
mainDriver.get(url)
mainDriver.implicitly_wait(10)
alrogithmDict = defaultdict(set)

problemDriver.implicitly_wait(10)

noLabelProblem = set()

time.sleep(2)

prev = ''

while True:
    problems = mainDriver.find_elements(By.CSS_SELECTOR, 'div.truncate')
    for problem in problems:
        try:
            problemDriver.get(problem.find_element(By.TAG_NAME, 'a').get_attribute('href'))
            time.sleep(3)

            element = problemDriver.find_element(By.XPATH, '//*[@id="qd-content"]')
            if len(element.find_elements(By.XPATH, './div')) == 4:
                print("unsubcribe")
                print()
                continue

            title = problemDriver.find_element(By.XPATH, '//*[@id="qd-content"]/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[1]/div[1]/div/div/span')
            prev = title.text
            
            problem = problemDriver.find_element(By.XPATH, '//*[@id="qd-content"]/div[1]/div/div/div/div[2]/div/div/div[3]/div')
            pbTexts = problem.find_elements(By.XPATH, './/*')

            problemText = pbTexts[0].text
            if problemText == 'SQL Schema':
                print("sql", title.text)
                print()
                continue
            for i in range(1, len(pbTexts)):
                if pbTexts[i].text == "Example 1:":
                    break
                problemText = problemText + " " + pbTexts[i].text
            problemText = problemText.replace("\n", " ")
            key = title.text + "\n\n" + re.sub(r"\s+", " ", problemText.replace("\n", " "))

            RTBtn = problemDriver.find_element(By.XPATH, '//*[@id="qd-content"]/div[1]/div/div/div/div[2]/div/div/div[7]/div')
            RTBtn.click()
            time.sleep(1)
            relatedTopics = RTBtn.find_elements(By.TAG_NAME, 'a')
            
            if len(relatedTopics) == 0:
                print(1)
                RTBtn = problemDriver.find_element(By.XPATH, '//*[@id="qd-content"]/div[1]/div/div/div/div[2]/div/div/div[6]/div')
                RTBtn.click()
                time.sleep(1)
                relatedTopics = RTBtn.find_elements(By.TAG_NAME, 'a')
            if len(relatedTopics) == 0:
                print(2)
                RTBtn = problemDriver.find_element(By.XPATH, '//*[@id="qd-content"]/div[1]/div/div/div/div[2]/div/div/div[5]/div')
                RTBtn.click()
                time.sleep(1)
                relatedTopics = RTBtn.find_elements(By.TAG_NAME, 'a')
            if len(relatedTopics) == 0:
                print(3)
                noLabelProblem.add(title.text)
        except:
            print("noLabel")
            print()
            try:
                noLabelProblem.add(title.text)
            except:
                noLabelProblem.add(prev)
            continue
            
        for i in relatedTopics:
            alrogithmDict[key].add(i.text)
        
        print("problem num:", len(alrogithmDict), "no label num:", len(noLabelProblem))
        print(key)
        print(list(alrogithmDict[key]))
        print()
        print()

        if len(alrogithmDict) >= 1000 and len(alrogithmDict) % 100 == 0:
            saveDict = {}
            for k in alrogithmDict:
                saveDict[k] = list(alrogithmDict[k])
            with open('data_'+str(len(alrogithmDict))+'.json', 'w') as f : 
                json.dump(saveDict, f, indent=4)

    try:
        nextButton = mainDriver.find_element(By.XPATH, '//*[@id="__next"]/div/div[2]/div[1]/div[1]/div[5]/div[3]/nav/button[10]')
        nextButton.click()
        time.sleep(3)
    except:
        break

    
for k in alrogithmDict:
    alrogithmDict[k] = list(alrogithmDict[k])

with open('data.json', 'w') as f : 
	json.dump(alrogithmDict, f, indent=4)

with open('nolabel.json', 'w') as f : 
    json.dump(list(noLabelProblem), f, indent=4)