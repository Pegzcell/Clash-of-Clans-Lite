# COC Lite

>Run game.py to start playing

### Aim
Destroy all the buildings using the player with the help of 3 army troops. You will be asked to choose between __King__ and __Archer Queen__ as your main player at the beginning.

### Gameplay
- Buildings are magenta structures.
- You control the player's motion and attacks
- 3 spawning spots inside wall enclosures are available
- each spot can spawn any troop
- cannon buildings fire at the player and your armies except balloons
- wizard towers fire at the player and your armies
- use spells to empower your troops

>__King__: Uses Leviathan attack to cause a circular AOE around itself

>__Queen__: Uses Archery to cause a sqaure AOE at a fixed range. Eagle attack has more range and AOE but affects target after 1 second of being shot.

>__Barbarians__: The infantry

>__Archers__: They stop to attack at a fixed distance to break walls/buildings

>__Balloons__: They can fly over walls/buildings to target defensive buildings. They are safe from cannons

### Levels
The number of cannons and wizard towers progressively increases with the levels. all your team is renewed at the start of each level. The spells' effect is not undone.

### Game-endings
>__Victory__: you win if you destroy all enemy buildings with some member of your army surviving(i.e., player or troop member) in the third level

>__Defeat__: you lose if the enemy defensive buildings manage to destroy all of your army and you have no troops left to spawn on any level

### Controls
- WASD - Player movement
- space - Player attack
- E - Archer Queen's Eagle Attack
- 1,2,3 - Spawn Barbarians
- 4,5,6 - Spawn Archers
- 7,8,9 - Spawn Balloons
- H - heal spell: 1.5 x health of all active army members
- R - rage spell: 2 x speed and attack of all active army members
- Q - quit game

### Replays
Replays of previous plays are saved in the 'replays' folder. Just run replay.py and enter the name of the file to replay the saved game


## About the implementation:

The game code is modular and extensively uses the concepts of Object Oriented Programming.
* __Inheritance:__ You could have one building class and have the different kinds of building inherit
from the building class.
* __Polymorphism:__ You could have one spell class and override various characteristics to exhibit
different properties.
* __Encapsulation:__ The fact that you’re using classes and objects should suffice for this! Use a class
and object based approach for all the functionality that you implement.
* __Abstraction:__ Intuitive functionality like move(), attack() etc should be methods within the class. So
for instance (no pun intended), if you declare an object ’player’ of the person class, you can call
the methods player.move() and player.attack(), stowing away inner details from the end user.