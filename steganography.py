import cv2
import wave
import os

# Image Encoding Capacity
def max_words_image(img_path):
    img = cv2.imread(img_path)
    if img is None:
        raise FileNotFoundError(f"Image at path '{img_path}' not found.")
    
    height, width, _ = img.shape
    total_bits = height * width * 3  # Total bits available in the image (RGB channels)
    max_bytes = total_bits // 8  # Convert bits to bytes
    max_words = max_bytes // 6  # Assuming an average word length of 5 characters + 1 space
    max_mb = max_bytes / (1024 * 1024)  # Convert bytes to megabytes
    return max_words


def max_words_audio(audio_path):
    try:
        with wave.open(audio_path, 'rb') as audio_file:
            # Get the parameters of the audio file
            n_channels = audio_file.getnchannels()
            sampwidth = audio_file.getsampwidth()
            framerate = audio_file.getframerate()
            n_frames = audio_file.getnframes()
            
            # Calculate the total number of bits available in the audio file
            total_bits = n_channels * sampwidth * 8 * n_frames
            
            # Calculate the maximum bytes available for encoding (assuming LSB method)
            max_bytes = total_bits // 8
            
            # Calculate the maximum words and MB (assuming average word length of 6 bytes, including space)
            max_words = max_bytes // 6
            max_mb = max_bytes / (1024 * 1024)
            
            return max_words
    except Exception as e:
        raise RuntimeError(f"Failed to process audio file: {e}")


# # Video Encoding Capacity
# def max_words_video(video_path):
#     cap = cv2.VideoCapture(video_path)
#     if not cap.isOpened():
#         raise ValueError("Failed to open video file.")

#     total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
#     frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#     frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

#     cap.release()

#     total_bits = total_frames * frame_height * frame_width * 3 * 8  # 3 bytes per pixel (RGB), 8 bits per byte
#     max_bytes = total_bits // 8
#     max_words = max_bytes // 5  # Assuming an average word length of 5 characters

#     return max_words

# Text Document Encoding Capacity
def max_words_text(text_path):
    # Replace this with actual text file handling logic
    text_size = os.path.getsize(text_path)
    max_words = text_size // 5  # Assuming an average word length of 5 characters
    max_mb = text_size / (1024 * 1024)  # Convert bytes to megabytes

    return max_words

def encode_img_data(img_path, message, key, output_path):
    image_path = "C:\\sasta copies\\7 excellent\\Sample_cover_files\\cover_image.jpg"  # Define the image path here
    try:
        # Read the image
        img = cv2.imread(img_path)
        if img is None:
            raise ValueError("Image not found or unable to read image")
        
        # Combine key with the message
        message_with_key = key + ':' + message

        # Convert the message to binary
        binary_message = ''.join(format(ord(char), '08b') for char in message_with_key)
        binary_message += '1111111111111110'  # Delimiter to indicate end of message

        data_index = 0
        message_len = len(binary_message)

        for values in img:
            for pixel in values:
                for i in range(3):
                    if data_index < message_len:
                        # Modify the pixel value only if there are bits left in the message
                        pixel[i] = int(format(pixel[i], '08b')[:-1] + binary_message[data_index], 2)
                        data_index += 1

        if data_index < message_len:
            raise ValueError("Message is too long to encode in the provided image")

        # Save the encoded image
        cv2.imwrite(output_path, img) 
        print("Message encoded successfully")
        
        # Ensure the new image size is similar to the original
        original_size = os.path.getsize(image_path)
        new_size = os.path.getsize(output_path)
        if abs(new_size - original_size) > original_size * 0.1:  # Allow up to 10% size difference
            return False
            return True

    except Exception as e:
        print(f"Error encoding image: {e}")
        raise e

