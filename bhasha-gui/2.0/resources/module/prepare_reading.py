import sys
import string
from random import randint, shuffle
from pathlib import Path
import os, json


#GENERIC
def check_file_exists(filePath):
      my_file = Path(filePath)
      return my_file.is_file()

def get_paragraphs_from_file(filePath):
  with open(filePath, encoding="utf8") as f:
    text = f.read()
    paragraphs = list(filter(lambda x : x != '', text.split('\n\n')))
    for para in paragraphs:
      para = para.strip("\n")
      para = para.strip("\t")
      para = para.replace('\n','')
      para = para.replace('\t','')
    return paragraphs

#HTML FOR DOWNLOAD
def download(filePath, OUTPUT_FOLDER_NAME="PRACTICE_OUTPUT_FOLDER") : 
    if not check_file_exists(filePath) :
        #print (f"Given file :{sys.argv[1]} does not exist ")
        sys.exit()
    questionPara=[]
    options=[]
    truth=[]
    alpha_letters = list(string.ascii_lowercase)
    paras=get_paragraphs_from_file(filePath)
    for i,p in enumerate(paras):
        index=alpha_letters[i]
        s, a=prepare_question_source(p, index)
        questionPara.append(s)
        options.append((a, index))
    shuffle(options)
    prepare_question_paper(questionPara, options, filePath, OUTPUT_FOLDER_NAME)

def prepare_question_paper(source, options, filename,OUTPUT_FOLDER_NAME="PRACTICE_OUTPUT_FOLDER" ):
  with open(os.path.join("resources", "html", "s_style.css")) as f:
    htmlStyle = f.read()
  with open(os.path.join("resources", "html", "s_script.js")) as f:
    htmlScript = f.read()
  if not os.path.exists(OUTPUT_FOLDER_NAME):
    os.makedirs(OUTPUT_FOLDER_NAME)
  question_file = "Reading-1.html"
  with open(os.path.join(OUTPUT_FOLDER_NAME, question_file), 'w', encoding="utf8") as writer:
    indexOrder=[]
    writer.write('<head>')
    writer.write('<title>Fill in the Blanks Type 1 </title>')
    writer.write('</head>')
    writer.write(htmlStyle)
    writer.write(htmlScript)
    writer.write("<br><br>")
    writer.write(f'<p > Source File : {filename}</p>')
    writer.write('<p id="score" ></p>')
    writer.write('<p id="answer_key" style="font-size: 150%; color:green"></p>')
    # write global 
    writer.write('<div align="right"> <span id="time" style="font-size: 150%; background: black; color:red">13:00</span></div>')
    writer.write('<body style="background-color:powderblue;">')
    writer.write('<br>')
    writer.write('<br>')
    writer.write('<div class="float-container">')
    #here comes options
    writer.write('<div class="float-child green">')
    writer.write('<h3> Here are missing sentences corresponding to content. <br> Please fill in the blanks with right letter in the right pane. </h3>')
    writer.write('<ol>')
    for opt in options :
      writer.write('<li>')
      (stmt, index)= opt
      writer.write(str(stmt))
      indexOrder.append(index)
      writer.write('<br>')
      writer.write('<br>')
      writer.write('<br>')
      writer.write('</li>')
    writer.write('</ol>')
    writer.write('</div>')
    writer.write('<div class="float-child2 magenta">')
    writer.write('<h3> Here is the text content with missing sentences.  <br> Please read carefully. </h3>')
    writer.writelines(source)
    writer.write('</div>')
    writer.write('</div>')
    writer.write(f'<button type="button" onclick="submitAndValidate({str(indexOrder)})">Submit Answers!</button>')
    writer.write('</body>')


#R1 READING (Missing Sentences)
def prepare_question_source_text(para, index):
    sentences = list(filter(lambda x : x != '', para.split('.')))
    choice=randint(1, len(sentences)-2)
    answer=sentences[choice] + "."
    sentences[choice]=f"<b style='color:red'>---({index})---</b>"
    lastItem = f"{sentences[-1]}.\n </p>"
    firstItem = f"<p style='color:blue'>{sentences[0]}"
    sentences[0] = firstItem
    sentences[-1] = lastItem
    source_para = ".".join(sentences)
    return f'{source_para}', answer

def prepare_html_content(filePath, OUTPUT_FOLDER_NAME="PRACTICE_OUTPUT_FOLDER"):
    source, options = return_text(filePath, OUTPUT_FOLDER_NAME)
    return_html_content = "<html><body background-color= '#E6E6FA'>"
    return_html_content += f'<p > Source File : {filePath}</p>'
    return_html_content += '<h3 style="color:red"> Here is the text content with missing sentences.  <br> Please scroll down and read carefully. <br>Also assign correct letters in the right pane for given options. </h3>'
    return_html_content += "\n\n\n".join(source)
    return_html_content +='</div></body></html>'
    return return_html_content, options
    
