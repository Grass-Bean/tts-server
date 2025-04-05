import io
import numpy as np
import soundfile as sf
import litserve as ls
from fastapi.responses import Response
from kokoro import KPipeline

class KokoroAPI(ls.LitAPI):
    """
    KokoroAPI is a subclass of ls.LitAPI that provides an interface to the Kokoro model for text-to-speech task.

    Methods:
        - setup(device): Called once at startup for the task-specific setup.
        - decode_request(request): Convert the request payload to model input.
        - predict(inputs): Uses the model to generate audio from the input text.
        - encode_response(output): Convert the model output to a response payload.
    """

    def __init__(self):
        super().__init__()
        self.pipeline = None
        self.current_lang = None

    def setup(self, device):
        self.device = device

    def decode_request(self, request):
        """
        Convert the request payload to model input.
        """
        # Extract the inputs from request payload
        language_code = request.get("language_code", "a")
        text = request.get("text")
        voice = request.get("voice", "af_heart")

        # Initialize or update pipeline if language changes
        if self.current_lang != language_code:
            self.current_lang = language_code
            self.pipeline = KPipeline(lang_code=language_code, device=self.device)

        # Return the inputs
        return text, voice

    def predict(self, inputs):
        """
        Run inference and generate audio file using th  e Kokoro model.
        """
        # Get the inputs
        text, voice = inputs
        # Generate audio files

        generator = self.pipeline(text, voice=voice, speed=1, split_pattern=r'\n+|\. |\? |! |。| ？')

        # Return the audio data
        return self.combine_audio_chunks(generator)
    
    def combine_audio_chunks(self, generator):
        audio_segments = []
        samplerate = 24000  # Assuming fixed sample rate from pipeline
        
        # Process audio entirely in memory
        for _, _, audio in generator:
            audio_segments.append(audio)

        if not audio_segments:
            raise ValueError("No audio generated")

        # Concatenate all audio segments
        final_audio = np.concatenate(audio_segments)

        # Create in-memory audio file
        audio_buffer = io.BytesIO()
        sf.write(audio_buffer, final_audio, samplerate, format="WAV")
        audio_buffer.seek(0)
        audio_data = audio_buffer.getvalue()
        audio_buffer.close()

        return audio_data

    def encode_response(self, output):
        """
        Convert the model output to a response payload.
        """
        # Package the generated audio data into a response
        return Response(content=output, headers={"Content-Type": "audio/wav"})


if __name__ == "__main__":
    # Create an instance of the KokoroAPI class and run the server
    api = KokoroAPI()
    # Update accelerator to specifically use cpu, gpu or auto-detect
    server = ls.LitServer(api, track_requests=True, accelerator="auto")
    server.run(port=8000)