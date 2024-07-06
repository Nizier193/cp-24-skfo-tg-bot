from services.RAGApp import RagAPP
import os

flow = RagAPP()
for filename in os.listdir('files_to_load'):
    flow.add_file(os.path.join('files_to_load', filename))