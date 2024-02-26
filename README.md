# zk-copyright

zk-copyright project provides an E2E pipeline, under picoZK, to test copyright infringement under Zero-Knowledge Proof.

----

## 📖 Setting up

<strong> Option A Use published docker image </strong>

Run this in the command line:
```
docker run --platform linux/amd64 -it hicsail/zk-copyright:main      
```

<strong> Option B Clone Repo </strong>

Run this in the command line:
```
git clone git@github.com:hicsail/zk-copyright.git
```

Move into the root directory of the project

```
cd zk-copyright
```

Inside the root directory, run the build image:

```
docker-compose up -d --build
```

Now you have a brand new container running on your machine



## 🖥️ Getting started

<strong> Enter Docker Shell</strong> 

Since you have a running container, you can subsequently run the following command in your terminal to start Docker Shell:

```
docker exec -it <containerID> bash
```

You can get a containerID from the docker desktop app by clicking the small button highlighted in the red circle
<ul>
    <img width="1161" alt="image" src="https://user-images.githubusercontent.com/62607343/203409123-1a95786f-8b2a-4e71-a920-3a51cf50cf0f.png">
</ul>

If you see something like the following in your command line, you are successfully inside the docker shell
<ul>
<img width="300" alt="image" src="https://user-images.githubusercontent.com/62607343/203413803-19021cb9-07ba-4376-ade0-dbdc6c8506c5.png">
</ul>


<strong> Install wiztoolkit</strong> 

Inside the container, clone wiztoolkit repo and move into wiztoolkit:

(*) You might need to set up ssh key - Follow <a href="https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent?platform=linux"> the instruction </a>

```
git clone git@github.mit.edu:sieve-all/wiztoolkit.git
cd wiztoolkit
```

And run the following commands to install wiztoolkit (Backend for IR0):

```
make
make install
```

## 🏋️‍♀️ Run your Python script and firealarm test module inside the container

Run the following command in the docker shell: 

<strong> Madlibs example 📄 </strong> :
```
/bin/bash ./run_IR0.sh -f copyright_madlibs.py 
```
This runs <a href="https://github.com/hicsail/zk-copyright/blob/main/copyright_madlibs.py">    copyright_madlibs.py</a> and checks the format of output statements<br>

<strong> Phonebook Example☎️ </strong> :
```
/bin/bash ./run_IR0.sh -f copyright_phonebook.py
```
This runs <a href="https://github.com/hicsail/zk-copyright/blob/main/copyright_phonebook.py">    copyright_phonebook.py</a> and checks the format of output statements <br>

<strong> Alternative Execution </strong> :<br>
You can run just the Python statement as below inside the container:
```
python3 copyright_madlibs.py.py
python3 copyright_phonebook.py.py
```
