from flask import Flask, render_template, redirect, request, url_for
import time

app = Flask(__name__)

data = []
with open("logs/voices_logs") as f:
    for line in f:
        data.append([float(x) for x in line.split()])
voices1 = (int)(data[0][0])
voices2 = (int)(data[1][0])
voices3 = (int)(data[2][0])
voices4 = (int)(data[3][0])

@app.route('/', methods=['POST', 'GET'])
def main():
   global voices1
   global voices2
   global voices3
   global voices4

   if request.method == 'POST':
         all_logs_file = open("logs/all_logs", "a+")
         named_tuple = time.localtime()
         time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
         sum_voices = voices1 + voices2 + voices3 + voices4

         if request.form.get('btn1') == 'btn1':
            voices1 += 1
            logs_str = 'sum\t' + str(sum_voices) + '\tbtn1\t' + str(voices1) + "\ttime\t" + str(time_string) + "\n"

         elif request.form.get('btn2') == 'btn2':
            voices2 += 1
            logs_str = 'sum\t' + str(sum_voices) + '\tbtn2\t' + str(voices2) + "\ttime\t" + str(time_string) + "\n"

         elif request.form.get('btn3') == 'btn3':
            voices3 += 1
            logs_str = 'sum\t' + str(sum_voices) + '\tbtn3\t' + str(voices3) + "\ttime\t" + str(time_string) + "\n"

         elif request.form.get('btn4') == 'btn4':
            voices4 += 1
            logs_str = 'sum\t' + str(sum_voices) + '\tbtn4\t' + str(voices4) + "\ttime\t" + str(time_string) + "\n"

         all_logs_file.write(logs_str)
         all_logs_file.close()

         voices_logs_file = open("logs/voices_logs", "w")
         logs_str = str(voices1) + "\n" + str(voices2) + "\n" + str(voices3) + "\n" + str(voices4)
         voices_logs_file.write(logs_str)
         voices_logs_file.close()
         return redirect(request.url)

   return render_template("index.html", voices1=voices1, voices2=voices2, voices3=voices3, voices4=voices4)

if __name__ == "__main__":
   app.run(debug=True)