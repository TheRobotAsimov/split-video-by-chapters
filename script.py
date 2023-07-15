import os
import subprocess
import json

def get_chapter_info(video_path):
    """
    Use ffprobe to get chapter metadata from a video file.
    Returns a list of dictionaries containing the title, start, and end time for each chapter.
    """
    command = [
        "ffprobe",
        "-v",
        "quiet",
        "-print_format",
        "json",
        "-show_chapters",
        "-show_entries",
        "chapter=start_time,end_time",
        video_path,
    ]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    chapter_info = json.loads(result.stdout.decode('utf-8'))

    # Parse the JSON output and return a list of dictionaries
    chapter_list = []
    for chapter in chapter_info['chapters']:
        chapter_list.append({
            'title': chapter['tags']['title'],
            'start': chapter['start_time'],
            'end': chapter['end_time'],
        })
    return chapter_list

def split_video(video_path, output_dir):
    """
    Split a video into chapters and save the output files in the specified directory.
    """
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Get the chapter information
    chapters = get_chapter_info(video_path)

    # Iterate over the chapters and create a new video file for each one
    for i, chapter in enumerate(chapters):
        chapter_title = chapter['title']
        chapter_number = i + 1
        output_filename = f"{chapter_number}. {chapter_title}.mp4"
        output_path = os.path.join(output_dir, output_filename)
        command = [
            "ffmpeg",
            "-i",
            video_path,
            "-ss",
            str(chapter['start']),
            "-to",
            str(chapter['end']),
            "-c",
            "copy",
            output_path,
        ]
        subprocess.run(command)

# Test the functions
video_path = "./video.mkv"
output_dir = "./output"
split_video(video_path, output_dir)
