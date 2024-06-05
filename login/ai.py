import os
from django.conf import settings
import filetype
import cv2

def load_document(file_name):
    file_path = os.path.join(settings.MEDIA_ROOT, 'uploaded_files', file_name)
    try:
        with open(file_path, 'rb') as file:
            document = file.read()
        file_type = filetype.guess(document)  # Assuming filetype is installed
        type_of_file = file_type.mime
        return document, type_of_file
    except FileNotFoundError:
        return None, "File not found"
    except Exception as e:
        return None, str(e)  # Catch other potential errors

def preprocess_image(image_path):
    # Load the image using OpenCV
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Error reading image: {image_path}")

        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Enhance contrast using histogram equalization
        enhanced_gray = cv2.equalizeHist(gray)

        # Remove noise using a median blur
        denoised = cv2.medianBlur(enhanced_gray, 3)

        # Apply adaptive thresholding
        binary = cv2.adaptiveThreshold(denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

        # Invert the binary image
        inverted_binary = cv2.bitwise_not(binary)

        return inverted_binary


# # def apply_ai_editing(document):
# #     # Use OpenAI's GPT model to edit the document
# #     response = openai.Completion.create(
# #         engine="text-davinci-003",  # or another model you have access to
# #         prompt=f"Edit the following document for clarity and grammar:\n\n{document}",
# #         max_tokens=1024,
# #         n=1,
# #         stop=None,
# #         temperature=0.7,
# #     )

#     # Extract the edited text from the response
#     edited_text = response.choices[0].text.strip()
#     return edited_text



# def view_document(request, file_name):
#         try:
#             # Load the document (e.g., DOCX)
#             file_name = 'data_ingestion.pdf'
#             document, mime_type = load_document(file_name)
#             print(document)
#             print(mime_type)
#             return render(request, 'editor/view_pdf.html', {'pdf_url': document})
#             # Preprocess the document as needed
#             # preprocessed_document = preprocess_document(document)
#             # print(preprocess_document)
            
            
#             # # Apply AI editing
#             # edited_text = apply_ai_editing(document)

#             # # # Postprocess the edited text
#             # # processed_text = self.postprocess_text(edited_text)

#             # # # Save the edited document
#             # # self.save_edited_document(processed_text, file_name)

#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)




# def home(request):
#     file_name = 'data_ingestion.pdf'
#     context = {'file_name': file_name}
#     return render(request, 'home.html', context)