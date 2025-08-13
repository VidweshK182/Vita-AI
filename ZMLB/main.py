import multiprocessing
import subprocess
import time

def run_backend():
    subprocess.run([
        "python3",
        "-m",
        "ZMLB.backend.api"
    ])
    
# def run_frontend():
#     subprocess.Popen(
#         ["npm", "run", "dev"],
#         cwd="zmlf/app",
#         stdout=subprocess.PIPE,
#         stderr=subprocess.PIPE
#     )
# python3 -m zmlb.backend.api
# streamlit run streamlit_chatbot.py

def run_chatbot():
    subprocess.run([
        "streamlit",
        "run",
        # "ZMLB/vita-health-chatbot/streamlit_chatbot.py"
        "vita-health-chatbot/streamlit_chatbot.py"

    ])

if __name__ == "__main__":
    backend_process = multiprocessing.Process(target=run_backend)
    chatbot_process = multiprocessing.Process(target=run_chatbot)

    backend_process.start()
    time.sleep(2)
    chatbot_process.start()


    backend_process.join()
    chatbot_process.join()
