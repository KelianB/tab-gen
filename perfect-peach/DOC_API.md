# Description de l'API entre le back et le front

### Fonctionnalités nécessaires

- Le front doit pouvoir envoyer un fichier audio vers le back pour qu'il soit traité dans une version donnée du modèle
- Le front doit pouvoir connaître l'état du traitement (EN COURS OU FINI)
- Le front doit pouvoir récupérer la tablature sous une forme utilisable par le front (AlphaTex, GP, Midi, MusicXML)
- Systeme de version
- Éviter le traitement multiple du même fichier

### Fonctionnalités bonus

- Le front doit pouvoir connaître la progression du traitement (temps restant ou pourcentage de traitement)

# Proposition API

## **GET** /api/versions

---

Envoie les versions du modèle disponibles pour traitement

### **Example de réponse**

```json
[
  {
    "name": "Version10",
    "description": "Fonctionne bien pour les solos de guitare électriques",
    "id": 3
  },

  {
    "name": "Version11",
    "description": "Fonctionne bien pour les guitares classiques",
    "id": 7
  },

  ...


]
```

## **POST** /api/version/**:version_id**/

---

Envoie d'un fichier audio pour traitement dans la version **:version_id** du modèle

Réponse possible: un id correspond au traitement ("job_id")

### **Headers**

| Key          | Value      |
| ------------ | ---------- |
| Content-Type | audio/mpeg |

### **Parameters**

| Name     | Type   | Description                    |
| -------- | ------ | ------------------------------ |
| env-name | String | Name of the target environment |

### **Request Body**

| Name   | Type         | Description |
| ------ | ------------ | ----------- |
| **\_** | binary/audio | Audio file  |

### **Example de reponse**

```json
{
  "job_id": 5
}
```

## **GET** /api/version/**:version_id**/**:job_id**/state

---

Recupère l'état du traitement ayant l'id **:job_id** par le modèle de version **:version_id**

Reponse possible: Booléen False si le job est en cours, true s'il est fini
Code 404 (ou adapté) si le traitement n'existe pas

### **Example de reponse**

```json
{
  "etat": false
}
```

## **GET** /api/version/**:version_id**/**:job_id**/(result)

---

Renvoie la tablature dans le bon format

### **Exemple de reponse**

#### Fichier alphatex

```tex
\title "Canon Rock"
\subtitle "JerryC"
\tempo 90
.
:2 19.2{v f} 17.2{v f} |
15.2{v f} 14.2{v f}|
12.2{v f} 10.2{v f}|
12.2{v f} 14.2{v f}.4 :8 15.2 17.2 |
14.1.2 :8 17.2 15.1 14.1{h} 17.2 |
15.2{v d}.4 :16 17.2{h} 15.2 :8 14.2 14.1 17.1{b(0 4 4 0)}.4 |
15.1.8 :16 14.1{tu 3} 15.1{tu 3} 14.1{tu 3} :8 17.2 15.1 14.1 :16 12.1{tu 3} 14.1{tu 3} 12.1{tu 3} :8 15.2 14.2 |
12.2 14.3 12.3 15.2 :32 14.2{h} 15.2{h} 14.2{h} 15.2{h}14.2{h} 15.2{h}14.2{h} 15.2{h}14.2{h} 15.2{h}14.2{h} 15.2{h}14.2{h} 15.2{h}14.2{h} 15.2{h}
```
