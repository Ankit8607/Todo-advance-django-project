
## Tech Stack
- Language: Python
- Framework: Django
- Database: SQLite
- ORM: Django ORM

   
## Database Design : 
<img width="1339" alt="Screenshot 2024-07-15 at 1 01 47 PM" src="https://github.com/user-attachments/assets/29f9c90e-4738-4d2f-bbb4-6fcc959b9404">




## Running the System

1. Activate the env ```source venv/bin/activate```  (for windows : ```venv\Scripts\activate```)
2. Install the requirements ```pip install -r requirements.txt```

3. Run the Command ``` python manage.py runserver ```
4. Open Postman and test the endpoints
5. if first step fails run this command ```python3 -m venv venv ```
6. then try step 1


## Create Users

- Endpoint: `localhost:8000/api/users/`
- Create user and generate its access token for log into the system
- <img width="1071" alt="Screenshot 2024-07-13 at 10 19 22 PM" src="https://github.com/user-attachments/assets/ad8912bb-37a4-46aa-8709-fe918d006948">


## Login ( Token Generation )

- Endpoint: `localhost:8000/api/token/`
- <img width="1110" alt="Screenshot 2024-07-13 at 10 19 29 PM" src="https://github.com/user-attachments/assets/520847d3-26e8-49bc-9154-340963e79c20">

## Create tags
- Endpoint: `localhost:8000/api/tags/`
- <img width="1080" alt="Screenshot 2024-07-13 at 10 21 24 PM" src="https://github.com/user-attachments/assets/36e6e008-4786-40cf-a720-58a83d8ff931">

## Create and list Projects

- You need to add header "Authorization" = Bearer <Access token> 
- Endpoint: `localhost:8000/api/projects/`
- <img width="1098" alt="Screenshot 2024-07-15 at 12 08 12 PM" src="https://github.com/user-attachments/assets/9df65f60-1cef-4802-980c-5e7889327eaf"> 
- <img width="1123" alt="Screenshot 2024-07-15 at 12 08 50 PM" src="https://github.com/user-attachments/assets/503dc89c-657b-4056-a48a-cc75a4742ab2">


## Update, Retreive and Partial Update Project

- Endpoint: `localhost:8000/api/projects/<uuid of project>/`
- You need to add header "Authorization" = Bearer <Access token> 
- <img width="1104" alt="Screenshot 2024-07-13 at 10 19 59 PM" src="https://github.com/user-attachments/assets/94206d44-724b-45bf-a214-03e9e84e83fb"> 
- <img width="1091" alt="Screenshot 2024-07-15 at 12 30 41 PM" src="https://github.com/user-attachments/assets/82748daa-fb1c-41b2-b563-c2de059a20a5">



## Create and list Tasks

- Endpoint: `localhost:8000/api/projects/<uuid of project>/tasks/`
- You need to add header "Authorization" = Bearer <Access token> 
- <img width="1090" alt="Screenshot 2024-07-15 at 12 33 57 PM" src="https://github.com/user-attachments/assets/2471a585-75bd-44da-8fd4-fb5968a7c0a6"> 
- <img width="1079" alt="Screenshot 2024-07-13 at 10 15 02 PM" src="https://github.com/user-attachments/assets/5184c719-a5be-4a3e-a5f5-2c8959a0a221">




## Update, Retreive and Partial Update Task

- Endpoint: `localhost:8000/api/projects/<uuid of project>/tasks/<uuid of task>/`
- You need to add header "Authorization" = Bearer <Access token> 
- <img width="1124" alt="Screenshot 2024-07-13 at 10 20 49 PM" src="https://github.com/user-attachments/assets/bc67b085-142b-4fd0-8d87-5add33078dc7"> 
- <img width="1123" alt="Screenshot 2024-07-13 at 10 20 59 PM" src="https://github.com/user-attachments/assets/7cbf051e-71ec-4a0c-a5d4-634d1364dcfc"> 
  


## Create and list Subtasks

- Endpoint: `localhost:8000/api/tasks/<uuid of task>/subtasks/`
- You need to add header "Authorization" = Bearer <Access token> 
- <img width="1127" alt="Screenshot 2024-07-13 at 10 21 08 PM" src="https://github.com/user-attachments/assets/66436c06-2fb9-4da3-8f20-5af44a8eae2e"> ok




## Update, Retreive and Partial Update Subtask

- Endpoint: `localhost:8000/api/tasks/<uuid of task>/subtasks/<uuid of subtask>/`
- You need to add header "Authorization" = Bearer <Access token> 
- <img width="1108" alt="Screenshot 2024-07-13 at 10 21 16 PM" src="https://github.com/user-attachments/assets/de4d4c03-7b93-42f2-8a0d-36c32fbde003">
- after making this is_completed true, main task will be completed too becoz it has only 1 subtask
- <img width="1123" alt="Screenshot 2024-07-15 at 12 44 04 PM" src="https://github.com/user-attachments/assets/28cdd58e-03df-4c95-9b17-721a6d6bb0bb">


## Public Projects

- Endpoint: `localhost:8000/api/public-projects/<uuid of project>/`
- <img width="1109" alt="Screenshot 2024-07-15 at 12 47 23 PM" src="https://github.com/user-attachments/assets/60b54afe-296a-472e-a5a8-ac9114d820f6">

## Searching 

- <img width="1083" alt="Screenshot 2024-07-13 at 11 00 30 PM" src="https://github.com/user-attachments/assets/a5c5e433-770c-4141-afe0-bb7a29b7ba0d">
- <img width="1096" alt="Screenshot 2024-07-13 at 11 01 00 PM" src="https://github.com/user-attachments/assets/e81b0f01-dad6-4c65-9a4c-922d1a1f754f">

## Permission checks and token expiration

- Project Permissions: Only the project creator has the authority to update the project. Additionally, only the project creator can view a list of their projects.
- Task Permissions: Tasks can only be created by the person who created the project. To update or list tasks, you must be the project creator.
- Subtask Permissions: To update or list subtasks, you must either be the task owner or the task assignee.
- <img width="1101" alt="Screenshot 2024-07-14 at 12 28 13 AM" src="https://github.com/user-attachments/assets/e9c6b9b4-0809-4b55-b598-bff1bda5ab6b"> 
- <img width="1122" alt="Screenshot 2024-07-15 at 12 52 15 PM" src="https://github.com/user-attachments/assets/a50d2817-6f41-4630-8da1-a1e7a4ada8e9">








