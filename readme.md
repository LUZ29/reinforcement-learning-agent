# Project3
This project is about building a reinforcement learning agent. In particular, you will have to build a Frogger agent, who must navigate its way home.
## Environment
* Python 2.7.15
* Follow the README within the frogger_game_env tar to install the other necessary modules. 
>1. If you use pip, make sure you are downloading and installing the 2.7 version of the modules
>2. Make sure your python compiler knows where to look for the modules (set up an environment variable called PYTHONPATH if needed).

## How to run
Please put Qagent.py, QTABLE.txt and NTABLE.txt in the frogger folder. Then, run Qagent.py directly.

## How to learn
If you want to train this frog more, just uncomment line 99 (remove the "#" before "self.save_table()"). Then run Qagent.py. And if you want the frog to leatn from scratch, you can run it after removing QTABLE.txt and NTABLE.txt.

## About the data files
### Table
Q and N are saved in dictionary as values, and every "(state,action)" is saved as keys.
### State representation
I use AgentState class to deal with the GameState, and then get those properties as state: 1.water, 2.left, 3.right, 4.front, 5.back, 6.home_entry
1. whether the frog is going to cross river or not: True/False
2. how many steps the frog can move to left: 1/2/3/4/5
3. how many steps the frog can move to right: 1/2/3/4/5
4. can the frog go forward: True/False
5. can the frog go backward: True/False
6. what is in the closest home: 0,0.33,0.66 etc./None(when home is far or 2 home have the same |home_x-x_frog|)

## Result
The output shows the game.score when frog died or win this game (all five frogs go home). The transcript shows the result I got after running the pretrained model for 10 minutes.
1. score>10 means all frogs go home；
2. score>3 means 4 forgs go home；
3. score>2 means 3 frogs go home；
4. score>1 meams 2 frogs go home；
5. score>0 means 1 frog go home；
6. score<0 means the frog did't go home.

## Performance
* In test, on average 2.42 frogs make it home safely per game.
* 2.37 is the average score per game.
### What might be improved
* After observing how the frog die in games, I notice that the frog often float away and die for out of border when the frog arrives the wood on the top and homes in front of it is occupied. The same "out of border" situation also happended many times when the frog is standing on other river objects.
* Therefore I think it's a good idea to add a property to tell the frog whether he is close to border.
> I also wrote this in code, but didn't finish to train it. The training time is longer than the original one because the states are much more than original one. I also submit this version of code which contains the border property, in the floder "extra version".

* Besides, I only used approximate value to evaluate the distance of car/river objects and homes (something like 130.0, 260.0, 40.0 etc.). I think the performance would be better if I use more specific value to meature the distance between the frog and each object and each home.

## Transcript
    D:\installsws\Anaconda3\envs\pycharm\python.exe D:/workspace/2710/frogger/Qagent.py
    pygame 1.9.4
    Hello from the pygame community. https://www.pygame.org/contribute.html
    couldn't import doomish
    Couldn't import doom
    1.3
    0.2
    0.2
    fly bonus!
    3.4
    1.2
    fly bonus!
    fly bonus!
    3.5
    fly bonus!
    2.4
    -0.9
    0.2
    -0.9
    fly bonus!
    0.2
    3.5
    0.2
    fly bonus!
    3.4
    -0.9
    fly bonus!
    10.5
    3.5
    10.5
    fly bonus!
    fly bonus!
    3.5
    Process finished with exit code -1

## Details
I use class AgentState to get the state representation.
1.water, 2.left, 3.right, 4.front, 5.back, 6.home_entry
1. whether the frog is going to cross river or not: True/False
> I use the 'frog_y' to judge this boolean value, if 
2. how many steps the frog can move to left: 1/2/3/4/5
3. how many steps the frog can move to right: 1/2/3/4/5
4. can the frog go forward: True/False
5. can the frog go backward: True/False
6. what is in the closest home: 0,0.33,0.66 etc./None(when home is far or 2 home have the same |home_x-x_frog|)