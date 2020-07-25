#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  7 22:33:40 2018

@author: talhaseker
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import csv
import time

option = webdriver.ChromeOptions()
option.add_argument(" — incognito")
driver = webdriver.Chrome("/Users/talhaseker/PythonWorkspace/chromedriver",chrome_options= option)
print("Trying to fetch the web site first...")
driver.get("https://www.nytimes.com/crosswords/game/mini")
print("Got the web site successfully!")


        #find_elements_by_xpath returns an array of selenium objects.
titles_element = driver.find_elements_by_xpath("//*[@id='root']/div/div[1]/div[3]/div/main/div[2]/div/article/section[2]/div[1]/ol") #"//a[@class='cloud-zoom']")
        # use list comprehension to get the actual repo titles and not the selenium objects.
#titles = [x.text for x in titles_element]
        # print out all the titles.

spanElementsLabel = driver.execute_script("return document.getElementsByClassName('Clue-label--2IdMY')")
spanElementsClues = driver.execute_script("return document.getElementsByClassName('Clue-text--3lZl7')")
strGOpen = ">"
strGClose = "</"

labels = [1,1,1,1,1,1,1,1,1,1]
clues = ["","","","","","","","","",""]

for i in range(0, 10):
    executeScript = "return document.getElementsByClassName('Clue-label--2IdMY')[" + str(i) + "].innerHTML"
    labels[i] = driver.execute_script(executeScript)
    executeScript = "return document.getElementsByClassName('Clue-text--3lZl7')[" + str(i) + "].innerHTML"
    clues[i] = driver.execute_script(executeScript)

        #find_elements_by_xpath returns an array of selenium objects.
titles2_element = driver.find_elements_by_xpath("//*[@id='root']/div/div/div[3]/div/main/div[2]/div/article/section[2]/div[2]/ol") #"//a[@class='cloud-zoom']")
        # use list comprehension to get the actual repo titles and not the selenium objects.
titles2 = [x.text for x in titles2_element]
        # print out all the titles.

if titles2:
    titles2 = titles2[0]
else:
    titles2 = " "

#Clicking to the start button
element = driver.find_elements_by_xpath("//*[@id='root']/div/div/div[3]/div/main/div[2]/div/div[2]/div[2]/article/div[2]/button/div")
driver.implicitly_wait(5)
element[0].click()

#clicking reveal button
element = driver.find_elements_by_xpath("//*[@id='root']/div/div[1]/div[3]/div/main/div[2]/div/div/ul/div[1]/li[2]/button")
driver.implicitly_wait(5)
element[0].click()

#clicking puzzle button
element = driver.find_elements_by_xpath("//*[@id='root']/div/div/div[3]/div/main/div[2]/div/div/ul/div[1]/li[2]/ul/li[3]/a")
driver.implicitly_wait(5)
element[0].click()

#clicking another reveal button
element = driver.find_elements_by_xpath("//*[@id='root']/div/div[2]/div[2]/article/div[2]/button[2]/div")
driver.implicitly_wait(5)
element[0].click()

#clicking close button
element = driver.find_elements_by_xpath("//*[@id='root']/div/div[2]/div[2]/div/a")
driver.implicitly_wait(5)
element[0].click()

aa = driver.execute_script("return document.getElementsByTagName('div')[0].innerHTML")

strCells = "<g data-group=\"cells\">"
strGrid = "<g data-group=\"grid\">"

numberCells = aa.find(strCells)
numberGrid = aa.find(strGrid)

aa = aa[numberCells:numberGrid]

strBlackClass = "Cell-block--1oNaD"
strNumberClass = "text-anchor=\"start\""
strCharClass = "text-anchor=\"middle\""

strGOpen = "<g>"
strGClose = "</g>"

finalChars = ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1']
finalXs = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
finalYs = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
finalLengths = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
finalNumbers = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

for i in range(0, 25):
    numberGOpen = aa.find(strGOpen)
    numberGClose = aa.find(strGClose) + 4
    bb = aa[numberGOpen:numberGClose]
    if bb.find(strBlackClass) != -1:
        finalChars[i] = '0'
    elif bb.find(strCharClass) > 0:
        finalChars[i] = bb[bb.find(strCharClass) + 39]
        if bb.find(strNumberClass) > 0:
            finalNumbers[i] = int(bb[bb.find(strNumberClass) + 38])
        else:
            finalNumbers[i] = -1

    finalXs[i] = i%5
    finalYs[i] = i//5

    aa = aa[numberGClose:]

answersFile = open("puzzles/new/new-solution.txt", "w")
skeletonFile = open("puzzles/new/new-skeleton.txt", "w")

count = 0
for i in range(0,24):
    if count >= 4:
        count = 0
        answersFile.write(str(finalChars[i]) + "\n")
        if finalChars[i] == '0':
            skeletonFile.write("0" + "\n")
        else:
            skeletonFile.write("_" + "\n")
    else:
        count = count+1
        answersFile.write(str(finalChars[i]) + " ")
        if finalChars[i] == '0':
            skeletonFile.write("0" + " ")
        else:
            skeletonFile.write("_" + " ")

answersFile.write(str(finalChars[24]))
if finalChars[24] == '0':
    skeletonFile.write("0" + "\n")
else:
    skeletonFile.write("_" + "\n")


answersFile.close()
skeletonFile.close()



cluesFile = open("puzzles/new/new-clues.txt", "w")

cluesFile.write("#FRIDAY the 13th!\n")
cluesFile.write("# ACROSS\n")

for i in range(0, 5):
    indexOfNumber = finalNumbers.index(int(labels[i]))
    xOfNumber = finalXs[indexOfNumber]
    xIndexToIncrease = xOfNumber
    yOfNumber = finalYs[indexOfNumber]
    length = 0
    while xIndexToIncrease < 5:
        if finalChars[yOfNumber*5 + xIndexToIncrease] != '0':
            length = length + 1
        xIndexToIncrease = xIndexToIncrease + 1
    cluesFile.write(labels[i] + "\t" + str(yOfNumber) + "\t" + str(xOfNumber) + "\t" + str(length) + "\t" + clues[i] + "\n")

cluesFile.write("# DOWN\n")

for i in range(5, 9):
    indexOfNumber = finalNumbers.index(int(labels[i]))
    xOfNumber = finalXs[indexOfNumber]
    yOfNumber = finalYs[indexOfNumber]
    yIndexToIncrease = yOfNumber
    length = 0
    while yIndexToIncrease < 5:
        if finalChars[yIndexToIncrease*5 + xOfNumber] != '0':
            length = length + 1
        yIndexToIncrease = yIndexToIncrease + 1
    cluesFile.write(labels[i] + "\t" + str(yOfNumber) + "\t" + str(xOfNumber) + "\t" + str(length) + "\t" + clues[i] + "\n")

indexOfNumber = finalNumbers.index(int(labels[9]))
xOfNumber = finalXs[indexOfNumber]
yOfNumber = finalYs[indexOfNumber]
yIndexToIncrease = yOfNumber
length = 0
while yIndexToIncrease < 5:
    if finalChars[yIndexToIncrease*5 + xOfNumber] != '0':
        length = length + 1
    yIndexToIncrease = yIndexToIncrease + 1
cluesFile.write(labels[9] + "\t" + str(yOfNumber) + "\t" + str(xOfNumber) + "\t" + str(length) + "\t" + clues[9])
cluesFile.close()
