### Endpoints requis

* [x]   [User creation](#user-creation)
* [x]   [Authentication](#authentication)
* [x]   [User deletion](#user-deletion)
* [x]   [User update](#user-update)
* [x]   [User list](#user-list)
* [x]   [Users by ID](#users-by-id)
* [x]   [Video creation](#video-creation)
* [x]   [Video list](#video-list)
* [x]   [Video list by user](#video-list-by-user)
* [ ]   [Encoding video by id](#encoding-video-by-id)
* [x]   [Video update](#video-update)
* [x]   [Video deletion](#video-deletion)
* [x]   [Comment creation](#comment-creation)
* [x]   [Comment list](#comment-list)








### User creation
[Subject Step 1](https://rendu-git.etna-alternance.net/module-6737/activity-37907/group-779717/blob/master/annexes/sujet/sujet_phase1.html)

**Definition**

- `Méthode: POST /user`

- `Authentification: False`

**Paramètres**
```json
{
	"username*": string([a-zA-Z0-9_-]),
	"pseudo": string,
	"email*": string(email),
	"password*": string // algorithme de hachage obligatoire
}
```

**Réponse**

- `201 Created` on success

```json
{
	"message": "Ok",
	"data": User
}
```





### Authentication
[Subject Step 2](https://rendu-git.etna-alternance.net/module-6737/activity-37907/group-779717/blob/master/annexes/sujet/sujet_phase2.html)

**Definition**

- `Méthode: POST /auth`

- `Authentification: False`

**Paramètres**
```json
{
	"login*": string,
	"password*": string
}
```

**Réponse**

- `Code retour 201` on success

```json
{
	"message": "OK",
	"data": Token
}
```

### User deletion
[Subject Step 3](https://rendu-git.etna-alternance.net/module-6737/activity-37907/group-779717/blob/master/annexes/sujet/sujet_phase3.html)

**Definition**

- `Méthode: DELETE /user/:id`

- `Authentification: Token`

**Paramètres**
```json
{
	"login*": string,
	"password*": string
}
```

**Réponse**

- `Code retour 201` on success
 


### User update
[Subject Step 4](https://rendu-git.etna-alternance.net/module-6737/activity-37907/group-779717/blob/master/annexes/sujet/sujet_phase4.html)

**Definition**

- `Méthode: PUT /user/:id`

- `Authentification: Token`

**Paramètres**
```json
{
	"username": string([a-zA-Z0-9_-]),
	"pseudo": string,
	"email": string(email),
	"password": string
}
```

**Réponse**

- `Code retour 200` on success

```json
{
	"message": "Ok",
	"data": User,
}
```

### User list
[Subject Step 5](https://rendu-git.etna-alternance.net/module-6737/activity-37907/group-779717/blob/master/annexes/sujet/sujet_phase5.html)

**Definition**

- `Méthode: GET /users`

- `Authentification: False`

**Paramètres**
```json
{
	"pseudo": string,
	"page": int,
	"perPage": int
}
```

**Réponse**

- `Code retour 200` on success

```json
{
	"message": "OK",
	"data": [
		User,
		...
	],
	"pager": {
		"current": int,
		"total": int
	}
}
```

### Users by ID
[Subject Step 6](https://rendu-git.etna-alternance.net/module-6737/activity-37907/group-779717/blob/master/annexes/sujet/sujet_phase6.html)

**Definition**

- `Méthode: GET /user/:id`

- `Authentification: Token`

**Paramètres**

**Réponse**

- `Code retour 200` on success

```json
{
	"message": "OK",
	"data": User
}
```


### Video creation
[Subject Step 7](https://rendu-git.etna-alternance.net/module-6737/activity-37907/group-779717/blob/master/annexes/sujet/sujet_phase7.html)

**Definition**

- `Méthode: POST /user/:id/video`

- `Authentification: Token`

**Paramètres**
```json
{
	"name": string,
	"source": file
}
```

**Réponse**

- `Code retour 201` on success

```json
{
	"message": "OK",
	"data": Video
}
```


### Video list
[Subject Step 8](https://rendu-git.etna-alternance.net/module-6737/activity-37907/group-779717/blob/master/annexes/sujet/sujet_phase8.html)

**Definition**

- `Méthode: GET /videos`

- `Authentification: False`

**Paramètres**
```json
{
	"name": string,
	"user": string|int,
	"duration": int,
	"page": int,
	"perPage": int
}
```

**Réponse**

- `Code retour 200` on success

```json
{
	"message": "OK",
	"data": [
		Video,
		...
	],
	"pager": {
		"current": int,
		"total": int
	}
}
```


### Video list by user
[Subject Step 9](https://rendu-git.etna-alternance.net/module-6737/activity-37907/group-779717/blob/master/annexes/sujet/sujet_phase9.html)

**Definition**

- `Méthode: GET /user/:id/videos`

- `Authentification: False`

**Paramètres**
```json
{
	"page": int,
	"perPage": int
}
```

**Réponse**

- `Code retour 200` on success

```json
{
	"message": "OK",
	"data": [
		Video,
		...
	],
	"pager": {
		"current": int,
		"total": int
	}
}
```

### Encoding video by ID
[Subject Step 10](https://rendu-git.etna-alternance.net/module-6737/activity-37907/group-779717/blob/master/annexes/sujet/sujet_phase10.html)

**Definition**

- `Méthode: PATCH /video/:id`

- `Authentification: False`

**Paramètres**
```json
{
	"format": string,
	"file": string
}
```

**Réponse**

- `Code retour 200` on success

```json
{
	"message": "OK",
	"data": Video
}
```

### Video update
[Subject Step 11](https://rendu-git.etna-alternance.net/module-6737/activity-37907/group-779717/blob/master/annexes/sujet/sujet_phase11.html)

**Definition**

- `Méthode: PUT /video/:id`

- `Authentification: Token`

**Paramètres**
```json
{
	"name": string,
	"user": int
}
```

**Réponse**

- `Code retour 200` on success

```json
{
	"message": "OK",
	"data": Video
}
```

### Video deletion
[Subject Step 12](https://rendu-git.etna-alternance.net/module-6737/activity-37907/group-779717/blob/master/annexes/sujet/sujet_phase12.html)

**Definition**

- `Méthode: DELETE /video/:id`

- `Authentification: Token`

**Paramètres**
```json
{
	"name": string,
	"user": int
}
```

**Réponse**

- `Code retour 204` on success

### Comment creation
[Subject Step 13](https://rendu-git.etna-alternance.net/module-6737/activity-37907/group-779717/blob/master/annexes/sujet/sujet_phase13.html)

**Definition**

- `Méthode: POST /video/:id/comment`

- `Authentification: Token`

**Paramètres**
```json
{
	"body": string
}
```

**Réponse**

- `Code retour 201` on success

```json
{
	"message": "OK",
	"data": Commentaire
}
```

### Comment list
[Subject Step 14](https://rendu-git.etna-alternance.net/module-6737/activity-37907/group-779717/blob/master/annexes/sujet/sujet_phase14.html)

**Definition**

- `Méthode: GET /video/:id/comments`

- `Authentification: Token`

**Paramètres**
```json
{
	"page": int,
	"perPage": int
}
```

**Réponse**

- `Code retour 201` on success

```json
{
	"message": "OK",
	"data": [
		Commentaire,
		...
	],
	"pager": {
		"current": int,
		"total": int
	}
}
```