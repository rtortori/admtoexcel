# Tetration ADM to Excel
##### Upload your ADM generated by Cisco Tetration and get it converted in MS Excel format policy file

## Deployment Guide
admtoexcel can be deployed in two ways:<br>
- As a standalone Docker container<br>
- As a Kubernetes deployment<br>

#### Docker container:<br>

`docker run -itd -p 5000:5000 rtortori/secmachine:latest`<br>

connect with a browser to `http://localhost:5000`

#### Kubernetes deployment:<br>

`kubectl create -f https://raw.githubusercontent.com/rtortori/admtoexcel/master/yaml/secmachine.yaml`

Identify your NodePort with:

```
➜  ~ > kubectl get svc -l run=secmachine
NAME         TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
secmachine   NodePort   10.100.120.60   <none>        5000:30346/TCP   41s
```
in this case '30346'.<br>
Connect with your browser to `http://nodeip:30346`

## Usage
Connect to the admtoexcel UI.<br>
From Cisco Tetration, run an ADM and export it in JSON format.<br>
Upload both policies and cluster files below, then press the 'Convert to Excel' button. <br>
Check 'Dynamic ADM' if your ADM is dynamic.<br>
**Note: the files need to be uploaded together and have the suffix 'policies.json' and 'clusters.json'**
<br>
![admtoexcel UI](https://raw.githubusercontent.com/rtortori/admtoexcel/master/screenshots/admtoexcel.png)