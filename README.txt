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

II) PROCEDURE D'INSTALLATION & UTILISATION

- Se placer dans le répertoire principal et lancer : docker-compose up -d
- L'ensemble des containers peuvent être managés via Portainer (0.0.0.0:9000)

---------------------------------------------------------------------------------------------------

III) REFERENCES

Installation de Docker et Docker Compose :

- https://docs.docker.com/install/linux/docker-ce/ubuntu/
- https://docs.docker.com/compose/install/

Installation de containers Minio via Docker Compose :

- https://github.com/minio/minio
- https://docs.minio.io/docs/deploy-minio-on-docker-compose

Installation de Elasticsearch et Kibana via Docker Compose :

- https://github.com/maxyermayank/docker-compose-elasticsearch-kibana
- https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html

Données utilisées pour les tests :

- https://filez.insa-toulouse.fr/ewa9170p

SSH un container :

- https://linoxide.com/linux-how-to/ssh-docker-container/

---------------------------------------------------------------------------------------------------
