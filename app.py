from flask import Flask, render_template, request, json
import time
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
matplotlib.use('agg')
import datetime

app = Flask(__name__)
application = app

def ip2decimal(ip_address):
    parts = list(map(int, ip_address.split('.')))
    decimal = 0
    for part in parts:
        decimal = decimal * 256 + part
    return decimal

def decimal2ip(decimal):
    parts = []
    for i in range(4):
        parts.insert(0, str(decimal % 256))
        decimal //= 256
    return '.'.join(parts)

voices = []
with open("logs/state_voices_logs") as file:
   voices = json.load(file)

chat = ""
with open("logs/state_chat_logs") as file:
   chat = file.read()

lines = []
with open("logs/state_ips_voices_logs") as file:
   lines = file.readlines()

ips = list(map(int, lines[0].strip().split(',')))
ips_voices = list(map(int, lines[1].strip().split(',')))

@app.route('/')
def main():
   return render_template("index.html")

@app.route('/ips_rating')
def render_ips_rating():
   return render_template("ips_rating.html")

@app.route('/rivals_rating')
def render_rivals_rating():
   return render_template("rivals_rating.html")
   
@app.route('/update_ips_rating', methods=['POST'])
def update_ips_graph():
   if request.method == 'POST':
      lines = []
      with open("logs/ips_voices_logs") as file:
         lines = file.readlines()

      count_leads = 5
      leaders_ips = [-1] * count_leads
      max_ips = [-1] * count_leads
      times = []
      ips_state = [[]]
      ips_voices = [[]]
      count = 0
      for i in range(0, len(lines), 3):
         times.append(lines[i])
         ips_state.append(list(map(int, lines[i + 1].strip().split(','))))
         ips_voices.append(list(map(int, lines[i + 2].strip().split(','))))
         count += 1

      for i in range(len(ips_voices[count])):
         for j in range(count_leads):
            if max_ips[count_leads - j - 1] < ips_voices[count][i]:
               for k in range(count_leads - j - 2):
                  leaders_ips[k] = leaders_ips[k + 1]
                  max_ips[k] = max_ips[k + 1]
               leaders_ips[count_leads - j - 1] = i
               max_ips[count_leads - j - 1] = ips_voices[count][i]
               break

      x_dates = [datetime.datetime.strptime(date, "%m/%d/%Y %H:%M:%S\n") for date in times]

      for j in range(count_leads - 1, 0, -1):
         if (leaders_ips[j] == -1):
            continue
         y_dates = []
         for i in range(1, count + 1, 1):
            y_dates.append(ips_voices[i][leaders_ips[j]])
         
         leader_info = str(count_leads - j) + ": " + str(decimal2ip(ips_state[count][leaders_ips[j]]))
         plt.plot(x_dates, y_dates, marker='.', label=leader_info)

      plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%m/%d/%Y %H:%M:%S"))
      plt.gcf().autofmt_xdate()
      plt.xlabel('time')
      plt.ylabel('voices')
      plt.title('IP rating')
      plt.legend()
      plt.grid(True)
      plt.savefig("static/ips_graph.png")
      plt.clf()
      return {}
   

@app.route('/btn', methods=['POST'])
def btn():
   global voices
   btn_ind = (int)(request.values.get('btn_ind'))
   if request.method == 'POST':
      if btn_ind != -1:
         voices[btn_ind - 1] += 1
         update_ips_voices(request.remote_addr)
         log_ips_voices()
         log_btn(btn_ind)
         log_state()

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
      log_msg()
      log_state()

   return {"chat":chat}

@app.route('/process', methods=['POST'])
def process():
   global voices
   return {"voices1":voices[0], "voices2":voices[1], "voices3":voices[2], "voices4":voices[3], "chat":chat}

def update_ips_voices(request_addr):
   global ips
   global ips_voices

   dec_addr = ip2decimal(request_addr)
   for i in range(len(ips)):
      if ips[i] == dec_addr:
         ips_voices[i] += 1
         return
   ips.append(dec_addr)
   ips_voices.append(1)

def log_ips_voices():
   global chat
   global ips
   global ips_voices
   named_tuple = time.localtime()
   time_string = time.strftime("%m/%d/%Y %H:%M:%S", named_tuple)
   rival_logs_file = open("logs/ips_voices_logs", "a+")
   logs_str = str(time_string) + '\n' 
   logs_str += ",".join([str(element) for element in ips]) + '\n'
   logs_str += ",".join([str(element) for element in ips_voices]) + '\n'
   rival_logs_file.write(logs_str)
   rival_logs_file.close()

def log_btn(btn_ind):
   global voices
   named_tuple = time.localtime()
   time_string = time.strftime("%m/%d/%Y %H:%M:%S", named_tuple)

   btn_logs_file = open("logs/voices_logs", "a+")
   logs_str = str(time_string) + "\t" + str(btn_ind) + "\t" + "\t".join([str(element) for element in voices]) + '\n'
   btn_logs_file.write(logs_str)
   btn_logs_file.close()

def log_msg():
   global chat
   named_tuple = time.localtime()
   time_string = time.strftime("%m/%d/%Y %H:%M:%S", named_tuple)
   msg_logs_file = open("logs/messages_logs", "a+")
   logs_str = str(time_string) + '\n' + chat + "\n"
   msg_logs_file.write(logs_str)
   msg_logs_file.close()

def log_state():
   global voices
   global chat
   global ips
   global ips_voices

   voices_logs_file = open("logs/state_voices_logs", "w")
   voices_logs_file.write("[" + ",".join([str(element) for element in voices]) + "]")
   voices_logs_file.close()

   chat_logs_file = open("logs/state_chat_logs", "w")
   logs_str = chat + "\n"
   chat_logs_file.write(logs_str)
   chat_logs_file.close()

   chat_logs_file = open("logs/state_ips_voices_logs", "w")
   logs_str = ",".join([str(element) for element in ips]) + '\n'
   logs_str += ",".join([str(element) for element in ips_voices]) + '\n'
   chat_logs_file.write(logs_str)
   chat_logs_file.close()

if __name__ == "__main__":
   app.run(debug=True)