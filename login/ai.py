import os
from django.conf import settings
import filetype

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

# def preprocess_document(document):
#     # Implement preprocessing tasks here
#     # For example, you can clean up the document, remove unwanted characters,
#     # or transform the data as needed
    
#     # For demonstration purposes, let's assume we want to convert the document content to lowercase
#     preprocessed_document = document.lower()
    
#     return preprocessed_document


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