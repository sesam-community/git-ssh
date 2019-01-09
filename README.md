# Access remote Git repos

## How to configure

```json
{
  "_id": "my-git",
  "type": "system:microservice",
  "docker": {
    "image": "[..]",
    "port": 5000,
    "environment": {
      "GIT_REPO": "git@github.com:sesam-community/git-ssh.git",
      "SSH_PRIVATE_KEY": "-----BEGIN RSA PRIVATE [..]"  
    }
  }
}
```

## How to use

Pull down a list of files if you point to '/<directory>', and pull down the file content with '/<file-path>'.
