# dit-contact-forms
DIT Contact Forms

## Creating Docker container for CircleCI

```bash
export VERSION=1.0.0 # Increment this version each time when you edit Dockerfile.

docker login # Ask webops for Docker Hub access to the ukti group.
docker build -f Dockerfile -t dit-contact-forms .

docker tag dit-contact-forms:latest ukti/dit-contact-forms:${VERSION}
docker tag dit-contact-forms:latest ukti/dit-contact-forms:latest

docker push ukti/dit-contact-forms:${VERSION}
docker push ukti/dit-contact-forms:latest
```