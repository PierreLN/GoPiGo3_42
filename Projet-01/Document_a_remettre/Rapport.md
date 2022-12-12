# Rapport sur le projet #1 du cours C64

## Membres de l'équipe
+ Nicolas Charbonneau
+ Pierre Long Nguyen

## À propos de la librairie FiniteStateMachine

### Pourcentage estimé de la proximité entre la réalisation et la conception donnée : **95%**

### Éléments réalisés autrement :
+ Aucune modification particulière a été effectuée lors de la conception et la programmation de la librarie du projet. Le 5% de réalisation différent est pour les erreurs de conception possibles mais le projet a été concu pour respecter le UML. 
    
## Description de l'infrastructure
+ Classe représentant le robot :

    - Validation de l'intégrité du robot : 
        - Instantiation du robot :
        lorsqu'on crée une instance de Robot, dans la fonction __init__, on retrouve un try except qui vérifie que la librarie easygopigo3 soit importée avec succès. On instancie ensuite un objet de la classe easygopigo3.EasyGoPiGo3. Si une exception est lancée, l'instantiation du robot est un échec.
        - Intégrité du robot : 
        Dans le même try except, une fois le robot instancié, on instancie la télécommande et on vérifie que cette-dernière n'est pas None. Dans le projet, on utilise seulement la télécommande comme signal et capteur externe à GoPiGo3. Il n'y a donc pas de vérifications supplémentaires à effectuer.

    - Gestion de la télécommande :
        - Nous avons créé une condition et une transition propres à la télécommande. Dans cette condition, on possède une instance remote_control qui est utilisée dans le _compare pour évaluer si la touche pressée est celle recherchée. Nous avons gérer le cas où cliquer sur OK à partir d'une tâche et qui nous fait sortir de l'application complètement sans appuyer à nouveau. 

    - Gestion de la couleur pour les yeux : 
        - On instancie la couleur des yeux à bleu dans le __init__. Par la suite, nous avons créé deux méthodes de mutation pour aller modifier la couleur de chaque oeil. Ces méthodes prennent en paramètre un tuple (R,B,G) d'entiers non signés de 8 bits.

+ Structure générale du logiciel :
    - Infrastructure générale : 
        - Les 3 niveaux et la partie applicative du projet sont regroupés par cellules dans le fichier ipynb. Dans la partie applicative, on retrouve:
            - LedBlinkers, EyeBlinkers qui sont des SideBlinker
            - ManualControlStateMachine, C64Projet1, LedBlinkers et EyeBlinkers qui sont des FiniteStateMachine
            - ManualControlState(RobotState) contient un ManualControlStateMachine. Il s'agit d'un état de C64Projet possédant des sous-états pour accomplir la tâche du contrôle manuel.
            - Dans C64Projet1, on a redéfinie la fonction track pour que les blinkers puissent eux-aussi exécuter leur fonction track. 

    - Capacité modulaire d'insertion d'une nouvelle tâche :
        - Nous n'avons pas réfléchi à cet aspect. Nous créons le layout de C64Projet1 dans le __init__ et c'est à cet endroit que les états sont générés. On aurait pu passer un layout un paramètre afin qu'il soit possible de construire de nouvelles tâches et les ajouter de l'extérieur mais puisque nous avions seulement une tâche à réaliser nous avons préféré faire ainsi.