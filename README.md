# datafun-03-project
Data Analytics Fundamentals - Module 3

Clone YOUR New Repo to Your Machine
On your machine, open a PowerShell terminal. Execute the commands one at a time to:
1.	Change directory to the root (C:)
2.	Create a Projects folder (if you don't already have one)
3.	Clone YOUR repo into your C:\Projects.
4.	Change directory into your new repository folder.
5.	Open your new folder in VS Code.
6.	Opens current directory folder in VS Code
cd \
mkdir Projects
cd Projects
git clone https://github.com/**youraccount**/**your-repo-name**
cd **your-repo-name**
code .

Create a place for our local project virtual environment
1.	With your project folder open in VS Code, open a new terminal (CTRL ` or menu: Terminal / New Terminal.
2.	Create a local virtual environment folder named .venv using the following command. The first works on Windows, the second on Mac/Linux:
py -m venv .venv
Details: The command starts python, the -m venv means "run venv as a module", and .venv is the name of the subfolder that will hold our project virtual environment. 
This is generally a one-time effort. Once you create a .venv folder in your project repository, you shouldn't need to create it again unless things get messed up. You can always delete the folder and recreate it. It's fine to delete .venv folder for any inactive project.

Update Requirements text
py -m pip install --upgrade -r requirements.txt	

Create a new file named .gitignore in the root folder of our project. 
# This .gitignore file lists content that does NOT need to be tracked in the project history

# Python virtual environment
.venv/

# Visual Studio Code settings and workspace
.vscode/

# Compiled Python files
__pycache__/

# macOS system files
.DS_Store

1. Git add the files to source control
2. Git commit the files as a named set of changes
3. Git push the files to GitHub

git add .
git commit -m "Add .gitignore"
git push -u origin main