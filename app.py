from flask import Flask, render_template, request, json, redirect
import time

app = Flask(__name__)
application = app

voices = []
with open("logs/state_voices_logs") as file:
   voices = json.load(file)

chat = ""
with open("logs/state_chat_logs") as file:
   chat = file.read()

@app.route('/')
def main():
   return render_template("index.html")

@app.route('/ips_rating.html')
def render_ips_rating():
   return render_template("ips_rating.html")

@app.route('/rivals_rating.html')
def render_rivals_rating():
   return render_template("rivals_rating.html")

@app.route('/btn', methods=['POST'])
def btn():
   global voices
   btn_ind = (int)(request.values.get('btn_ind'))
   if request.method == 'POST':
      if btn_ind != -1:
         voices[btn_ind - 1] += 1
         logging_btn(btn_ind)
         logging_state()

   return {"voices1":voices[0], "voices2":voices[1], "voices3":voices[2], "voices4":voices[3]}

@app.route('/msg', methods=['POST'])
def msg():
   global chat
   message = request.values.get('msg')
   if (message == ""):
      return {"chat":chat}
   
   if request.method == 'POST':
      named_tuple = time.localtime()
      time_string = time.strftime("%m/%d/%Y %H:%M:%S", named_tuple)
      chat += "from " + str(request.remote_addr) + "\tat " + str(time_string) + "<br/>" + "\n"
      message_width = 34
      for i in range(int(len(message) / message_width) + 1):
         left_border  = min(len(message), i * message_width)
         right_border = min(len(message), (i + 1) * message_width )
         chat += str(message[left_border:right_border]) + "<br/>" + "\n"
      logging_msg()
      logging_state()

   return {"chat":chat}

@app.route('/process', methods=['POST'])
def process():
   global voices
   return {"voices1":voices[0], "voices2":voices[1], "voices3":voices[2], "voices4":voices[3], "chat":chat}

def logging_btn(btn_ind):
   global voices
   named_tuple = time.localtime()
   time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)

   btn_logs_file = open("logs/voices_logs", "a+")
   logs_str = str(time_string) + "\t" + str(btn_ind) + "\t" + "\t".join([str(element) for element in voices]) + '\n'
   btn_logs_file.write(logs_str)
   btn_logs_file.close()

def logging_msg():
   global chat
   named_tuple = time.localtime()
   time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
   msg_logs_file = open("logs/messages_logs", "a+")
   logs_str = str(time_string) + '\n' + chat + "\n"
   msg_logs_file.write(logs_str)
   msg_logs_file.close()

def logging_state():
   global voices
   global chat
   voices_logs_file = open("logs/state_voices_logs", "w")
   voices_logs_file.write("[" + ",".join([str(element) for element in voices]) + "]")
   voices_logs_file.close()
   chat_logs_file = open("logs/state_chat_logs", "w")
   chat_logs_file.write(chat + "\n")
   chat_logs_file.close()

if __name__ == "__main__":
   app.run(debug=True)