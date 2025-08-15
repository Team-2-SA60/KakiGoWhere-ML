
## Production Server

KakiGoWhere is deployed on Digital Ocean, and will be kept running until 31st August 2025.

You can access our deployed Web Application [here](http://206.189.43.202/admin/login)

## 🛠️ Getting started using 🐳 Docker

Pre-requisite:
- Follow steps on [KakiGoWhere-Backend](https://github.com/Team-2-SA60/KakiGoWhere-Backend)

---

1. Open terminal / command prompt and change directory to KakiGoWhere

    ```
    cd KakiGoWhere
    ```

2. Clone repository

    ```
    git clone https://github.com/Team-2-SA60/KakiGoWhere-ML.git
    ```

3. Change directory to KakiGoWhere-ML

    ```
    cd KakiGoWhere-ML
    ```

4. Build and run Flask-ML using Docker Compose

    ```
    docker compose -f ./docker/docker-compose.dev.yml up -d --build
    ```

    > This process can take very long (15 mins - 30 mins depending on CPU performance and RAM) due to downloading of pre-trained models and CPU-intensive tasks

5. Go back to [KakiGoWhere-Backend](https://github.com/Team-2-SA60/KakiGoWhere-Backend) and continue steps

6. When all containers are running: 
- Access web application @ http://localhost/admin/login
- Mobile app (android) @ https://github.com/Team-2-SA60/KakiGoWhere-Android