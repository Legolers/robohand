import client
import speech_recognition as sr
import serial
import serial.tools.list_ports
import struct,time


print("Running SpeechRecognition v:",sr.__version__)


ear = client.Client()
ear.debug()