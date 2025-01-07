import requests

def get_url(query):
    spaced_query = query.replace("+", " ")
    BASE_URL = "https://www.youtube.com/youtubei/v1/search?prettyPrint=false"
    body = {
        "context": {
            "client": {
                "hl": "en",
                "gl": "IN",
                "remoteHost": "",
                "deviceMake": "",
                "deviceModel": "",
                "visitorData": "",
                "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36,gzip(gfe)",
                "clientName": "WEB",
                "clientVersion": "2.20241219.01.00",
                "osName": "Windows",
                "osVersion": "10.0",
                "originalUrl": f"https://www.youtube.com/results?search_query={query}",
                "screenPixelDensity": 1,
                "platform": "DESKTOP",
                "clientFormFactor": "UNKNOWN_FORM_FACTOR",
                "configInfo": {
                    "appInstallData": "",
                    "coldConfigData": "",
                    "coldHashData": "",
                    "hotHashData": ""
                },
                "screenDensityFloat": 1.25,
                "userInterfaceTheme": "USER_INTERFACE_THEME_DARK",
                "timeZone": "",
                "browserName": "Chrome",
                "browserVersion": "131.0.0.0",
                "acceptHeader": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "deviceExperimentId": "",
                "rolloutToken": "",
                "screenWidthPoints": 0,
                "screenHeightPoints": 0,
                "utcOffsetMinutes": 0,
                "memoryTotalKbytes": "8000000",
                "mainAppWebInfo": {
                    "graftUrl": f"/results?search_query={query}",
                    "pwaInstallabilityStatus": "PWA_INSTALLABILITY_STATUS_UNKNOWN",
                    "webDisplayMode": "WEB_DISPLAY_MODE_BROWSER",
                    "isWebNativeShareAvailable": True
                }
            },
            "user": {
                "lockedSafetyMode": False
            },
            "request": {
                "useSsl": True,
                "internalExperimentFlags": [],
                "consistencyTokenJars": []
            },
            "clickTracking": {
                "clickTrackingParams": ""
            },
            "adSignalsInfo": {
                "params": []
            }
        },
        "query": spaced_query,
        "webSearchboxStatsUrl": ""
    }
    try:
        response = requests.post(BASE_URL, json=body)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch video URL: {response.content}")
        data = response.json()
        sectionListRendererParent = data["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]
        if "sectionListRenderer" not in sectionListRendererParent:
            return None
        sectionListRenderer = sectionListRendererParent["sectionListRenderer"]
        if "contents" not in sectionListRenderer:
            return None
        contents = sectionListRenderer["contents"]
        if len(contents) == 0:
            return None
        for content in contents:
            if "itemSectionRenderer" not in content:
                continue
            itemSectionRenderer = content["itemSectionRenderer"]
            if "contents" not in itemSectionRenderer:
                continue
            contents = itemSectionRenderer["contents"]
            if len(contents) == 0:
                continue
            for inner_content in contents:
                if "videoRenderer" not in inner_content:
                    continue
                videoRenderer = inner_content["videoRenderer"]
                if "videoId" not in videoRenderer:
                    continue
                video_id = videoRenderer["videoId"]
                return f"https://www.youtube.com/watch?v={video_id}"
    except Exception as e:
        print(f"An error occurred: {e}")
        return None