from asyncore import write
import googleapiclient.discovery
import demoji
import re
import csv

CLEANR = re.compile('<.*?>') 

def clean_text(text):
    text = str(text)
    text = re.sub(CLEANR, '', text)
    text = demoji.replace(text, "")
    text = text.replace("\n", " ")
    text = text.strip()
    return text


def fetchComments(videoId):
    text_rows = []
    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyA-vEbdwfyM6z5qU06DBMciE4xHP3Vn4EY"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

    try:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=videoId,
            maxResults=100,
        )
        response = request.execute()
        items = response['items']
        for item in items:
            text = clean_text(item['snippet']['topLevelComment']['snippet']['textDisplay'])
            text_rows.append([str(text), ""])
    except:
        pass
    return text_rows

def fetchMultipleComments(videoIdArr):
    comment_list = []
    for videoId in videoIdArr:
        comment_list.extend(fetchComments(videoId))
    return comment_list

def fetchMultipleCommentsByQuery(queries):
    arr = []
    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyA-vEbdwfyM6z5qU06DBMciE4xHP3Vn4EY"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

    for query in queries:
        request = youtube.search().list(
            part="snippet",
            maxResults=25,
            q=query
        )
        response = request.execute()
        for item in response['items']:
            arr.append(item['id']['videoId'])

    return fetchMultipleComments(arr)
    
        
def writeToCsv(header, rows, file):
    with open(file, 'w') as csvfile: 
        csvwriter = csv.writer(csvfile) 
        csvwriter.writerow(header) 
        csvwriter.writerows(rows)
        
if __name__ == "__main__":
    comment_list = fetchMultipleCommentsByQuery(['blockchain', 'crypto', 'vaccine', 'metaverse'])
    print(len(comment_list))
    writeToCsv(["text", "bad"], comment_list, "data.csv")