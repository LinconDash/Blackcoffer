from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

tasks = []  
task_counter = 0 

@app.route("/", methods=["GET", "POST"])
def index():
    global task_counter
    if request.method == "POST":
        task_text = request.form.get("task")
        if task_text:
            tasks.append({"id": task_counter, "text": task_text})
            task_counter += 1  
    return render_template("index.html", tasks=tasks)

@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task["id"] != task_id]  
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)