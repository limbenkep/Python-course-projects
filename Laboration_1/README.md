# Laboration 1

## Environment & Tools 
Window 10 pro, PyCharm 2021.2.1(Professional edition), Python 3.9.6,git version 2.33.0.windows.2 

## Purpose
The purpose of the laboration is to provide practical experience in regards to…
- Bitbucket and simple Git commands!
- working with basic data types, operators and conditional statements!
- Markdown syntax!

## Procedure
To fullfill the aim of this lab I did the following..
- Clone my personal repository from bitbucket. This was achieved by opening repository in bitbucket, \
clicking on clone and copy the command. Git Bash is then opened in the local folder where the repository is to be cloned, the command 
- Create and checkout a new branch named laboration_1 using command *git checkout -b laboration_1*
- Set an uptream for the new branch. We were to use command *git push –-set-upstream origin laboration_1*. But this command generated the error so I pushed through PyCharm.
- Study and implement pseudocode found in Laboration_1/assigment.py.
- Stage and commit all changes using command *commit -a -m "commit message"*
- Fill this ReadMe.md document using Markdown syntax following report format stated on study guide
- Stage and commit all changes using command *commit -a -m "commit message"*
- Push local commits to remote origin still remaining it laboration_1.
- Merge laboration_1 with master branch by using command *git checkout master*,
then command *git merge laboration_1.
- Synchronize master with remote origin so that it's ip to date.
## Discussion  
The purpose of this lab was satisfied. I learned how use git from command line to
create and work with branches, stage and  commits changes, push to remote 
and merge branches. I also learned basic syntax 
in python as well as the concept of variables, expressions and conditions 
which I used to write my firs Python program.
My main difficulty was that kept getting the following error message 
when setting an upstream for my new branch from the command line.
>$ git push –-set-upstream origin laboration_1
fatal: '–-set-upstream' does not appear to be a git repository
fatal: Could not read from remote repository.
Please make sure you have the correct access rights
and the repository exists.

But it worked fine when I push through the iDE. 