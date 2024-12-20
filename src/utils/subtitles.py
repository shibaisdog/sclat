import re

def time_to_seconds(time_str: str) -> float:
    time_parts = re.split('[:.]', time_str)
    hours = int(time_parts[0])
    minutes = int(time_parts[1])
    seconds = int(time_parts[2])
    milliseconds = int(time_parts[3])
    total_seconds = hours * 3600 + minutes * 60 + seconds + milliseconds / 1000.0
    return total_seconds

def parse_vtt_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        vtt_content = file.read()
    time_regex = r'(\d{2}:\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}:\d{2}\.\d{3})\s*(size:\d+% position:\d+% line:\d+%)?'
    subtitle_regex = r'<c\.[^>]+>(.*?)</c>'
    content_without_color = re.sub(subtitle_regex, r'\1', vtt_content)
    content_without_color = re.sub(r'<[^>]+>', '', content_without_color)
    subtitles = []
    for match in re.finditer(time_regex, content_without_color):
        start_time, end_time, attributes = match.groups()
        size = position = line = None
        if attributes:
            size_match = re.search(r'size:(\d+%)', attributes)
            position_match = re.search(r'position:(\d+%)', attributes)
            line_match = re.search(r'line:(\d+%)', attributes)
            size = size_match.group(1)[:-1] if size_match else None
            position = position_match.group(1)[:-1] if position_match else None
            line = line_match.group(1)[:-1] if line_match else None
        subtitle_start = match.end()
        subtitle_end = content_without_color.find('\n\n', subtitle_start)
        if subtitle_end == -1:
            subtitle_end = len(content_without_color)
        subtitle_text = content_without_color[subtitle_start:subtitle_end].strip()
        subtitle_text = re.sub(r'\s*(align:[^ \n]+|size:[^ \n]+|position:[^ \n]+|line:[^ \n]+)\s*', '', subtitle_text)
        if position == None:
            position = 50
        if line == None:
            line = 90
        subtitles.append({
            "start_time": time_to_seconds(start_time),
            "end_time": time_to_seconds(end_time),
            "text": subtitle_text,
            "size": size,
            "position": position,
            "line": line
        })
    return subtitles
