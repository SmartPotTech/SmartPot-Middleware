## **1. Construcción de la Imagen Docker**

### 1 **Construcción de la Imagen Docker**

1. **Abre una terminal** y navega hasta la raíz de tu proyecto, donde se encuentra el archivo `Dockerfile`.
   
2. Ejecuta el siguiente comando para construir la imagen Docker:

   ```bash
   docker build -t sebastian190030/middleware-smartpot:latest .
   ```

   **Explicación**:
   - **`docker build`**: Este comando le indica a Docker que construya una imagen basada en las instrucciones del archivo `Dockerfile`.
   - **`-t middleware-smartpot:latest`**: Le asigna el nombre `middleware-smartpot` y la etiqueta `latest` a la imagen Docker. El nombre de la imagen puede ser cualquier nombre que desees, pero es recomendable utilizar un nombre significativo.
   - **`.`**: Este punto (`.`) especifica el directorio actual como contexto de construcción (es decir, el directorio donde se encuentra el `Dockerfile`).

   Este comando construye la imagen Docker según lo especificado en el `Dockerfile`, incluyendo la instalación de dependencias y la configuración de la aplicación.


## **2. Publicación de la Imagen en Docker Hub**

Una vez que la imagen Docker esté lista, el siguiente paso es **subirla a Docker Hub** para poder compartirla y utilizarla en otros entornos.

### 2.1 **Iniciar Sesión en Docker Hub**

Para subir la imagen a **Docker Hub**, primero debes iniciar sesión en tu cuenta desde la terminal. Ejecuta el siguiente comando:

```bash
docker login
```

**Explicación**:
- **`docker login`**: Este comando solicita tu **nombre de usuario** y **contraseña** de Docker Hub. Si aún no tienes una cuenta, puedes crear una en [Docker Hub](https://hub.docker.com/).

Una vez que inicies sesión correctamente, Docker te permitirá subir imágenes a tu cuenta de Docker Hub.

### 2.2 **Subir la Imagen a Docker Hub**

Finalmente, para subir la imagen a Docker Hub, ejecuta el siguiente comando:

```bash
docker push sebastian190030/middleware-smartpot:latest
```

**Explicación**:
- **`docker push`**: Este comando sube la imagen etiquetada al repositorio correspondiente en Docker Hub.

El proceso de subida puede tomar un tiempo, dependiendo del tamaño de la imagen y la velocidad de tu conexión a Internet. Una vez que termine, la imagen estará disponible en Docker Hub.
