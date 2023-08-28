# 
# FROM python:3.9 as requirements-stage

# # 
# WORKDIR /tmp

# # 
# RUN pip install poetry

# # 
# COPY ./pyproject.toml ./poetry.lock* /tmp/

# # 
# RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# # 
FROM python:3.9-slim-buster

# 
WORKDIR /code

# 
# COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt
COPY requirements.txt /code/requirements.txt

# 
RUN pip install --upgrade pip
RUN pip install -r /code/requirements.txt
# 
COPY ./iam /code/iam

# 
CMD ["uvicorn", "iam.app:get_application", "--host", "0.0.0.0", "--port", "80"]