# zk-copyright

zk-copyright repository provides an E2E pipeline, supported by picozk, to test differential privacy under Zero-Knowledge Proof.

----
## Project Objective
This software is designed to demonstrate two simplified court cases of copy-right infringement discussed in <a href="https://arxiv.org/abs/2206.01230"> this paper </a>. 
Both cases either prove or disprove the similarity of the processes to produce outputs, over which two parties - termed as the ’producer’ and ’reproducer’ in our program - are disputing.
The first program, which we refer to ’mad-libs example’, is inspired by the Proctor-Gamble case in the paper. 
It is a ’mad-libs’ style program that uses a hardcoded, short string to choose between a limited number of permutations of a set of text strings. 

Only the producer is given pre-filled mad-libs, wherein only the last few words differ from the actual output. 
Following different steps, both the producer and the reproducer output filled madlibs.

The second program is a toy version of Feist’s case regarding telephone directories in the paper.
The dictionary consists of names and phone numbers, including honey entries, and both the producer and the reproducer output lexicographically ordered dictionary by phone numbers in their respective ways. 
Only the producer possesses a dictionary that is pre-sorted alphabetically by name



## Quick Navigation

- [Use Docker](#-use-docker)
- [Run Locally](#-run-locally)
- [Different Setup](#-different-setup)


## 🐳 [Use Docker](#-use-docker)

#### 🚧 Build Docker Image and Run Container

##### <ins><i> Option A Use published docker image </i> </ins>

Run this line of code in the command line:
```
docker run --platform linux/amd64 -it hicsail/zk-copyright:main   
```

##### <ins><i> Option B Clone Repo </i> </ins>

Run the following in the command line to get the container up and running:
```
git clone https://github.com/hicsail/zk-copyright.git # Clone the repository
cd zk-copyright                                       # Move into the root directory of the project
docker-compose up -d --build                          # Inside the root directory, run the build image:
```

#### 🖥️ Getting started

##### <ins><i> Step1: Enter Docker Shell</i> </ins>

Since you have a running container, you can subsequently run the following command in your terminal to start Docker Shell:

```
docker exec -it <containerID> bash
```

You can get a container-ID from the docker desktop app by clicking the small button highlighted in the red circle
<ul>
    <img width="1161" alt="image" src="https://user-images.githubusercontent.com/62607343/203409123-1a95786f-8b2a-4e71-a920-3a51cf50cf0f.png">
</ul>

If you see something like the following in your command line, you are successfully inside the docker shell
<ul>
<img width="300" alt="image" src="https://user-images.githubusercontent.com/62607343/203413803-19021cb9-07ba-4376-ade0-dbdc6c8506c5.png">
</ul>


##### <ins><i> Step2: Install wiztoolkit</i> </ins>

We are using Fire Alarm, one of wiztoolkit packages.
After entering the container, clone wiztoolkit repo and run the following commands to install wiztoolkit:

(* You might need to set up ssh key - Follow <a href="https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent?platform=linux"> the instruction </a>)

```
git clone git@github.mit.edu:sieve-all/wiztoolkit.git
cd wiztoolkit
make
make install
```

### 🏋️‍♀️ Run shell script

Now all setups are done for you to run your Python script inside the docker shell.
Run the following command in the docker shell, and you will see your choice of the Python scripts,<a href="https://github.com/hicsail/zk-copyright/blob/main/copyright_madlibs.py"> copyright_madlibs.py</a> or <a href="https://github.com/hicsail/zk-copyright/blob/main/copyright_phonebook.py">    copyright_phonebook.py</a>, generating zk statements and fire-alarm checks the format of the statements:

```
/bin/bash ./run_IR0.sh -f copyright_madlibs
/bin/bash ./run_IR0.sh -f copyright_phonebook
```

## 👨‍💻 [Run Locally](#-run-locally)

This option doesn't require Docker, while it focuses on running the Python scripts, skipping setting Fire Alarm.

Run this in the command line:
```
git clone git@github.com:hicsail/zk-copyright.git
```

Move into the root directory of the project and install dependencies

```
cd zk-copyright
git clone https://github.com/uvm-plaid/picozk.git
python3 -m venv venv           # or pypy3 -m venv myenv
source venv/bin/activate       # or source myenv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install picozk/.
```


Run either of these lines in the command line:

```
python3 copyright_madlibs.py.py
python3 copyright_phonebook.py.py
```

## 🧪 [Different Setup](#-different-setup)

Both of the current files generate synthetic inputs: one creates a dictionary of names and phone numbers, and the other generates Mad Libs.


You can change the size of these inputs by modifying a variable called 'scale' in <a href="https://github.com/hicsail/zk-copyright/blob/3d53b58b88303072ed9fdcb51532cdb0018e6ade/copyright_madlibs.py#L6"> copyright_madlibs.py </a> and <a href="https://github.com/hicsail/zk-copyright/blob/3d53b58b88303072ed9fdcb51532cdb0018e6ade/copyright_phonebook.py#L6">copyright_phonebook.py </a>, which defaults to 5.

<img width="603" alt="image" src="https://github.com/hicsail/zk-copyright/assets/62607343/5e142ede-a6de-4e53-8784-9e11762b08e2">

For the phonebook system, generates a dictionary with a number of entries equal to the 'scale' value and a max(1, 10%) of honey entries. This means that the default configuration returns a dictionary with 5 entries and 1 honey entry.

The Mad Libs system, on the other hand, produces a Mad Libs statement of 'scale' length with half of the words being blanks. Unless the scale value is changed, it will generate 5-word length Mad Libs with 2 blanks.
