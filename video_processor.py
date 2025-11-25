import os
import math
import ffmpeg
from faster_whisper import WhisperModel
import pysrt
from translate import Translator
from gtts import gTTS
from pydub import AudioSegment
from moviepy.editor import VideoFileClip, AudioFileClip

class VideoProcessor:
    def __init__(self, job_id, jobs_dict):
        self.job_id = job_id
        self.jobs = jobs_dict
        self.temp_dir = 'temp'
        os.makedirs(self.temp_dir, exist_ok=True)
    
    def update_progress(self, progress, step):
        self.jobs[self.job_id]['progress'] = progress
        self.jobs[self.job_id]['step'] = step
        self.jobs[self.job_id]['status'] = 'processing'
    
    def extract_audio(self, video_path):
        self.update_progress(10, 'Extracting audio from video...')
        
        extracted_audio = os.path.join(self.temp_dir, f"{self.job_id}_audio.wav")
        stream = ffmpeg.input(video_path)
        stream = ffmpeg.output(stream, extracted_audio)
        ffmpeg.run(stream, overwrite_output=True, quiet=True)
        
        return extracted_audio
    
    def transcribe(self, audio_path):
        self.update_progress(25, 'Transcribing audio (this may take a while)...')
        
        model = WhisperModel("small", device="cpu", compute_type="int8")
        segments, info = model.transcribe(audio_path)
        language = info.language
        segments = list(segments)
        
        print(f"Detected language: {language}")
        return language, segments
    
    def generate_subtitle_file(self, language, segments):
        self.update_progress(40, 'Generating subtitle file...')
        
        subtitle_file = os.path.join(self.temp_dir, f"{self.job_id}_original.srt")
        text = ""
        
        for index, segment in enumerate(segments):
            segment_start = self.format_time(segment.start)
            segment_end = self.format_time(segment.end)
            text += f"{str(index+1)} \n"
            text += f"{segment_start} --> {segment_end} \n"
            text += f"{segment.text} \n"
            text += "\n"
        
        with open(subtitle_file, "w", encoding="utf-8") as f:
            f.write(text)
        
        return subtitle_file
    
    def format_time(self, seconds):
        hours = math.floor(seconds / 3600)
        seconds %= 3600
        minutes = math.floor(seconds / 60)
        seconds %= 60
        milliseconds = round((seconds - math.floor(seconds)) * 1000)
        seconds = math.floor(seconds)
        formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:01d},{milliseconds:03d}"
        return formatted_time
    
    def translate_subtitles(self, subtitle_file, from_lang, to_lang):
        self.update_progress(50, f'Translating subtitles to {to_lang}...')
        
        subs = pysrt.open(subtitle_file)
        translated_file = os.path.join(self.temp_dir, f"{self.job_id}_translated.srt")
        
        translator = Translator(to_lang=to_lang, from_lang=from_lang)
        
        for i, sub in enumerate(subs):
            try:
                sub.text = translator.translate(sub.text)
                if i % 10 == 0:
                    self.update_progress(50 + (i / len(subs)) * 10, f'Translating {i+1}/{len(subs)}...')
            except Exception as e:
                print(f"Translation error for segment {i}: {e}, keeping original text")
        
        subs.save(translated_file, encoding='utf-8')
        return translated_file
    
    def generate_dubbed_audio(self, subtitle_file, target_lang):
        self.update_progress(65, 'Generating dubbed audio (this may take a while)...')
        
        subs = pysrt.open(subtitle_file)
        combined = AudioSegment.silent(duration=0)
        
        for i, sub in enumerate(subs):
            if i % 5 == 0:
                self.update_progress(65 + (i / len(subs)) * 15, f'Generating speech {i+1}/{len(subs)}...')
            
            start_time = sub.start.ordinal / 1000.0
            text = sub.text
            
            try:
                tts = gTTS(text, lang=target_lang)
                temp_mp3 = os.path.join(self.temp_dir, f"{self.job_id}_temp_{i}.mp3")
                tts.save(temp_mp3)
                
                audio = AudioSegment.from_mp3(temp_mp3)
                
                current_duration = len(combined)
                silent_duration = start_time * 1000 - current_duration
                
                if silent_duration > 0:
                    combined += AudioSegment.silent(duration=silent_duration)
                
                combined += audio
                
                os.remove(temp_mp3)
            except Exception as e:
                print(f"Error generating audio for segment {i}: {e}")
        
        dubbed_audio_file = os.path.join(self.temp_dir, f"{self.job_id}_dubbed.wav")
        combined.export(dubbed_audio_file, format='wav')
        
        return dubbed_audio_file
    
    def merge_audio_video(self, video_path, audio_path):
        self.update_progress(85, 'Merging dubbed audio with video...')
        
        output_path = os.path.join('outputs', f"{self.job_id}_dubbed.mp4")
        
        video = VideoFileClip(video_path)
        audio = AudioFileClip(audio_path)
        
        video_with_new_audio = video.set_audio(audio)
        video_with_new_audio.write_videofile(
            output_path, 
            codec='libx264', 
            audio_codec='aac',
            logger=None
        )
        
        video.close()
        audio.close()
        
        return output_path
    
    def cleanup_temp_files(self):
        try:
            for file in os.listdir(self.temp_dir):
                if file.startswith(self.job_id):
                    os.remove(os.path.join(self.temp_dir, file))
        except Exception as e:
            print(f"Error cleaning up temp files: {e}")
    
    def process(self, input_video_path, source_language, target_language):
        try:
            audio_path = self.extract_audio(input_video_path)
            
            detected_language, segments = self.transcribe(audio_path)
            
            subtitle_file = self.generate_subtitle_file(detected_language, segments)
            
            from_lang = source_language if source_language else detected_language
            
            translated_subtitle_file = self.translate_subtitles(
                subtitle_file, 
                from_lang, 
                target_language
            )
            
            dubbed_audio_path = self.generate_dubbed_audio(
                translated_subtitle_file, 
                target_language
            )
            
            output_path = self.merge_audio_video(
                input_video_path, 
                dubbed_audio_path
            )
            
            self.cleanup_temp_files()
            
            try:
                os.remove(input_video_path)
            except:
                pass
            
            return output_path
            
        except Exception as e:
            self.cleanup_temp_files()
            raise e
