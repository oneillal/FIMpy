## Kubernetes

I'm a bit obsessed with Kubernetes at the moment. I first became aware of it watching a Google Dev conference on YouTube a couple of years ago. Bluemix (soon to be known as IBM Cloud) offers a free one node cluster so of course I could stop with just running FIMpy in a container, I had to deploy it within a Kube cluster!

![](../assets/kubernetes.png)

In order to get the deployment to work on a Bluemix cluster, I needed to publish my image to [dockerhub](https://hub.docker.com/r/alanoneill/fimpy/). I could of also created a private Bluemix registry but I already had a dockerhub account from yester-year. Took a little time to figure out the networking with Kubernetes. I couldn't get the internal exposed 5000 port exposed to an external port. With a little help from a collegue, turns out the issue was with the `apiVersion`. Once that was fixed it worked a treat. Next task is to get the SSL working within the cluster.

Here's the deployment yaml.
```yaml
apiVersion: apps/v1beta1
kind: Deployment
metadata:
  name: pyfim-app
  labels:
    app: pyfim-app
spec:
  selector:
    matchLabels:
      app: pyfim-app
  template:
    metadata:
      labels:
        app: pyfim-app
    spec:
      containers:
      - name: pyfim-app
        image: alanoneill/pyfim
        ports:
        - containerPort: 5000
```

And the service yaml.
```yaml
apiVersion: v1
kind: Service
metadata:
  name: pyfim-service
  labels:
    name: pyfim-app
spec:
  type: NodePort
  ports:
    - port: 5000
      targetPort: 5000
      protocol: TCP
      name: pyfim-service
  selector:
    app: pyfim-app
```
