import random

from locust import HttpUser, TaskSet, between, task

movies = ["Inception", "Batman", "Avengers", "Matrix", "Titanic", "Frozen", "Interstellar", "Joker", "Transformers"]

class MovieTestTasks(TaskSet):
  @task
  def fetch_movies(self):
    movie_filter = random.choice(movies)
    self.client.get(f"/api/movies?filter={movie_filter}")

class MovieUser(HttpUser):
  tasks = [MovieTestTasks]
  wait_time = between(1, 5)