# Demo 03: Azure OpenAI SDK: Conversație cu Azure OpenAI folosind recunoașterea vocală și sinteza vocală
# Documentatie: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/openai-speech

import os
import azure.cognitiveservices.speech as speechsdk
from openai import AzureOpenAI
from dotenv import load_dotenv

# Configuration

load_dotenv(override=True)  # take environment variables from .env file
AZURE_OPENAI_API_ENDPOINT = os.getenv("AZURE_OPENAI_API_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")

AZURE_SPEECH_API_REGION = os.getenv("AZURE_SPEECH_API_REGION")
AZURE_SPEECH_API_KEY = os.getenv("AZURE_SPEECH_API_KEY")

client = AzureOpenAI(
    # https://learn.microsoft.com/azure/ai-services/openai/reference#rest-api-versioning
    api_version="2024-06-01",
    api_key=AZURE_OPENAI_API_KEY,
    azure_endpoint=AZURE_OPENAI_API_ENDPOINT,
)

speech_config = speechsdk.SpeechConfig(
    subscription=AZURE_SPEECH_API_KEY, 
    region=AZURE_SPEECH_API_REGION)

speech_config.speech_recognition_language="ro-RO"
speech_config.set_profanity(speechsdk.ProfanityOption.Raw)
audio_output_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)

# Should be the locale for the speaker's language.
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_output_config)

# The language of the voice that responds on behalf of Azure OpenAI.
speech_config.speech_synthesis_voice_name='ro-RO-AlinaNeural'
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

# Prompts Azure OpenAI with a request and synthesizes the response.
def ask_openai(prompt):

    # Ask Azure OpenAI
    completion = client.chat.completions.create(
    model=AZURE_OPENAI_CHAT_DEPLOYMENT_NAME,
    messages=[
        {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": prompt
            }]
        }
    ],
    )

    text = completion.choices[0].message.content.replace('\n', '').replace(' .', '.').strip()
    print('Azure OpenAI response:' + text)

    # Azure text-to-speech output
    speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

    # Check result
    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized to speaker for text [{}]".format(text))
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))

# Continuously listens for speech input to recognize and send as text to Azure OpenAI
def chat_with_open_ai():
    while True:
        print("Azure OpenAI is listening. Say 'Stop' or press Ctrl-Z to end the conversation.")
        try:
            # Get audio from the microphone and then send it to the TTS service.
            speech_recognition_result = speech_recognizer.recognize_once_async().get()

            # If speech is recognized, send it to Azure OpenAI and listen for the response.
            if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
                if speech_recognition_result.text == "Stop.": 
                    print("Conversation ended.")
                    break
                print("Recognized speech: {}".format(speech_recognition_result.text))
                ask_openai(speech_recognition_result.text)
            elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
                print("No speech could be recognized: {}".format(speech_recognition_result.no_match_details))
                break
            elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
                cancellation_details = speech_recognition_result.cancellation_details
                print("Speech Recognition canceled: {}".format(cancellation_details.reason))
                if cancellation_details.reason == speechsdk.CancellationReason.Error:
                    print("Error details: {}".format(cancellation_details.error_details))
                    print("Did you set the speech resource key and region values?")
        except EOFError:
            break

# Main

try:
    chat_with_open_ai()
except Exception as err:
    print("Encountered exception. {}".format(err))