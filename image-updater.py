import yaml
import subprocess
import requests

def get_latest_image(image_name):
  repo_tag_url = "https://hub.docker.com/v2/repositories/%s/tags" % image_name
  results = requests.get(repo_tag_url).json()['results']
  for tag in results:
    if tag['name'] == 'latest':
      continue
    latest_tag = tag['name']
    print("Latest image tag:", latest_tag)
    break
  return latest_tag

def update_docker_compose(image_name):
  # load docker-compose.yaml
  with open("docker-compose.yaml", 'r') as yaml_file:
    data = yaml.load(yaml_file, Loader = yaml.FullLoader)

  # update image
  data['services']['whoami']['image'] = image_name
  print("Service image updated to:", image_name)

  # save docker-compose.yaml
  with open("docker-compose.yaml", 'w') as yaml_file:
    yaml_file.write(yaml.dump(data, default_flow_style=False))

def main():
  image_name = "containous/whoami"

  new_image = "%s:%s" % (image_name, get_latest_image(image_name))
  update_docker_compose(new_image)

  # add docker-compose.yaml to stage
  subprocess.run(
    "git add docker-compose.yaml", shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

  # commit staged
  git_commit_command = "git commit -m 'Update service image to %s'" % new_image
  try:
    git_commit_out = subprocess.run(git_commit_command, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
  except:
    print("Nothing to commit")
    exit()

  # push updated docker-compose.yaml
  subprocess.run("git push origin main", shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
  print("Git repository updated")

main()