def decode_img_data(img_path, key):
    try:
        img = cv2.imread(img_path)
        if img is None:
            raise ValueError("Image not found or unable to read image")

        binary_message = ''
        for values in img:
            for pixel in values:
                for i in range(3):
                    binary_message += format(pixel[i], '08b')[-1]
    
        # Find the position of the delimiter to stop decoding
        delimiter_pos = binary_message.find('1111111111111110')
        if delimiter_pos != -1:
            binary_message = binary_message[:delimiter_pos]
    
        # Convert binary message to text
        all_bytes = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]
        decoded_message_with_key = ''.join([chr(int(byte, 2)) for byte in all_bytes])
    
        # Split the key and the actual message
        provided_key, decoded_message = decoded_message_with_key.split(':', 1)
    
        # Validate the key
        if provided_key != key:
            return "Incorrect key provided"

        return decoded_message

    except Exception as e:
        return f"Error decoding image: {e}"

def encode_aud_data(audio_path, message, key, output_path):
    try:
        # Combine key with the message
        message_with_key = key + ':' + message

        # Open the audio file
        audio = wave.open(audio_path, 'rb')
        frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))

        # Prepare the message to be encoded with padding
        message_with_key += int((len(frame_bytes) - (len(message_with_key) * 8)) / 8) * '#'
        bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8, '0') for i in message_with_key])))

        # Modify the LSB of each byte of the audio file
        for i, bit in enumerate(bits):
            frame_bytes[i] = (frame_bytes[i] & 254) | bit

        # Write the modified bytes to the output file
        with wave.open(output_path, 'wb') as fd:
            fd.setparams(audio.getparams())
            fd.writeframes(frame_bytes)

        audio.close()
        print("Message encoded successfully")
    except Exception as e:
        print(f"Error encoding audio: {e}")
        raise e

def decode_aud_data(audio_path, key):
    try:
        # Open the audio file
        audio = wave.open(audio_path, 'rb')
        frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))

        # Extract the LSB of each byte
        message_bits = []
        for byte in frame_bytes:
            message_bits.append(byte & 1)

        # Convert bits to characters
        decoded_message = ''.join(chr(int(''.join(map(str, message_bits[i:i+8])), 2)) for i in range(0, len(message_bits), 8))

        # Strip out the padding characters
        decoded_message = decoded_message.split('#')[0]

        # Split the key and the actual message
        provided_key, decoded_message = decoded_message.split(':', 1)

        # Validate the key
        if provided_key != key:
            return "Incorrect key provided"

        audio.close()
        return decoded_message
    except Exception as e:
        return f"Error decoding audio: {e}"

# Function to encode text data into a text document
def encode_txt_data(txt_path, message, key, output_path):
    try:
        with open(txt_path, 'r') as file:
            content = file.read().strip()  # Read existing content and strip any trailing newline
        
        # Combine key with the message
        message_with_key = key + ':' + message
        
        # Simple XOR encryption
        encrypted_message = ''.join(chr(ord(char) ^ ord(key[i % len(key)])) for i, char in enumerate(message_with_key))
        
        with open(output_path, 'w') as file:
            file.write(content + "\n" + encrypted_message)
        
        print("Encoded the data successfully in the text file.")
    except Exception as e:
        print(f"Error encoding data in text file: {e}")

# Function to decode text data from a text document
def decode_txt_data(txt_path, key):
    try:
        with open(txt_path, 'r') as file:
            content = file.read().strip()  # Read entire content and strip any trailing newline
        
        # Assume the encrypted message is at the end of the document after a newline
        encrypted_message = content.split('\n')[-1]
        
        # Simple XOR decryption
        decrypted_message_with_key = ''.join(chr(ord(char) ^ ord(key[i % len(key)])) for i, char in enumerate(encrypted_message))
        
        # Split the key and the actual message
        provided_key, decoded_message = decrypted_message_with_key.split(':', 1)
        
        # Validate the key
        if provided_key != key:
            return "Incorrect key provided"
        
        return decoded_message
    except Exception as e:
        return f"Error decoding data from text file: {e}"

# # Video Steganography
# def embed(frame, message, key):
#     data = key + ':' + message
#     binary_message = ''.join(format(ord(char), '08b') for char in data)
#     binary_message += '1111111111111110'  # Delimiter to indicate end of message

#     data_index = 0
#     message_len = len(binary_message)

