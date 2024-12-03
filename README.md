link
https://di.univ-blida.dz/jspui/bitstream/123456789/3400/1/Taguelmint%20Ikram%28D%C3%A9veloppement%20d%27une%20application....pdf
#exemple de fichiers log de securité a analyste cybersecurité python -- Recherche Google

Projet de fin e forùation Initiation en programation - Principalement en python.

Introuction

L'idée part du fait de vouloir faire de l'analuse de données de grandes volumes de données quui sont en faite les big-data.
l'apprentissange de python m'as pousser à vouloir l'apploquer dans un domaine d'applications que je connect en peu l'administration des reseaux et des systemes
en pousssant bcp plus sur la gestion des fichiers logs d'evenements. qui sont de plusisieurs sortes :
-Les scanners de ports de comunication des ordinateurs, serveurs ou tout autres ressources dans le reseau ainsi que tout retour d'un evenement dans un fichier de reportage.
Apres le but est d'analyse cette information pour plusieurs raisons l'audit, scanne la vulnerabilité de la securité, analyse du protocole, detecter les intrusion, la securité web, reseau sans fil, anayse des données machines

mon choix c'est portés sur l'analyse des fichiers de connexion web, qui sont retourner dans des fichiers logs de connexion ou chaque ligne comprend une information d'une conexion.
le but de ce projet est de pourvoir detecter une connexion vumnerable dans chanque connexion et de pourvoir isoler les connxion vulnables dans un fichier de csv qui permettrant de les analyser ainsi que de du prouracentatage de vulnerabilité du lkog sure une certain periode et à  un instant donné de l'analyse. 

Du memoire utilisé "Mémoire de fin d’étude pour l’obtention du diplôme de Master 2 en Informatique Option : Sécurité des systèmes d’information" pour avoir une meilleire comprehension rapidement et passe au codage, il ressort qu'une predilection est aussi possible avec la creation d'une connaissance de precions avec plusieurs fichiers et de pouvoir bloquer les connexions à risquer. une autre applicabilité.

Du code.

Nous avons utilisé des fichiers logs trouver dans un repositioire du memoire qui a ete notre reference de comprehion de l'approche. ces logs sont collectés au fur et à memusre de l'usage de l'ordinateur, du serveurs, du telephone,etc  en fait de tout activite d'un machine automaique -- par des collecteurs. on se retrouve avec trois type de fichiers à savoir structures, non-sutructures et semi structures qui dependent de chaque evenement et de l'application qui fait la collecte des logs. pour mon cas je suis limite a trois type de logs de connexion internet. les "WSC" Work Space Environment, "NCA" common log files , "IIS" Internet Security System.

Apres leur indentification via une fonction "detect_log_format", nous les extraions avec une fonction "extract_type de format", dans un processus "process_logs". A partir de la luiste contenue dans ces listes de données, nous l'analysions pour detecter ceux qui à risque donc vulnerable par de critere isolé dans les logs, ligne par ligne connexion par connexion de la   nous les en registrons dans un fichier CSV qui est plus structuré et plus lisible avec des possibilité d'y effectuer d'autres analyses plus poussé. De la nous generaons le pourcentage de vulnerabilité que nous affichons sur graphe et nous enregistrons le tout dans un rapport pour une analyse plus pousser.

Conclusion 

Sur une tres courte periode de formation et sur plusieurs champs d'applicabilité, nous avons compris que le python avec ces differentes bibiotheques dont nous avons utilisé pres une dizaine, nous aider a generer des scripts et de progrmmane qui permettent d'analyse un grand volume de donner à la fois pour degager une comportement regulier et l'analyse suivant des indicateurs claires à la fois pour l'audit , la surveillance et aussi la predilection. il est important de savoir que pourla suite d'autres outils existent ppour poursuiivre ceux taches. Et nous ne sommes limiter que sur un seul secteur d'applicabilité de ces analyses qui sont aussi utilisé dans bcp de d'autres grands donnés comme le markenting de vente en ligne avec certaines methode permettant de savoir ce que celui qui a achete un article pourrait aussi voiloir. avec la thechinique du plus proche voisin. 

Avoir une image de la vulnerabilité d'un systeme sur une periode à un instant donné pour l'analyse et en tirer ses conculusions.


