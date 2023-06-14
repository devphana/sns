from bs4 import BeautifulSoup
import requests
import json
import csv
import pandas as pd
import os
from openpyxl import Workbook

# 사용자 입력 받기
api_key = input("YouTube API 키를 입력하세요: ") ##API키는 본인의 API키를 입력하시면 됩니다
keyword = input("검색할 키워드를 입력하세요: ")
video_count = int(input("조회할 영상 수를 입력하세요: "))
comment_count = int(input("각 영상에서 가져올 댓글 수를 입력하세요: "))
file_path = input("파일 저장 경로를 입력하세요: ")

# YouTube API 호출을 위한 URL 설정
url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults={video_count}&q={keyword}&type=video&key={api_key}"

# YouTube API 호출 및 결과 받아오기
response = requests.get(url)
data = json.loads(response.text)

# 댓글 정보 저장할 리스트 초기화
comments = []

# 각 영상에서 댓글 가져오기
for item in data["items"]:
    video_id = item["id"]["videoId"]
    
    # YouTube API 호출을 위한 URL 설정
    comment_url = f"https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&maxResults={comment_count}&videoId={video_id}&key={api_key}"
    
    # 댓글 API 호출 및 결과 받아오기
    comment_response = requests.get(comment_url)
    comment_data = json.loads(comment_response.text)
    
    # 댓글 정보 추출하여 리스트에 저장
    for comment_item in comment_data["items"]:
        comment = comment_item["snippet"]["topLevelComment"]["snippet"]
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        comment_author = comment["authorDisplayName"]
        comment_date = comment["publishedAt"]
        comment_text = comment["textDisplay"]
        soup = BeautifulSoup(comment_text, "html.parser")
        comment_text_cleaned = soup.get_text()
        comments.append([video_url, comment_author, comment_date, comment_text_cleaned])

# txt 파일로 저장
txt_file_path = os.path.join(file_path , 'comment.txt')
with open(txt_file_path, "w", encoding="utf-8") as file:
    for i, comment in enumerate(comments):
        file.write(f"{i+1}번째 영상의 {i+1}번째 댓글\n")
        file.write("---------------------------\n")
        file.write(f"유튜브 영상 URL: {comment[0]}\n")
        file.write(f"댓글 작성자명: {comment[1]}\n")
        file.write(f"댓글 작성일자: {comment[2]}\n")
        file.write(f"댓글 내용: {comment[3]}\n\n")


# csv 파일로 저장
csv_file_path = os.path.join(file_path , 'comment.csv')

with open(csv_file_path, "w", newline="", encoding="utf-8-sig") as file:
    writer = csv.writer(file)
    writer.writerow(["URL", "댓글 작성자명", "댓글 작성일자", "댓글 내용"])
    writer.writerows(comments)

excel_file_path =os.path.join(file_path , 'comment.xlsx')
df = pd.DataFrame(comments, columns=["URL", "댓글 작성자명", "댓글 작성일자", "댓글 내용"])
df.to_excel(excel_file_path, index=False,encoding="utf-8")