def return_text(filePath, OUTPUT_FOLDER_NAME="PRACTICE_OUTPUT_FOLDER") :
    if not check_file_exists(filePath) :
        sys.exit()
    questionPara=[]
    options=[]
    truth=[]
    alpha_letters = list(string.ascii_lowercase)
    paras=get_paragraphs_from_file(filePath)
    for i,p in enumerate(paras):
        index=alpha_letters[i]
        s, a=prepare_question_source_text(p, index)
        questionPara.append(s)
        options.append((a, index))
    return questionPara, options

def prepare_question_source(para, index):
  sentences = list(filter(lambda x : x != '', para.split('.')))
  choice=randint(1, len(sentences)-2)
  answer=sentences[choice] + "."
  sentences[choice]=f'---<b>({index})---</b><input size ="1" maxlength="2" type="text" id=t_{index}>'
  lastItem = f"{sentences[-1]}.\n\n"
  sentences[-1] = lastItem
  source_para = ".".join(sentences)
  return f'<p id=p_{index}>{source_para}</p>', answer



#R2 READING (Missing words)
def get_r2_html_content(filePath):
    return_html_content = ""
    with open(filePath, encoding="utf8") as f:
        text = f.read()
    sentences = list(filter(lambda x : x != '', text.split('.')))
    source, options = prepare_r2_sentences(sentences)
    return_html_content = "<html><body background-color= '#E6E6FA'>"
    return_html_content += f'<p > Source File : {filePath}</p>'
    return_html_content += '<div"> <h3 style="color:red"> Here is the text content with missing words.  <br> Please scroll down and read carefully. <br>Also assign correct letters in the right pane for given options. </h3>'
    return_html_content += f"\n\n\n{source}"
    return_html_content +='<div></body></html>'
    return return_html_content, options

def find_sentence_indices(ss):
    total_blanks = 10
    indices_set = set()
    sentences_len = len(ss)
    looper = 0
    if  sentences_len < total_blanks:
        print("There are less number of sentences")
        return False 
    else:
        while looper < total_blanks :
            choice=randint(0, sentences_len-1)
            if not ss[choice].isspace() and  choice not in indices_set and len(ss[choice])>2:
                indices_set.add(choice)
                looper = looper +1
    return sorted(list(indices_set))
   

def prepare_r2_sentences(ss):
    total_missing_words = 10
    answer_word_set = set()
    answer_key = []
    index = 0
    i_list=find_sentence_indices(ss)
    alpha_letters = list(string.ascii_lowercase)
    source_para = ""
    for i in i_list :
        words = ss[i].split()
        while True :
            choice=randint(1, len(words)-2)
            if words[choice].lower() not in answer_word_set and len(words[choice])>2:
                answer_word_set.add(words[choice].lower())
                answer_key.append((words[choice],alpha_letters[index]))
                words[choice]=f"<b style='color:red'>---({alpha_letters[index]})---</b>"
                ss[i]=' '.join(words)+"."
                index = index +1
                break
    text_content = ".".join(ss)
    for para in list(filter(lambda x : x != '', text_content.split('\n'))):
        sentences=list(filter(lambda x : x != '', para.split('.')))
        lastItem = f"{sentences[-1]}</p>"
        firstItem = f"<p style='color:blue'>{sentences[0]}"
        sentences[0] = firstItem
        sentences[-1] = lastItem
        source_para += ".".join(sentences) +"\n"
    return source_para, answer_key


#R3 READING (classifieds)
def return_classifieds_question(filePath):
    total_questions = 5
    answer_key = []
    indices_set = set()
    looper = 0
    alpha_letters = list(string.ascii_lowercase)

    if not check_file_exists(filePath) :
        sys.exit()    
    with open(filePath, "r", encoding='utf-8') as fp:
        classifieds = json.load(fp)
    
    cl_len = len(classifieds)

    if   cl_len < total_questions:
        print("There are less number of sentences")
        return False 
    else:
        while looper < total_questions :
            choice=randint(0, cl_len-1)
            if choice not in indices_set:
                indices_set.add(choice)
                looper = looper +1
        return_html_content = "<html><body background-color= '#E6E6FA'>"
        return_html_content += f'<p > Source File : {filePath}</p>'
        return_html_content += '<div"> <h3 style="color:red"> Here are different madeup classifieds.  <br> Please scroll down and read carefully. <br>Also assign correct letters in the right pane for given options. </h3><br>'
        for ind, index in enumerate(indices_set):
            return_html_content += f"<b style='color:red'> {alpha_letters[ind]} </b>"
            return_html_content += f"<p style='color:blue'>{classifieds[index]['text']}</p>"
            answer_key.append((classifieds[index]['query'], alpha_letters[ind]))
    return_html_content +='<div></body></html>'
    return return_html_content, answer_key



if __name__ == '__main__':
    filePath = sys.argv[1]
    s, a = return_classifieds_question(filePath)
    print(s,a)

    