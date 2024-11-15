import cv2
import os

def process_video(video_path, frames_dir='./frames', frame_rate=1):
    """
    Extract frames from a video file.
    
    Args:
    video_path (str): Path to the input video file.
    frames_dir (str): Directory to save the extracted frames.
    frame_rate (int): Number of frames to skip between saves. A frame_rate of 1 saves every frame.
    
    Returns:
    list: Paths to the saved frames.
    """
    # Create directory for frames if it does not exist
    if not os.path.exists(frames_dir):
        os.makedirs(frames_dir)
    
    video = cv2.VideoCapture(video_path)
    count = 0
    frame_count = 0
    frame_list = []

    success, image = video.read()
    while success:
        # Save frame every 'frame_rate' frames
        if count % frame_rate == 0:
            frame_filename = os.path.join(frames_dir, f"frame_{frame_count}.jpg")
            cv2.imwrite(frame_filename, image)
            frame_list.append(frame_filename)
            frame_count += 1
        
        success, image = video.read()
        count += 1

    video.release()
    return frame_list

# Example usage:
# video_path = 'path_to_your_video.mp4'
# frames = process_video(video_path)
# print("Frames extracted:", frames)
