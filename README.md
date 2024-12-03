link
https://di.univ-blida.dz/jspui/bitstream/123456789/3400/1/Taguelmint%20Ikram%28D%C3%A9veloppement%20d%27une%20application....pdf
#exemple de fichiers log de securité a analyste cybersecurité python -- Recherche Google


Projet de Fin de Formation : Initiation à la Programmation - Principalement en Python
Introduction
L’idée de ce projet s’inscrit dans le cadre de l’analyse de grandes quantités de données, communément appelées Big Data. Mon apprentissage de Python m’a incité à appliquer mes compétences dans un domaine connexe à l’administration des réseaux et des systèmes, en mettant l’accent sur la gestion et l’analyse des fichiers logs d’événements. Ces logs incluent :

Les scanners de ports de communication des ordinateurs, serveurs ou autres ressources réseau.
Les rapports d’événements générés par différentes applications ou systèmes.
Le but ultime est d’analyser ces informations pour répondre à divers besoins tels que :

L’audit de sécurité.
La détection de vulnérabilités réseau.
L’analyse des protocoles de communication.
La détection d’intrusions.
La sécurité des applications web et des réseaux sans fil.
L’analyse des données machines.
Mon projet se concentre sur l’analyse des fichiers logs de connexions web, lesquels contiennent des enregistrements détaillés de chaque connexion. L’objectif principal est de détecter les connexions vulnérables, de les isoler dans un fichier CSV, et de fournir des statistiques sur les vulnérabilités observées (notamment en termes de pourcentage) pour une période donnée ou un instant précis.

Sources et Méthodologie
Inspiré par le mémoire intitulé "Mémoire de fin d’étude pour l’obtention du diplôme de Master 2 en Informatique, Option : Sécurité des systèmes d’information", j’ai adapté une approche qui combine compréhension théorique et application pratique via Python. Ce travail ouvre également la voie à une potentielle extension consistant à prédire les connexions à risque, en se basant sur des données historiques.

Approche technique
Les fichiers logs utilisés dans ce projet proviennent d’un référentiel du mémoire de référence. Ces logs, collectés par des outils automatiques, reflètent l’activité des ordinateurs, serveurs, téléphones et autres machines. Ils se divisent en trois catégories principales :

Structurés.
Non structurés.
Semi-structurés.
Mon projet se concentre spécifiquement sur trois types de fichiers logs :

WSC (Work Space Environment).
NCA (Common Log Files).
IIS (Internet Security System).
Les étapes clés de l’analyse sont les suivantes :

Identification du format des logs
Une fonction nommée detect_log_format est utilisée pour déterminer le type de fichier log analysé.

Extraction des données pertinentes
Une fonction extract_type_de_format traite chaque type de log pour en extraire les informations utiles, dans un processus global appelé process_logs.

Analyse des connexions à risque

Chaque ligne des logs est analysée pour identifier les connexions vulnérables selon des critères définis.
Les connexions jugées vulnérables sont enregistrées dans un fichier CSV structuré, facilitant ainsi une analyse approfondie.
Visualisation des résultats

Le pourcentage de vulnérabilités détectées est représenté graphiquement.
Un rapport synthétique est généré pour documenter les conclusions de l’analyse.
Conclusion
Au cours de cette courte période de formation, Python et ses nombreuses bibliothèques (environ une dizaine utilisées) se sont révélés être des outils puissants pour développer des scripts et des programmes permettant d’analyser efficacement de grands volumes de données. Ces analyses nous aident à identifier des comportements récurrents ou à détecter des anomalies à des fins d’audit, de surveillance, et même de prédiction.

Bien que ce projet se limite à l’analyse des fichiers logs de connexions web, il est important de noter que de nombreux outils et techniques complémentaires existent pour poursuivre et approfondir ce type de tâche. De plus, l’analyse de données a des applications bien au-delà de la cybersécurité, comme dans le marketing, où elle est utilisée pour prédire les comportements d’achat grâce à des méthodes comme celle des "k-plus proches voisins".

En conclusion, disposer d’une vue claire de la vulnérabilité d’un système à un moment donné ou sur une période donnée est crucial pour une analyse approfondie et une prise de décision éclairée

