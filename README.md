 FastAPI + Docker Todo Backend (JWT Auth Edition)

A high-performance RESTful API backend built with **FastAPI**. This project features a robust **OAuth2 + JWT** authentication system and is fully **Dockerized** to ensure seamless deployment across different environments (Windows/Linux/macOS).


Key Features

 High Performance: Powered by FastAPI, offering near-Go/NodeJS speeds and auto-generated interactive OpenAPI (Swagger) documentation.
 Industrial-Grade Security: 
 Bcrypt Password Hashing: Automatically adds a unique “Salt” to passwords to prevent Rainbow Table and Brute Force attacks.
 Stateless JWT Auth: Implements OAuth2 Password Flow with JSON Web Tokens for secure, scalable session management.
 Containerization: Includes a production-ready Dockerfile to eliminate the "it works on my machine" problem.
 Database Persistence: Uses SQLAlchemy ORM to communicate with MySQL, supporting automatic schema generation and data persistence.



My Tech Stack

  Language: Python 3.9+
  Framework: FastAPI
  Web Server: Uvicorn
  Database: MySQL 8.0 (SQLAlchemy ORM)
  Security: Passlib (Bcrypt), Python-jose (JWT)
  Infrastructure: Docker


Quick Start Guide

1. Clone the Repository
```bash
git clone [https://github.com/illytr22/fastapi-docker-todo.git](https://github.com/illytr22/fastapi-docker-todo.git)
cd fastapi-docker-todo
