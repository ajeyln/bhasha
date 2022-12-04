import sys
import string
from random import randint, shuffle
from pathlib import Path
import os 


OUTPUT_FOLDER_NAME="PRACTICE_OUTPUT_FOLDER"

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

def prepare_question_source(para, index):
  sentences = list(filter(lambda x : x != '', para.split('.')))
  choice=randint(1, len(sentences)-2)
  answer=sentences[choice] + "."
  sentences[choice]=f'---<b>({index})---</b><input size ="1" maxlength="2" type="text" id=t_{index}>'
  lastItem = f"{sentences[-1]}.\n\n"
  sentences[-1] = lastItem
  source_para = ".".join(sentences)
  return f'<p id=p_{index}>{source_para}</p>', answer



def prepare_question_paper(source, options, filename):
#  for opt in options :
#    print(opt)

  with open(os.path.join("resources", "s_style.css")) as f:
    htmlStyle = f.read()
  
  with open(os.path.join("resources", "s_script.js")) as f:
    htmlScript = f.read()
  
  if not os.path.exists(OUTPUT_FOLDER_NAME):
    os.makedirs(OUTPUT_FOLDER_NAME)
  question_file = "FillInTheBlanks-Type-I-Questions.html"
  
  print(f"Output file:- {os.path.join(OUTPUT_FOLDER_NAME, question_file)}")
  #question_file = "test.html"
  with open(os.path.join(OUTPUT_FOLDER_NAME, question_file), 'w', encoding="utf8") as writer:
    indexOrder=[]
    #writer.write('<link rel="icon" href="resources\s_logo.png">')
    writer.write('<head>')
    writer.write('<title>Fill in the Blanks Type 1 </title>')
    writer.write('</head>')
    writer.write(htmlStyle)
    writer.write(htmlScript)
    #writer.write('<script type="text/javascript" src="script.js"></script>')
    writer.write("<br><br>")

    writer.write(f'<p > Source File : {filename}</p>')
    
    writer.write('<p id="score" ></p>')
    writer.write('<p id="answer_key" style="font-size: 150%; color:green"></p>')

    # write global 
    writer.write('<div align="right"> <span id="time" style="font-size: 150%; background: black; color:red">13:00</span></div>')

    writer.write('<body style="background-color:powderblue;">')
    #writer.write('<img src="logo.png" alt="HTML5 Icon" style="width:80px;height:80px;">')
    writer.write('<br>')
    writer.write('<br>')
    writer.write('<div class="float-container">')
    #here comes questions
 
    #here comes options
    writer.write('<div class="float-child green">')
    writer.write('<h3> Here are missing sentences corresponding to content. <br> Please fill in the blanks with right number. </h3>')
    writer.write('<ol>')
    for opt in options :
      writer.write('<li>')
      (stmt, index)= opt
      writer.write(str(stmt))
      #writer.write(str(index))
      indexOrder.append(index)
      writer.write('<br>')
      writer.write('<br>')
      writer.write('<br>')
      writer.write('</li>')
    writer.write('</ol>')
    #writer.write(str(indexOrder))
    writer.write('</div>')


    writer.write('<div class="float-child2 magenta">')
    writer.write('<h3> Here is the text content with missing sentences.  <br> Please read carefully. </h3>')
    writer.writelines(source)
    writer.write('</div>')

    writer.write('</div>')

    writer.write(f'<button type="button" onclick="submitAndValidate({str(indexOrder)})">Submit Answers!</button>')
    
    writer.write('</body>')

if __name__ == '__main__':
  print(f"Given file name is :{sys.argv[1]} ")

  filePath = sys.argv[1]
  if not check_file_exists(filePath) :
    print (f"Given file :{sys.argv[1]} does not exist ")
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
  prepare_question_paper(questionPara, options, filePath)