README.txt

Ce dépôt contient l'ensemble des fichiers de notre projet intégrateur,
réalisé en 5e année SDBD à l'INSA Toulouse.

---------------------------------------------------------------------------------------------------

I) CONTENU

- Un fichier .gitignore
- Un script bash docker-clear.sh servant à faire un nettoyage complet de Docker sur l'hôte
- Un docker-compose.yml permettant de mettre en place toute l'architecture Docker du projet
- Un script python learning.py pour l'apprentissage & envoi de nouvelles données
- Un dossier data contenant le nécessaire pour build le container Spark Master
- Un dossier spark contenant le nécessaire pour build les containers Spark Workers
- Un dossier docs contenant la documentation du projet, notamment le sujet, la présentation et le rapport

---------------------------------------------------------------------------------------------------

II) PROCEDURE D'INSTALLATION

- Se placer dans le répertoire principal et lancer : docker-compose up -d

---------------------------------------------------------------------------------------------------

III) REFERENCES

L'installation de Docker et Docker Compose peut se faire via les liens suivants :

- https://docs.docker.com/install/linux/docker-ce/ubuntu/
- https://docs.docker.com/compose/install/

Nous nous sommes référés à ces documentations pour l'installation de containers Minio via Docker Compose :

- https://github.com/minio/minio
- https://docs.minio.io/docs/deploy-minio-on-docker-compose

Nous nous sommes basés sur ces documentations pour installer Elastic Search et Kibana via Docker Compose :

- https://github.com/maxyermayank/docker-compose-elasticsearch-kibana
- https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html

Les données utilisées pour les tests sont disponibles ici :

- https://filez.insa-toulouse.fr/ewa9170p

---------------------------------------------------------------------------------------------------
