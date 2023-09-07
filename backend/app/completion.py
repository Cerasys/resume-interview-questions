import PyPDF2
import os
import openai
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())  # read local .env file
openai.api_key = os.environ["OPENAI_API_KEY"]


# save the extracted data from pdf to a txt file
# we will use file handling here
# dont forget to put r before you put the file path
# go to the file location copy the path by right clicking on the file
# click properties and copy the location path and paste it here.
# put "\\your_txtfilename"
def readPdf(file_path):
    pdf_obj = open(file_path, "rb")
    pdf_reader = PyPDF2.PdfReader(pdf_obj)
    result = ""
    for page in pdf_reader.pages:
        result += page.extract_text() + "\n"
    return result


def generateQuestions(resume_path, jd_path):
    # create file object variable
    # opening method will be rb
    resume = readPdf(resume_path)
    print(resume)
    print(len(resume))

    # call to LLM to process highlights and questions to ask
    resume_summary_prompt = "Given a resume, summarize it in 4-5 sentences" + "\n" + "Resume: " + resume

    print("Querying OpenAI for summarized resume now...\n")
    response = openai.ChatCompletion.create(
        temperature=0,
        model="gpt-3.5-turbo-0613",
        messages=[{"role": "user", "content": resume_summary_prompt}],
    )
    summarized_resume = response["choices"][0]["message"]["content"]
    print(summarized_resume)
    print(len(summarized_resume))

    # create file object variable
    # opening method will be rb
    jd = readPdf(jd_path)

    print(jd)
    print(len(jd))

    # call to LLM to process highlights and questions to ask
    jd_summarize_prompt = (
        "Given a job description, summarize it into 3-5 key technical requirements" + "\n" + "Job Description: " + jd
    )

    print("Querying OpenAI for job description summary now...\n")
    response = openai.ChatCompletion.create(
        temperature=0,
        model="gpt-3.5-turbo-0613",
        messages=[{"role": "user", "content": jd_summarize_prompt}],
    )
    summarized_jd = response["choices"][0]["message"]["content"]
    print(summarized_jd)

    # call to LLM to process highlights and questions to ask
    interview_prompt = (
        "You are an experienced interviewer. Given a resume and a job description, generate a list of 10 open-ended questions to determine the skill and fit of the candidate for the role. Questions should try to relate the candidate's experience to the job description\n"
        + "Resume: "
        + summarized_resume
        + "\n"
        + "Job Description: "
        + summarized_jd
    )

    print("Querying OpenAI for questions now...\n")
    response = openai.ChatCompletion.create(
        temperature=0,
        model="gpt-4-0613",
        messages=[{"role": "user", "content": interview_prompt}],
    )

    question_list = response["choices"][0]["message"]["content"]

    print(question_list)
    return question_list


generateQuestions("./app/Downloads/resume.pdf", "./app/Downloads/jobDescription.pdf")