#     for values in frame:
#         for pixel in values:
#             for i in range(3):
#                 if data_index < message_len:
#                     pixel[i] = int(format(pixel[i], '08b')[:-1] + binary_message[data_index], 2)
#                     data_index += 1

#     if data_index < message_len:
#         raise ValueError("Message is too long to encode in the provided frame")

#     return frame

# def extract(frame, key):
#     binary_message = ''
#     for values in frame:
#         for pixel in values:
#             for i in range(3):
#                 binary_message += format(pixel[i], '08b')[-1]

#     delimiter_pos = binary_message.find('1111111111111110')
#     if delimiter_pos != -1:
#         binary_message = binary_message[:delimiter_pos]

#     all_bytes = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]
#     decoded_message_with_key = ''.join([chr(int(byte, 2)) for byte in all_bytes])

#     provided_key, decoded_message = decoded_message_with_key.split(':', 1)

#     if provided_key != key:
#         return "Incorrect key provided"

#     return decoded_message

# def encode_vid_data(video_path, message, key, frame_number, output_path):
#     try:
#         cap = cv2.VideoCapture(video_path)
#         if not cap.isOpened():
#             raise ValueError("Failed to open video file.")

#         frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

#         if frame_number >= frame_count:
#             raise ValueError(f"Frame number {frame_number} is out of range. The video has {frame_count} frames.")

#         frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#         frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#         fourcc = cv2.VideoWriter_fourcc(*'XVID')
#         out = cv2.VideoWriter(output_path, fourcc, cap.get(cv2.CAP_PROP_FPS), (frame_width, frame_height))

#         current_frame = 0
#         while cap.isOpened():
#             ret, frame = cap.read()
#             if not ret:
#                 break

#             if current_frame == frame_number:
#                 frame = embed(frame, message, key)

#             out.write(frame)
#             current_frame += 1

#         cap.release()
#         out.release()
#         print("Message encoded successfully in the video.")

#     except Exception as e:
#         print(f"Error encoding video: {e}")
#         raise e

# def decode_vid_data(video_path, key, frame_number):
#     try:
#         cap = cv2.VideoCapture(video_path)
#         if not cap.isOpened():
#             raise ValueError("Failed to open video file.")

#         frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

#         if frame_number >= frame_count:
#             raise ValueError(f"Frame number {frame_number} is out of range. The video has {frame_count} frames.")

#         current_frame = 0
#         decoded_message = None

#         while cap.isOpened():
#             ret, frame = cap.read()
#             if not ret:
#                 break

#             if current_frame == frame_number:
#                 decoded_message = extract(frame, key)
#                 break

#             current_frame += 1

#         cap.release()
#         return decoded_message if decoded_message else "Message not found or decoding failed."

#     except Exception as e:
#         return f"Error decoding video: {e}"

def display_image_encoding_capacity():
    image_path = "C:\\sasta copies\\7 excellent\\Sample_cover_files\\cover_image.jpg"  # Define the image path here
    try:
        max_words = max_words_image(image_path)
        print(f"Image Encoding Capacity:")
        print(f"  Maximum words that can be encoded: {max_words}")
    except FileNotFoundError as e:
        print(e)

def display_audio_encoding_capacity():
    audio_path = "C:\\sasta copies\\7 excellent\\Sample_cover_files\\cover_audio.wav" # Define the audio path here
    try:
        max_words = max_words_audio(audio_path)
        print(f"Audio Encoding Capacity:")
        print(f"  Maximum words that can be encoded: {max_words}")
    except FileNotFoundError as e:
        print(e)

def display_text_encoding_capacity():
    text_path = "C:\\sasta copies\\7 excellent\\Sample_cover_files\\cover_text.txt"  # Define the text path here
    try:
        max_words = max_words_text(text_path)
        print(f"Text Encoding Capacity:")
        print(f"  Maximum words that can be encoded: {max_words}")
    except FileNotFoundError as e:
        print(e)

# Call the functions to display encoding capacity
display_image_encoding_capacity()
display_audio_encoding_capacity()
display_text_encoding_capacity()

